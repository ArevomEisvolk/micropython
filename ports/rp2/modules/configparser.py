import ujson

class ConfigParser:
    """Klasse um die Parameter Datei 'parameter.wl' zu lesen/bearbeiten"""
    
    def __init__(self, path):
        self.path = path
        self.parameter = {}

    def read_config(self):
        try:
            self.parameter = ujson.load(open(self.path))
        except:
            print("Beim Lesen der Konfigurationdatei ist ein Fehler augetreten, Sie ist Defekt oder Leer")
            
    def return_category(self, key : str):
        key = key.upper()
        if self.parameter.get(key):

            return self.parameter[key]
        else:
            raise Exception("Die Konfigurationdatei ist Defekt oder Unzureichend Konfiguriert")

    def update_category(self, key : str, value : dict):
        key = key.upper()
        if self.parameter.get(key):
            self.parameter[key] = value
        elif key in ["SETUP", "GRPS", "SMTP"]:
            self.parameter[key] = value
        else:
            raise Exception("Es gab einen Eingabe Fehler {0}".format(key))

    def write_config(self):
        with open(self.path, "w") as configfile:
            ujson.dump(self.parameter, configfile)
            