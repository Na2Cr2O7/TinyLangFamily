import json
import configparser
config = configparser.ConfigParser()
# config.read('datasetINI.ini','w')
config.add_section('g')
with open('datasetTiny.json','r',encoding='utf8') as f:
    data=json.load(f)
for key,value in data.items():
    try:

        config.set('g',key,value)
    except Exception as e:
        print(e)
with open('datasetINI.ini','w',encoding='utf8') as f:
    config.write(f)
