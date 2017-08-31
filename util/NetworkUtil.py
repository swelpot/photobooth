import netifaces as ni

class NetworkUtil():
    interface = 'en0'

    maxLength = {
        "interface": 16,
        "essid": 32
    }
    calls = {
        "SIOCGIWESSID": 0x8B1B
    }


    @staticmethod
    def getIp():
        ni.ifaddresses(NetworkUtil.interface)
        ip = ni.ifaddresses(NetworkUtil.interface)[ni.AF_INET][0]['addr']
        return ip
