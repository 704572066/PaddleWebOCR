import re
import time

import cv2
import numpy as np
import orjson
import logging
from typing import Any
from fastapi import APIRouter, File, UploadFile, Form, status
from fastapi.responses import ORJSONResponse, JSONResponse

from paddlewebocr.pkg.dataelem_ocr import api_call
from paddlewebocr.pkg.util import *
from paddlewebocr.pkg.ocr import text_ocr, text_ocr_v4
from paddlewebocr.pkg.db import save2db, get_imgs, get_texts
from paddlewebocr.pkg.edge import get_receipt_contours
from paddlewebocr.pkg.orientation import orientation_detect
from paddlewebocr.pkg.pair import texts_pair_algorithm_aa, texts_pair_algorithm_bb
from typing import List

mysql_res = None
class MyORJSONResponse(ORJSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY)


router = APIRouter()


@router.post('/ocr')
async def ocr(img_upload: List[UploadFile] = File(None),
              img_b64: str = Form(None),
              compress_size: int = Form(None),
              confidence: float = Form(None),
              ocr_model: str = Form(None),
              language: str = Form(None)):
    start_time = time.time()
    img_bytes = img_upload[0].file.read()
    if img_upload is not None:
        img = convert_bytes_to_image(img_bytes)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})

    img = rotate_image(img)
    img = img.convert("RGB")
    img = compress_image(img, compress_size)

    b64 = convert_image_to_b64(img)

    texts = api_call(b64, language)


    # texts = text_ocr_v4(img, language)[0]

    # 去掉置信度小于0.9的文本
    print(texts)
    i = 0
    while i < len(texts):
        if texts[i][1][1] < confidence:
            texts.pop(i)
            i -= 1
        else:
            i += 1
    # for i, text in enumerate(texts):
    #     if text[1][1] < confidence:
    #         texts.pop(i)
    img_drawed = draw_box_on_image(img.copy(), texts)
    img_drawed_b64 = convert_image_to_b64(img_drawed)

    # save2db("123",img_bytes,img_upload[1].file.read(),'|'.join(list(map(lambda x: x[1][0], texts))))
    data = {'code': 0, 'msg': '成功',
            'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                     'raw_out': list(map(lambda x: [x[0], x[1][0], x[1][1]], texts)),
                     'speed_time': round(time.time() - start_time, 2)}}
    return MyORJSONResponse(content=data)



@router.post('/images')
async def images(vin: str = Form(None)):
    if vin is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})
    results = get_imgs(vin)
    global mysql_res
    mysql_res = []
    # print(mysql_res)
    list = []
    # pair  = []
    for row in results:
        pair = {'id':row[0],'location_img':'data:image/jpeg;base64,'+row[1],'label_img':'data:image/jpeg;base64,'+row[2]}
        # pair.append(row[0])
        # pair.append('data:image/jpeg;base64,'+row[1])
        # pair.append('data:image/jpeg;base64,'+row[2])
        list.append(pair)
        mysql_res.append([row[0], row[3], row[4], row[5], row[6]])

    data = {'code': 0, 'msg': '成功',
            'data': {'images': list}}
    return MyORJSONResponse(content=data)


@router.post('/save')
async def save(img_upload: List[UploadFile] = File(None),
              vin: str = Form(None),
              img_b64: str = Form(None),
              compress_size: int = Form(None),
              confidence: float = Form(None),
              ocr_model: str = Form(None),
              language: str = Form(None)):
    start_time = time.time()
    img_bytes = img_upload[0].file.read()
    if img_upload is not None:
        img = convert_bytes_to_image(img_bytes)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})

    img = rotate_image(img)
    img = img.convert("RGB")
    img = compress_image(img, compress_size)
    # img = item_extract(np.array(img))
    # img = get_receipt_contours(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    # img = orientation_detect(img)
    # img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
    # texts = text_ocr(img, ocr_model)
    # texts = text_ocr_v4(img, language)[0]
    b64 = convert_image_to_b64(img)

    texts = api_call(b64, language)
    # 去掉置信度小于0.9的文本
    # i = 0
    # while i < len(texts):
    #     if texts[i][1][1] < confidence:
    #         texts.pop(i)
    #         i -= 1
    #     else:
    #         i += 1
    img_drawed = draw_box_on_image(img.copy(), texts)
    img_drawed_b64 = convert_image_to_b64(img_drawed)

    save2db(vin,convert_image_to_b64(img),b64encode(img_upload[1].file.read()),'|'.join(list(map(lambda x: x[1][0], texts))),language)
    data = {'code': 0, 'msg': '成功',
            'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                     'raw_out': list(map(lambda x: [x[0], x[1][0], x[1][1]], texts)),
                     'speed_time': round(time.time() - start_time, 2)}}
    return MyORJSONResponse(content=data)


