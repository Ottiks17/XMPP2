Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\XMPPClient && venv\Scripts\activate && python main.py", 0, False
