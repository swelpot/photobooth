import logging
import httplib, urllib
import datetime


class PushoverSender():
    @staticmethod
    def send(conf, message):
        timestamp = datetime.datetime.now()
        device = conf.get("pushover.device")

        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST", "/1/messages.json",
            urllib.urlencode({
                "token": conf.get("pushover.api_token"),
                "user": conf.get("pushover.user_key"),
                "device": device,
                "title": conf.get("pushover.message_title"),
                "message": message,
                "priority": 0
            }), {"Content-type": "application/x-www-form-urlencoded"})
        resp = conn.getresponse()

        status = resp.status

        if status is not 200:
            logging.error("error sending pushover notification to device [{}]".format(device))
            return False

        logging.info("sent pushover notification to device [{}]".format(device))

        return True


if __name__ == '__main__':
    conf = {"pushover.user_key": "udx9eymet9d68egrfoymrnqdh519ou",
            "pushover.api_token": "akbhx62gwpm99h58paqotq1vqg2ejm",
            "pushover.message_title": "Photobooth",
            "pushover.device": "iphonestefan"}

PushoverSender.send(conf, "Testmessage")
