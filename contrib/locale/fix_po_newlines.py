#!/usr/bin/env python3
"""
Fix .po files where msgid and msgstr have mismatched leading/trailing \\n.
These cause "fatal error" from msgfmt which skips generating the .mo file for
those languages.

Rules applied:
  - If msgid does NOT begin with \\n but msgstr does, strip leading \\n lines from msgstr.
  - If msgid does NOT end with \\n but msgstr does, strip trailing \\n from msgstr
    (and drop any trailing empty "" continuation line).
  - Vice-versa cases (msgid has \\n but msgstr doesn't) are left alone; those are
    just untranslated lines, which msgfmt handles gracefully.
"""
import re
import sys
import os
import glob


def decode_po_string(lines):
    """Concatenate the content of a list of po string lines (each is a quoted string)."""
    result = []
    for line in lines:
        m = re.match(r'^\s*"(.*)"\s*$', line)
        if m:
            # Interpret only \\n (the two-char sequence in the file)
            result.append(m.group(1))
    return ''.join(result)


def fix_po_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into logical entries separated by blank lines
    # We work on the raw text with regex to preserve everything else
    changed = False

    # Pattern: find msgid + msgstr pairs and fix newline mismatches
    # Match a full entry: msgid (possibly multiline) followed by msgstr (possibly multiline)
    entry_re = re.compile(
        r'(msgid\s+".*?"(?:\n".*?")*)\n'   # msgid lines
        r'(msgstr\s+".*?"(?:\n".*?")*)',    # msgstr lines
        re.DOTALL
    )

    def fix_entry(m):
        nonlocal changed
        msgid_block = m.group(1)
        msgstr_block = m.group(2)

        msgid_val = decode_po_string(msgid_block.splitlines())
        msgstr_val = decode_po_string(msgstr_block.splitlines())

        if not msgstr_val:  # empty/untranslated, leave alone
            return m.group(0)

        new_msgstr_block = msgstr_block
        modified = False

        # --- Fix leading \n mismatch ---
        if not msgid_val.startswith('\\n') and msgstr_val.startswith('\\n'):
            # Remove leading "\n" lines from msgstr
            lines = new_msgstr_block.splitlines(keepends=True)
            # First line is msgstr "..." - check if it's just "\n"
            # Remove lines after the first that are pure "\n" strings
            result_lines = [lines[0]]
            # If the first line's content is only \n, replace with empty string
            first_m = re.match(r'^(msgstr\s+)"(\\n)+"(\s*)$', lines[0])
            if first_m:
                # The whole first line is just newlines - replace with msgstr ""
                # and keep looking at continuation lines
                result_lines = [first_m.group(1) + '""' + first_m.group(3) + '\n']
                for line in lines[1:]:
                    if re.match(r'^\s*"\\n"\s*$', line):
                        continue  # skip pure \n continuation lines
                    result_lines.append(line)
                # If we ended up with msgstr "" followed by nothing useful, skip
                # Check if there's real content after
                rest = ''.join(result_lines[1:]).strip()
                if not rest:
                    result_lines = result_lines  # keep the empty msgstr
            new_msgstr_block = ''.join(result_lines)
            modified = True

        # --- Fix trailing \n mismatch ---
        if not msgid_val.endswith('\\n') and msgstr_val.endswith('\\n'):
            lines = new_msgstr_block.splitlines(keepends=True)
            # Remove trailing empty "" continuation lines first
            while len(lines) > 1 and re.match(r'^\s*""\s*$', lines[-1]):
                lines = lines[:-1]
            # Now remove trailing \n from the last content line
            if lines:
                last = lines[-1]
                # Replace trailing \\n" with just "
                new_last = re.sub(r'\\n(")\s*$', r'\1', last)
                if new_last != last:
                    lines[-1] = new_last
                    modified = True
            new_msgstr_block = ''.join(lines)

        if modified:
            changed = True
            return msgid_block + '\n' + new_msgstr_block

        return m.group(0)

    new_content = entry_re.sub(fix_entry, content)

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  fixed: {os.path.basename(os.path.dirname(path))}/{os.path.basename(path)}")


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_po_newlines.py <locale_dir>")
        sys.exit(1)
    locale_dir = sys.argv[1]
    for po_file in sorted(glob.glob(os.path.join(locale_dir, '*', 'electrum.po'))):
        fix_po_file(po_file)


if __name__ == '__main__':
    main()
