import json
import pprint
import warnings

from kivy import Logger


class ConfUtil():
    @staticmethod
    def load_json_conf(conf_file):
        warnings.filterwarnings("ignore")
        conf = json.load(open(conf_file))

        pp = pprint.PrettyPrinter(indent=4)
        Logger.info("Loaded Json config\n{}".format(pp.pformat(conf)))

        return conf
