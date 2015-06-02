import _winreg as winreg

KEY_SETTINGS = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
    r'Python.File\shell\Edit with IDLE\command',
    0, winreg.KEY_ALL_ACCESS)
name = ''
data, reg_type = winreg.QueryValueEx(KEY_SETTINGS, name)
new_data = '"C:\Python27\pythonw.exe" "C:\Python27\Lib\idlelib\idle.pyw" -n -e "%1"'
winreg.SetValueEx(KEY_SETTINGS, name, 0, reg_type, new_data)

KEY_SETTINGS = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
    r'Python.File\shell\open\command',
    0, winreg.KEY_ALL_ACCESS)
name = ''
data, reg_type = winreg.QueryValueEx(KEY_SETTINGS, name)
new_data = '"C:\Python27\python.exe" "%1" %*'
winreg.SetValueEx(KEY_SETTINGS, name, 0, reg_type, new_data)

KEY_SETTINGS = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
    r'Python.NoConFile\shell\Edit with IDLE\command',
    0, winreg.KEY_ALL_ACCESS)
name = ''
data, reg_type = winreg.QueryValueEx(KEY_SETTINGS, name)
new_data = '"C:\Python27\pythonw.exe" "C:\Python27\Lib\idlelib\idle.pyw" -n -e "%1"'
winreg.SetValueEx(KEY_SETTINGS, name, 0, reg_type, new_data)

KEY_SETTINGS = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
    r'Python.NoConFile\shell\open\command',
    0, winreg.KEY_ALL_ACCESS)
name = ''
data, reg_type = winreg.QueryValueEx(KEY_SETTINGS, name)
new_data = '"C:\Python27\python.exe" "%1" %*'
winreg.SetValueEx(KEY_SETTINGS, name, 0, reg_type, new_data)