@router.post('/diff')
async def ocr(img_upload: List[UploadFile] = File(None),
              img_b64: str = Form(None),
              compress_size: int = Form(None),
              id: int = Form(None),
              confidence: float = Form(None),
              ocr_model: str = Form(None),
              label_extract: bool = Form(None)):

    start_time = time.time()
    img_bytes = img_upload[0].file.read()
    # print(len(img_bytes))
    if img_upload is not None:
        img = convert_bytes_to_image(img_bytes)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})

    img = rotate_image(img)
    t = time.localtime()
    img = img.convert("RGB")
    img.save("images/ford/%s_%s_%s_%s.jpg" % (time.strftime("%Y-%m-%d-%H-%M-%S", t), id, compress_size, label_extract))

    # 压缩图片
    img = compress_image(img, compress_size)
    texts_confidence = None
    print("++++++++++++++")
    # print(mysql_res)
    if mysql_res is not None:
        for row in mysql_res:
            if row[0] == id:
                texts_confidence = [row[1], row[2], row[3], row[4]]
                # print(row[3])
                break
    else:
        texts_confidence = get_texts(id)

    if label_extract:
        img = get_receipt_contours(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        if img is None:
            data = {'code': 2, 'msg': '图片不合规,提取不到标签,请重新拍摄'}
            return MyORJSONResponse(content=data)
        # 文字方向检测
        # if texts_confidence[2]:
        #     img = orientation_detect(img)
        #     if img is None:
        #         data = {'code': 2, 'msg': '图片不合规,文字方向检测错误,请重新拍摄'}
        #         return MyORJSONResponse(content=data)

        img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
    # texts = text_ocr(img, ocr_model)

    b64 = convert_image_to_b64(img)

    texts = api_call(b64, texts_confidence[3])
    # texts = text_ocr_v4(img, texts_confidence[3])
    # for idx in range(len(texts)):
    #     res = texts[idx]
    #     print(idx)
    #     for line in res:
    #         print(line[1][1])
    if len(texts) == 0:
        data = {'code': 2, 'msg': '图片不合规,提取不到文字,请重新拍摄'}
        return MyORJSONResponse(content=data)

    #
    # print('|'.join(list(map(lambda x: x[1][0], texts))))
    # # 去掉置信度小于0.8的文本
    # i = 0
    # while i < len(texts):
    #     if texts[i][1][1] < texts_confidence[1]:
    #         texts.pop(i)
    #         i -= 1
    #     else:
    #         i += 1
    # print('|'.join(list(map(lambda x: x[1][0], texts))))
    # img_drawed = draw_box_on_image(img.copy(), texts)
    # img_drawed_b64 = convert_image_to_b64(img_drawed)
    # result1 = re.sub(r'[\s,]*', '', '|'.join(list(map(lambda x: x[1][0], texts[0]))))
    #
    # result2 = re.sub(r'[\s,]*', '', texts_confidence[0])
    # print(result1+"\n"+result2)
    # if result1 == result2:
    #     data = {'code': 0, 'msg': '成功', 'data': {'speed_time': round(time.time() - start_time, 2)}}
    # else:
        # list2 = list(map(str, result2.split('|')))
        # list1 = list(map(str, result1.split('|')))
        # length2 = len(list2)
        # length1 = len(list1)
    percentage_a, filter_texts_a = texts_pair_algorithm_aa(texts, texts_confidence[0])
    percentage_b, filter_texts_b = texts_pair_algorithm_bb(texts, texts_confidence[0])
    if percentage_a < percentage_b:
        percentage = percentage_a
        filter_texts = filter_texts_a
    else:
        percentage = percentage_b
        filter_texts = filter_texts_b

    if percentage > 0.3:
        img_drawed = draw_box_on_image(img, filter_texts)
        img_drawed_b64 = convert_image_to_b64(img_drawed)
        data = {'code': 1, 'msg': '失败', 'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                                                   'speed_time': round(time.time() - start_time, 2)}}
        # list(map(lambda x: x, texts))
    else:
        data = {'code': 0, 'msg': '成功', 'data': {'percentage': percentage,'speed_time': round(time.time() - start_time, 2)}}
    # if length1 <= length2:
    #     for i, text in enumerate(list1):
    #         if text != list2[i]:
    #             print(text)
    #             print(list2[i])
    #             img_drawed = draw_one_box_on_image(img, texts[i][0])
    #             break
    # else:
    #     for i, text in enumerate(list1):
    #         if i<length2 and text != list2[i]:
    #             img_drawed = draw_one_box_on_image(img, texts[i][0])
    #             break
    # img_drawed = draw_box_on_image(img.copy(), texts)


    return MyORJSONResponse(content=data)


