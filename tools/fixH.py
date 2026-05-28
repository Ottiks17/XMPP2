import re

content = open('gui_app.py', 'rb').read()

old = b'        QTimer.singleShot(3000, self.auto_start)\n'
new = (
    b'        QTimer.singleShot(3000, self.auto_start)\n'
    b'        QTimer.singleShot(5000, self.check_for_updates)\n'
)

print("Found timer:", old in content)
if old in content:
    content = content.replace(old, new)

old2 = b'    def auto_start(self):\n'
new2 = (
    b'    def check_for_updates(self):\n'
    b'        try:\n'
    b'            from updater import check_for_updates\n'
    b'            def on_update_check(has_update, latest_version, download_url):\n'
    b'                if has_update:\n'
    b'                    QMetaObject.invokeMethod(self, "_show_update_dialog",\n'
    b'                        Qt.QueuedConnection,\n'
    b'                        Q_ARG(str, latest_version),\n'
    b'                        Q_ARG(str, download_url or ""))\n'
    b'            check_for_updates(on_update_check)\n'
    b'        except Exception:\n'
    b'            pass\n'
    b'\n'
    b'    @pyqtSlot(str, str)\n'
    b'    def _show_update_dialog(self, latest_version, download_url):\n'
    b'        from version import VERSION\n'
    b'        msg = QMessageBox(self)\n'
    b'        msg.setWindowTitle("\xd0\x9e\xd0\xb1\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd0\xbe")\n'
    b'        msg.setText(f"\xd0\x94\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd0\xb0 \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x8f \xd0\xb2\xd0\xb5\xd1\x80\xd1\x81\xd0\xb8\xd1\x8f {latest_version} (\xd1\x82\xd0\xb5\xd0\xba\xd1\x83\xd1\x89\xd0\xb0\xd1\x8f: {VERSION}).\\n\xd0\xa5\xd0\xbe\xd1\x82\xd0\xb8\xd1\x82\xd0\xb5 \xd1\x81\xd0\xba\xd0\xb0\xd1\x87\xd0\xb0\xd1\x82\xd1\x8c?")\n'
    b'        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)\n'
    b'        if msg.exec_() == QMessageBox.Yes:\n'
    b'            import webbrowser\n'
    b'            webbrowser.open(download_url if download_url else "https://github.com/Ottiks17/XMPP2/releases/latest")\n'
    b'\n'
    b'    def auto_start(self):\n'
)

print("Found auto_start:", old2 in content)
if old2 in content:
    content = content.replace(old2, new2)
    open('gui_app.py', 'wb').write(content)
    print("Done!")
