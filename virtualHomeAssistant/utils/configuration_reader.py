import json 

class ConfigurationReader():

    @staticmethod
    def read_config_file(fileName = "data/configuration.json") -> dict:
        with open(fileName, "r") as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
        return data
