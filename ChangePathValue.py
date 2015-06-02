import _winreg as winreg

ENVIRONMENT_SETTINGS = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
    r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    0, winreg.KEY_ALL_ACCESS)
name = 'Path'
data, reg_type = winreg.QueryValueEx(ENVIRONMENT_SETTINGS, name)
print data
python26 = r'c:\Python26'
pythonscripts26 = r'c:\Python26\Scripts'
python27 =  r'c:\Python27'
pythonscripts27 = r'c:\Python27\Scripts'
split_data = data.split(';')
new_data = ''
for value in split_data:
    if value == python26:
        new_data = new_data + python27 + ';'
    elif value == pythonscripts26:
        new_data = new_data + pythonscripts27 + ';'
    else:
        new_data = new_data + value + ';'
new_data = new_data[:-1]
print new_data
winreg.SetValueEx(ENVIRONMENT_SETTINGS, name, 0, reg_type, new_data)
