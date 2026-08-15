# Copyright (C) 2019 The Electrum developers
# Distributed under the MIT software license, see the accompanying
# file LICENCE or http://www.opensource.org/licenses/mit-license.php
#
# ──────────────────────────────────────────────────────────────────────
# TODO [SECURITY] — Update checker is DISABLED during the testing phase.
#
# The upstream Electrum update checker fetches version info from
# electrum.org and validates it against Bitcoin-mainnet signing keys.
# Neither the URL nor the signing keys are applicable to Electrin.
#
# Before leaving the testing phase:
#   1. Deploy a version-announcement endpoint on electrin.net (or the
#      Electrin GitHub Releases API).
#   2. Generate Rincoin-mainnet signing keys for version announcements
#      (see SECURITY.md for the key-generation procedure).
#   3. Replace `url`, `download_url`, and
#      `VERSION_ANNOUNCEMENT_SIGNING_KEYS` below with the new values.
#   4. Re-enable the update checker in this file and in main_window.py.
#   5. Remove the DISABLED guard from `UpdateCheckThread.run()`.
#
# Until these steps are completed the update check will always report
# "disabled" so that no data is sent to third-party servers.
# ──────────────────────────────────────────────────────────────────────

import asyncio
import base64
import re
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QPushButton, QDialog

from electrum import version
from electrum import constants
from electrum.bitcoin import verify_usermessage_with_address
from electrum.i18n import _
from electrum.util import make_aiohttp_session
from electrum.logging import Logger
from electrum.network import Network
from electrum._vendor.distutils.version import StrictVersion

# TODO [SECURITY] — Replace with Electrin's own URLs and signing keys
#                    before production release.
_UPDATE_CHECK_DISABLED = True  # flip to False once Electrin infrastructure is ready


class UpdateCheck(QDialog, Logger):
    url = "https://electrum.org/version"              # TODO: change to electrin.net endpoint
    download_url = "https://electrum.org/#download"    # TODO: change to electrin.net download page

    VERSION_ANNOUNCEMENT_SIGNING_KEYS = (
        # TODO [SECURITY] — These are upstream Electrum Bitcoin-mainnet keys.
        #   Replace with Electrin/Rincoin keys before enabling update checks.
        "13xjmVAB1EATPP8RshTE8S8sNwwSUM9p1P",  # ThomasV (since 3.3.4)  — UPSTREAM, NOT OURS
        "1Nxgk6NTooV4qZsX5fdqQwrLjYcsQZAfTg",  # ghost43 (since 4.1.2)  — UPSTREAM, NOT OURS
    )

    def __init__(self, *, latest_version=None):
        QDialog.__init__(self)
        self.setWindowTitle('Electrin - ' + _('Update Check'))
        self.content = QVBoxLayout()
        self.content.setContentsMargins(*[10]*4)

        self.heading_label = QLabel()
        self.content.addWidget(self.heading_label)

        self.detail_label = QLabel()
        self.detail_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.detail_label.setOpenExternalLinks(True)
        self.content.addWidget(self.detail_label)

        self.pb = QProgressBar()
        self.pb.setMaximum(0)
        self.pb.setMinimum(0)
        self.content.addWidget(self.pb)

        versions = QHBoxLayout()
        versions.addWidget(QLabel(_("Current version: {}").format(version.ELECTRIN_VERSION)))
        self.latest_version_label = QLabel(_("Latest version: {}").format(" "))
        versions.addWidget(self.latest_version_label)
        self.content.addLayout(versions)

        self.update_view(latest_version)

        if not _UPDATE_CHECK_DISABLED:
            self.update_check_thread = UpdateCheckThread()
            self.update_check_thread.checked.connect(self.on_version_retrieved)
            self.update_check_thread.failed.connect(self.on_retrieval_failed)
            self.update_check_thread.start()
        else:
            self.pb.hide()
            self.heading_label.setText('<h2>' + _("Update check is disabled") + '</h2>')
            self.detail_label.setText(
                _("Automatic update checking is disabled during the testing phase.") + "<br><br>" +
                _("Please check for updates manually at") + " " +
                "<a href='https://github.com/takologi/electrin/releases'>GitHub Releases</a>."
            )

        close_button = QPushButton(_("Close"))
        close_button.clicked.connect(self.close)
        self.content.addWidget(close_button)
        self.setLayout(self.content)
        self.show()

    def on_version_retrieved(self, version):
        self.update_view(version)

    def on_retrieval_failed(self):
        self.heading_label.setText('<h2>' + _("Update check failed") + '</h2>')
        self.detail_label.setText(_("Sorry, but we were unable to check for updates. Please try again later."))
        self.pb.hide()

    @staticmethod
    def is_newer(latest_version):
        # StrictVersion only accepts 'X.Y.Z' or 'X.Y.Z[ab]N' forms, so
        # ELECTRIN_VERSION's '-beta.N'/'-rc.N' suffixes (e.g. '1.0.0-beta.1')
        # need normalizing to that form (e.g. '1.0.0b1') for comparison.
        local = re.sub(r'-beta\.?(\d+)$', r'b\1', version.ELECTRIN_VERSION)
        local = re.sub(r'-rc\.?(\d+)$', r'c\1', local)
        return latest_version > StrictVersion(local)

    def update_view(self, latest_version=None):
        if latest_version:
            self.pb.hide()
            self.latest_version_label.setText(_("Latest version: {}").format(latest_version))
            if self.is_newer(latest_version):
                self.heading_label.setText('<h2>' + _("There is a new update available") + '</h2>')
                url = "<a href='{u}'>{u}</a>".format(u=UpdateCheck.download_url)
                self.detail_label.setText(_("You can download the new version from {}.").format(url))
            else:
                self.heading_label.setText('<h2>' + _("Already up to date") + '</h2>')
                self.detail_label.setText(_("You are already on the latest version of Electrin."))
        else:
            self.heading_label.setText('<h2>' + _("Checking for updates...") + '</h2>')
            self.detail_label.setText(_("Please wait while Electrin checks for available updates."))


