import json
import pprint
import warnings

from jsmin import jsmin
from kivy import Logger


class ConfUtil(object):
    @staticmethod
    def load_json_conf(conf_file):
        warnings.filterwarnings("ignore")
        with open(conf_file, "r") as myfile:
            data = myfile.read()
            js_min = jsmin(data)
            conf = json.loads(js_min)

        pp = pprint.PrettyPrinter(indent=4)
        Logger.info("Loaded Json config\n{}".format(pp.pformat(conf)))

        return conf
