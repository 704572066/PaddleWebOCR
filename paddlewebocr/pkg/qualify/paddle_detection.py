
import requests
import json
import base64
from ast import literal_eval
def det(image_data):
    url = f"http://192.168.11.102:21502/ppdet/prediction"
    logid = 10000
    # base64 encode
    image = base64.b64encode(image_data).decode('utf8')

    data = {"key": ["image_0"], "value": [image], "logid": logid}
    # send requests
    r = requests.post(url=url, data=json.dumps(data))
    print(literal_eval(r.json()['value'][0])[0].split())
    array = list(float(char) for char in literal_eval(r.json()['value'][0])[0].split())
    # res_json = r.json()['value']
    print(array[-4:])
    return array[-4:]
    # return r.json()
