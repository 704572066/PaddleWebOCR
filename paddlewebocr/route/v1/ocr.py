import re
import time

import cv2
import numpy as np
import orjson
import logging
from typing import Any
from fastapi import APIRouter, File, UploadFile, Form, status
from fastapi.responses import ORJSONResponse, JSONResponse
from paddlewebocr.pkg.util import *
from paddlewebocr.pkg.ocr import text_ocr
from paddlewebocr.pkg.db import save2db, get_imgs, get_texts
from paddlewebocr.pkg.edge import get_receipt_contours
from paddlewebocr.pkg.orientation import orientation_detect
from paddlewebocr.pkg.pair import texts_pair
from typing import List

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
              ocr_model: str = Form(None)):
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

    texts = text_ocr(img, ocr_model)
    # 去掉置信度小于0.9的文本
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
    list = []
    # pair  = []
    for row in results:
        pair = {'id':row[0],'location_img':'data:image/jpeg;base64,'+row[1],'label_img':'data:image/jpeg;base64,'+row[2]}
        # pair.append(row[0])
        # pair.append('data:image/jpeg;base64,'+row[1])
        # pair.append('data:image/jpeg;base64,'+row[2])
        list.append(pair)

    data = {'code': 0, 'msg': '成功',
            'data': {'images': list}}
    return MyORJSONResponse(content=data)


@router.post('/save')
async def save(img_upload: List[UploadFile] = File(None),
              vin: str = Form(None),
              img_b64: str = Form(None),
              compress_size: int = Form(None),
              confidence: float = Form(None),
              ocr_model: str = Form(None)):
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
    img = get_receipt_contours(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
    texts = text_ocr(img, ocr_model)
    # 去掉置信度小于0.9的文本
    i = 0
    while i < len(texts):
        if texts[i][1][1] < confidence:
            texts.pop(i)
            i -= 1
        else:
            i += 1
    img_drawed = draw_box_on_image(img.copy(), texts)
    img_drawed_b64 = convert_image_to_b64(img_drawed)

    save2db(vin,convert_image_to_b64(img),b64encode(img_upload[1].file.read()),'|'.join(list(map(lambda x: x[1][0], texts))))
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
              ocr_model: str = Form(None)):
    start_time = time.time()
    img_bytes = img_upload[0].file.read()
    print(len(img_bytes))
    if img_upload is not None:
        img = convert_bytes_to_image(img_bytes)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})

    img = rotate_image(img)
    img = img.convert("RGB")
    # 不压缩图片
    img = compress_image(img, compress_size)
    # img = item_extract(np.array(img))
    img = get_receipt_contours(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    if img is None:
        data = {'code': 2, 'msg': '图片不合规,提取不到标签,请重新拍摄'}
        return MyORJSONResponse(content=data)

    img = orientation_detect(img)
    img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
    texts = text_ocr(img, ocr_model)

    if len(texts) == 0:
        data = {'code': 2, 'msg': '图片不合规,提取不到文字,请重新拍摄'}
        return MyORJSONResponse(content=data)

    print('|'.join(list(map(lambda x: x[1][0], texts))))
    # 去掉置信度小于0.8的文本
    i = 0
    while i < len(texts):
        if texts[i][1][1] < confidence:
            texts.pop(i)
            i -= 1
        else:
            i += 1
    print('|'.join(list(map(lambda x: x[1][0], texts))))
    # img_drawed = draw_box_on_image(img.copy(), texts)
    # img_drawed_b64 = convert_image_to_b64(img_drawed)
    result1 = re.sub(r'[\s,]*', '', '|'.join(list(map(lambda x: x[1][0], texts))))

    result2 = re.sub(r'[\s,]*', '', get_texts(id)[0])
    print(result1+"\n"+result2)
    if result1 == result2:
        data = {'code': 0, 'msg': '成功', 'data': {'speed_time': round(time.time() - start_time, 2)}}
    else:
        # list2 = list(map(str, result2.split('|')))
        # list1 = list(map(str, result1.split('|')))
        # length2 = len(list2)
        # length1 = len(list1)
        percentage, filter_texts = texts_pair(texts, get_texts(id)[0])
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


