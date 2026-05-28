import re

content = open('gui_app.py', 'rb').read()

match = re.search(
    rb'if self\.current_contact == from_jid:\r?\n\s+self\.refresh_chat_display\(\)\r?\n\s+else:',
    content
)

if match:
    print("Found block at:", match.start())
    old_block = match.group(0)
    nl = b'\r\n' if b'\r\n' in old_block else b'\n'

    new_block = (
        b'if self.current_contact == from_jid:' + nl +
        b'                self.refresh_chat_display()' + nl +
        b'                if msg_id and self.xmpp_service and self.xmpp_service.client and self.xmpp_service.client.is_connected:' + nl +
        b'                    self.xmpp_service.client.send_displayed_marker(from_jid, msg_id)' + nl +
        b'            else:'
    )
    content = content.replace(old_block, new_block)
    open('gui_app.py', 'wb').write(content)
    print("Done!")
else:
    print("Block not found")
    lines = content.split(b'\n')
    for i, line in enumerate(lines):
        if b'current_contact == from_jid' in line:
            print(f"Line {i}:", repr(line))
