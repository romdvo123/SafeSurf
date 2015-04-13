import _winreg as winreg, ctypes

def set_key(name, value):
    try:
        _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
    except WindowsError:
        if name == 'ProxyEnable':
            reg_type = winreg.REG_DWORD
        elif name == 'ProxyServer':
            reg_type = winreg.REG_SZ
            
    winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
        

INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, winreg.KEY_ALL_ACCESS)

set_key('ProxyEnable', 0)
set_key('ProxyServer', u'10.20.30.100:8081')
winreg.CloseKey(INTERNET_SETTINGS)

INTERNET_OPTION_REFRESH = 37
INTERNET_OPTION_SETTINGS_CHANGED = 39

internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
