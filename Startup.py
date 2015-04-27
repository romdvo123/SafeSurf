import _winreg
file_path = 'W:\Cyber\RomanRepos\SafeSurf\ChangeProxySettings2'
key3 = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, _winreg.KEY_ALL_ACCESS)
key2 = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Run',_winreg.KEY_ALL_ACCESS)
key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Run',_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(key,'SafeSurf',0,_winreg.REG_SZ,file_path) 
key.Close()
