import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Item {
    readonly property int paddingXXSmall: 4
    readonly property int paddingXSmall: 6
    readonly property int paddingSmall: 8
    readonly property int paddingMedium: 12
    readonly property int paddingLarge: 16
    readonly property int paddingXLarge: 20
    readonly property int paddingXXLarge: 28

    readonly property int fontSizeXSmall: 10
    readonly property int fontSizeSmall: 12
    readonly property int fontSizeMedium: 15
    readonly property int fontSizeLarge: 18
    readonly property int fontSizeXLarge: 22
    readonly property int fontSizeXXLarge: 28

    readonly property int iconSizeXSmall: 12
    readonly property int iconSizeSmall: 16
    readonly property int iconSizeMedium: 24
    readonly property int iconSizeLarge: 32
    readonly property int iconSizeXLarge: 48
    readonly property int iconSizeXXLarge: 64

    readonly property int fingerWidth: 64 // TODO: determine finger width from screen dimensions and resolution

    // Whether the active Material theme is dark (used for colour branching)
    readonly property bool isDark: Material.theme === Material.Dark

    property color mutedForeground: 'gray'
    property color darkerBackground: Qt.darker(Material.background, 1.20)
    property color darkerDialogBackground: Qt.darker(Material.dialogColor, 1.20)
    property color highlightBackground: Qt.lighter(Material.background, 1.30)
    property color dialogColor: Material.dialogColor
    property color seedTextAreaBackground: Qt.darker(darkerDialogBackground, 1.20)
    property color notificationBackground: Qt.lighter(Material.background, isDark ? 1.5 : 0.92)

    property color colorCredit: isDark ? "#ff80ff80" : "#ff00a000"
    property color colorDebit: isDark ? "#ffff8080" : "#ffc00000"

    property color colorInfo: Material.accentColor
    property color colorWarning: isDark ? 'yellow' : '#cc8800'
    property color colorError: isDark ? '#ffff8080' : '#ffc00000'
    property color colorProgress: isDark ? '#ffffff80' : '#cc8800'
    property color colorDone: isDark ? '#ff80ff80' : '#ff00a000'
    property color colorValidBackground: '#ff008000'
    property color colorInvalidBackground: '#ff800000'
    property color colorAcceptable: isDark ? '#ff8080ff' : '#ff4040d0'
    property color colorOk: colorDone

    property color colorLightningLocal: "#6060ff"
    property color colorLightningLocalReserve: "#0000a0"
    property color colorLightningRemote: isDark ? "yellow" : "#cc8800"
    property color colorLightningRemoteReserve: Qt.darker(colorLightningRemote, 1.5)
    property color colorChannelOpen: isDark ? "#ff80ff80" : "#ff00a000"

    property color colorPiechartTotal: Material.accentColor
    property color colorPiechartOnchain: Qt.darker(Material.accentColor, 1.50)
    property color colorPiechartFrozen: 'gray'
    property color colorPiechartLightning: 'orange'
    property color colorPiechartLightningFrozen: Qt.darker('orange', 1.20)
    property color colorPiechartUnconfirmed: Qt.darker(Material.accentColor, 2.00)
    property color colorPiechartUnmatured: 'magenta'

    property color colorPiechartParticipant: 'gray'
    property color colorPiechartSignature: isDark ? 'yellow' : '#cc8800'

    property color colorAddressExternal: isDark ? "#8af296" : "#1a7a28"
    property color colorAddressInternal: isDark ? "#ffff00" : "#cc8800"
    property color colorAddressUsed: Qt.rgba(0.5,0.5,0.5,1)
    property color colorAddressUsedWithBalance: isDark ? Qt.rgba(0.75,0.75,0.75,1) : Qt.rgba(0.35,0.35,0.35,1)
    property color colorAddressFrozen: Qt.rgba(0.5,0.5,1,1)
    property color colorAddressBilling: "#8cb3f2"
    property color colorAddressSwap: colorAddressBilling
    property color colorAddressAccounting: "#ff9b45"

    function colorAlpha(baseColor, alpha) {
        return Qt.rgba(baseColor.r, baseColor.g, baseColor.b, alpha)
    }
}
