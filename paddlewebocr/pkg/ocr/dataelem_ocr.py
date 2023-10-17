import base64
import io

import requests

from PIL.Image import Image

MAX_COMPRESS_SIZE = 1600

server = "http://192.168.11.102:21339"
def dataelem_ocr(b64, scene):
    url = f'{server}/lab/ocr/predict/general'




    # b64 = base64.b64encode(open(image, 'rb').read()).decode()
    # 图片id(可以不添加)，用于唯一标识某张图片，可以在SDK内部日志mlserver.log/socr.log查看到，以便确定图片识别状态。建议只使用数字和字符串
    data = {'id': "1", 'scene': scene, 'image': b64,
    'parameters': {'vis_flag': False, 'sdk': True}}
    res = requests.post(url, json=data).json()
    # json_str = '{"id": "0f1a5a5e-904d-45ed-8f8f-c278310a4e65","status": "success","message": null,"data": {"json": {"general_ocr_res": {"bboxes": [[[320,396],[667,395],[668,433],[321,435]],[[320,396],[667,395],[668,433],[321,435]]],"texts": ["北京市出租汽车专用发票","tee"]},"table_result": null},"resultFile": null,"resultImg": "/9j/4AAQSkZJ……"}}'
    # data = json.loads(json_str)
    # print(res)
    bboxes = res['data']['json']['general_ocr_res']['bboxes']
    texts = res['data']['json']['general_ocr_res']['texts']
    scores_norm = res['data']['json']['general_ocr_res']['scores_norm']
    i = 0
    array = []
    # print(len(bboxes))
    while i < len(bboxes):
        array.append([bboxes[i], (texts[i], scores_norm[i])])
        i += 1
    # return array
    # print(array)
    return array




# res = api_call('../../images/2.jpg','chinese_print')
# bboxes = res['data']['json']['general_ocr_res']['bboxes']
# texts = res['data']['json']['general_ocr_res']['texts']
# i = 0
# array = []
# print(len(bboxes))
# while i < len(bboxes):
#     array.append([bboxes[i],(texts[i],1)])
#     i += 1
# # return array
# print(array)
# 从JSON字符串中加载数据
# json_str = '{"name": "Alice", "age": 25, "address": {"city": "New York", "state": "NY"}, "hobbies": ["reading", "traveling", "swimming"]}'
# data = json.loads(json_str)

# 输出转换后的数据
# print(data)
#
#
# json_str = '{"id": "0f1a5a5e-904d-45ed-8f8f-c278310a4e65","status": "success","message": null,"data": {"json": {"general_ocr_res": {"bboxes": [[[320,396],[667,395],[668,433],[321,435]]],"texts": ["北京市出租汽车专用发票"]},"table_result": null},"resultFile": null,"resultImg": "/9j/4AAQSkZJ……"}}'