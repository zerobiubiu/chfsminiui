import platform

def judgeOS():
    os = platform.system().lower()
    architecture = platform.machine()

    if os == 'windows':
        return "chfswindowsamd.exe"
    elif os == 'linux':
        if architecture == 'arm64':
            return "chfslinuxarm"
        elif architecture == 'AMD64':
            return "chfslinuxamd"
        else:
            return ""
    elif os == 'darwin':
        return "chfsmacamd"
    else:
        return ""