import _winreg as winreg, ctypes, time

INTERNET_OPTION_REFRESH = 37
INTERNET_OPTION_SETTINGS_CHANGED = 39
INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, winreg.KEY_ALL_ACCESS)
internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

def set_key(name, value):
    try:
        _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
    except WindowsError:
        if name == 'ProxyEnable':
            reg_type = winreg.REG_DWORD
        elif name == 'ProxyServer':
            reg_type = winreg.REG_SZ        
    winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
enabled = 0
if enabled:
    print "Proxy enabled"
else:
    print "Proxy disabled"
while 1:
    set_key('ProxyEnable', enabled)
    set_key('ProxyServer', u'10.20.30.114:8082')
    winreg.CloseKey(INTERNET_SETTINGS)
    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, winreg.KEY_ALL_ACCESS)
    time.sleep(1)

