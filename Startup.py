import _winreg
file_path = 'W:\Cyber\RomanRepos\SafeSurf\ChangeProxySettingswin.pyw'
key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Run',_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(key,'SafeSurf',0,_winreg.REG_SZ,file_path) 
key.Close()
