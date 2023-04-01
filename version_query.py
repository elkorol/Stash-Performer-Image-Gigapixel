import winreg

def get_program_info(program_name):
    # Specify the path to the key that contains a list of installed programs
    key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'

    # Open the key that contains the list of installed programs
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)

    # Iterate through the subkeys to find the program you want to query
    for i in range(winreg.QueryInfoKey(key)[0]):
        subkey_name = winreg.EnumKey(key, i)
        subkey = winreg.OpenKey(key, subkey_name)
        try:
            # Check if the program name is in the DisplayName value
            display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
            if program_name in display_name:
                # If the program name is in the DisplayName value, get the program key
                program_key = subkey_name
                break
        except OSError:
            pass
        winreg.CloseKey(subkey)

    # Close the installed programs key
    winreg.CloseKey(key)

    # Check if the program key was found, and return None if not
    if not program_key:
        return None
    else:
        # Use the program key to get the version information and installation path
        key_path = fr'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{program_key}'
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        version = winreg.QueryValueEx(key, 'DisplayVersion')[0]
        install_location = winreg.QueryValueEx(key, 'InstallLocation')[0]
        exe_path = winreg.QueryValueEx(key, 'DisplayIcon')[0]
        winreg.CloseKey(key)
        return version, install_location, exe_path