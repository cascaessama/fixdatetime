import csv

def get_config(key):
    with open('/home/cascaes/Documents/git/fixdatetime/app.cfg', 'r') as file:
        configs = csv.DictReader(file, delimiter=';')
        for config in configs:
            if config['key'] == key:
                return config['value']