class UpdateCheckThread(QThread, Logger):
    checked = pyqtSignal(object)
    failed = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        Logger.__init__(self)
        self.network = Network.get_instance()
        self._fut = None  # type: Optional[asyncio.Future]

    async def get_update_info(self):
        # note: Use long timeout here as it is not critical that we get a response fast,
        #       and it's bad not to get an update notification just because we did not wait enough.
        async with make_aiohttp_session(proxy=self.network.proxy, timeout=120) as session:
            async with session.get(UpdateCheck.url) as result:
                signed_version_dict = await result.json(content_type=None)
                # example signed_version_dict:
                # {
                #     "version": "3.9.9",
                #     "signatures": {
                #         "1Lqm1HphuhxKZQEawzPse8gJtgjm9kUKT4": "IA+2QG3xPRn4HAIFdpu9eeaCYC7S5wS/sDxn54LJx6BdUTBpse3ibtfq8C43M7M1VfpGkD5tsdwl5C6IfpZD/gQ="
                #     }
                # }
                version_num = signed_version_dict['version']
                sigs = signed_version_dict['signatures']
                for address, sig in sigs.items():
                    if address not in UpdateCheck.VERSION_ANNOUNCEMENT_SIGNING_KEYS:
                        continue
                    sig = base64.b64decode(sig, validate=True)
                    msg = version_num.encode('utf-8')
                    if verify_usermessage_with_address(
                        address=address, sig65=sig, message=msg,
                        net=constants.BitcoinMainnet
                    ):
                        self.logger.info(f"valid sig for version announcement '{version_num}' from address '{address}'")
                        break
                else:
                    raise Exception('no valid signature for version announcement')
                return StrictVersion(version_num.strip())

    def run(self):
        # TODO [SECURITY] — Update checker disabled during testing phase.
        #   Do not contact electrum.org from Electrin. See module docstring.
        if _UPDATE_CHECK_DISABLED:
            self.logger.info("update check is disabled during testing phase")
            self.failed.emit()
            return
        if not self.network:
            self.failed.emit()
            return
        self._fut = asyncio.run_coroutine_threadsafe(self.get_update_info(), self.network.asyncio_loop)
        try:
            update_info = self._fut.result()
        except Exception as e:
            self.logger.info(f"got exception: '{repr(e)}'")
            self.failed.emit()
        else:
            self.checked.emit(update_info)

    def stop(self):
        if self._fut:
            self._fut.cancel()
        self.exit()
        self.wait()
