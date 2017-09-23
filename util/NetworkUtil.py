import netifaces as ni

class NetworkUtil(object):
    interfaces = ('wlan0', 'eth0', 'en0')

    maxLength = {
        "interface": 16,
        "essid": 32
    }
    calls = {
        "SIOCGIWESSID": 0x8B1B
    }


    @staticmethod
    def getIp():
        avail_interfaces = ni.interfaces()

        for interface in NetworkUtil.interfaces:
            if interface in avail_interfaces:
                ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

                if ip:
                    break


        return ip
