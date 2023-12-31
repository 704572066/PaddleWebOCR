import collections
import time
import uuid
import cv2
import numpy as np
import orjson
from typing import Any

from fastapi import APIRouter, File, UploadFile, Form, status
from fastapi.responses import ORJSONResponse, JSONResponse

from paddlewebocr.pkg.ocr.baidu_ocr import baidu_ocr
from paddlewebocr.pkg.ocr.dataelem_ocr import dataelem_ocr
from paddlewebocr.pkg.ocr.huawei_ocr import huawei_ocr
from paddlewebocr.pkg.qualify.label_qualify import label_qualify
from paddlewebocr.pkg.qualify.paddle_detection import det
from paddlewebocr.pkg.util import *
from paddlewebocr.pkg.db import save2db, get_imgs, get_texts
from paddlewebocr.pkg.edge import get_receipt_contours
from paddlewebocr.pkg.pair import texts_pair_algorithm_aa, texts_pair_algorithm_bb, split_texts, texts_pair_algorithm
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
    # quality, ratio = label_qualify(img_bytes, 0.8)
    # print(ratio)
    #
    # if quality is False:
    #     data = {'code': 2, 'msg': '图片不合规,提取不到文字,请重新拍摄', 'ratio': ratio}
    #     return MyORJSONResponse(content=data)


    if img_upload is not None:
        img = convert_bytes_to_image(img_bytes)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})


    # points = det(img_bytes)
    # img = img.convert("RGB")
    # img = compress_image(img, compress_size)

    if ocr_model == "huawei":
        b64 = convert_image_to_b64(img)
        texts = huawei_ocr(b64)
        texts = split_texts(texts)
    elif ocr_model == "dataelem":
        # dataelem_ocr
        b64 = convert_image_to_b64(img)
        dataelem_language = ((language == "en") and "english_print" or "chinese_print")
        texts = dataelem_ocr(b64, dataelem_language)
        if(language == "ch"):
            texts = split_texts(texts)
    else:
        # paddleocr
        img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
        # language = ( (language == "en") and "english_print" or "chinese_print")
        texts = baidu_ocr(img, language)[0]







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
    # 添加ppdet检测边框
    # img_drawed = draw_det_box_on_image(img_drawed, points)

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
        pair = {'id':row[0],'location_img':'data:image/jpeg;base64,'+row[1],'label_img':'data:image/jpeg;base64,'+row[2],'rotate':row[9],'margin':row[10],'frame_rotate':row[11]}
        # pair.append(row[0])
        # pair.append('data:image/jpeg;base64,'+row[1])
        # pair.append('data:image/jpeg;base64,'+row[2])
        list.append(pair)
        mysql_res.append([row[0], row[3], row[4], row[5], row[6],row[7],row[8],row[9]])

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

    if ocr_model == "huawei":
        b64 = convert_image_to_b64(img)
        texts = huawei_ocr(b64)
        texts = split_texts(texts)
    elif ocr_model == "dataelem":
        # dataelem_ocr
        b64 = convert_image_to_b64(img)
        dataelem_language = ((language == "en") and "english_print" or "chinese_print")
        texts = dataelem_ocr(b64, dataelem_language)
        if(language == "ch"):
            texts = split_texts(texts)
    else:
        # paddleocr
        img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
        # language = ( (language == "en") and "english_print" or "chinese_print")
        texts = baidu_ocr(img, language)[0]

    # b64 = convert_image_to_b64(img)
    # dataelem_language = ((language == "en") and "english_print" or "chinese_print")
    # texts = dataelem_ocr(b64, dataelem_language)
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
    print(len(img_bytes))
    if img_upload is not None:
        img = convert_bytes_to_image(img_bytes)
    elif img_b64 is not None:
        img = convert_b64_to_image(img_b64)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'code': 4001, 'msg': '没有传入参数'})

    img = rotate_image(img)
    t = time.localtime()
    # img = img.convert("RGB")
    uid = uuid.uuid4()
    img.save("images/ford/original/%s_%s_%s_%s_original.jpg" % (time.strftime("%Y-%m-%d-%H-%M-%S",t), id, compress_size, label_extract), format="JPEG", quality=100)

    # 压缩图片
    img = compress_image(img, compress_size)

    img.save("images/ford/compress/"
             "/%s_%s_%s_%s_compress.jpg" % (time.strftime("%Y-%m-%d-%H-%M-%S", t), id, compress_size, label_extract), format="JPEG", quality=100)

    texts_confidence = None
    print("++++++++++++++")
    # print(mysql_res)
    if mysql_res is not None:
        for row in mysql_res:
            if row[0] == id:
                texts_confidence = [row[1], row[2], row[3], row[4],row[5],row[6],row[7]]
                # print(row[3])
                break
    else:
        texts_confidence = get_texts(id)

    if label_extract:
        quality, ratio = label_qualify(convert_image_to_bytes(img), 0.1)
        print(ratio)
        if quality is False:
            data = {'code': 2, 'msg': '图片不合规,提取不到文字,请重新拍摄', 'ratio': ratio}
            return MyORJSONResponse(content=data)

    ocr_model = texts_confidence[4]
    language = texts_confidence[3]
    wrong_percentage = texts_confidence[5]
    rotate = texts_confidence[6]
    if ocr_model == "huawei":
        print("huawei :")
        img = img.rotate(rotate, expand=True)
        b64 = convert_image_to_b64(img)
        texts = huawei_ocr(b64)
        texts = split_texts(texts)
    elif ocr_model == "dataelem":
        print("dataelem: ")
        img = img.rotate(rotate, expand=True)
        # dataelem_ocr
        b64 = convert_image_to_b64(img)
        # dataelem_language = ((language == "en") and "english_print" or "chinese_print")
        texts = dataelem_ocr(b64, language)
        if language == "chinese_print":
            texts = split_texts(texts)
    else:
        # paddleocr
        img = Image.fromarray(cv2.cvtColor(np.uint8(img), cv2.COLOR_RGB2BGR))
        # language = ( (language == "en") and "english_print" or "chinese_print")
        texts = baidu_ocr(img, language)[0]

    img.save("images/ford/rotate/%s_%s_%s_%s_rotate.jpg" % (time.strftime("%Y-%m-%d-%H-%M-%S", t), id, compress_size, label_extract),
             format="JPEG", quality=100)

    # texts = text_ocr_v4(img, texts_confidence[3])
    # for idx in range(len(texts)):
    #     res = texts[idx]
    #     print(idx)
    #     for line in res:
    #         print(line[1][1])
    if len(texts) == 0:
        data = {'code': 2, 'msg': '图片不合规,提取不到文字,请重新拍摄'}
        return MyORJSONResponse(content=data)

    print(list(map(lambda x: x[1][0], texts)))
    print(texts)

    percentage, filter_texts = texts_pair_algorithm(texts, texts_confidence[0])


    if percentage > wrong_percentage:

        # 去掉置信度小于0.8的文本
        i = 0
        while i < len(filter_texts):
            if filter_texts[i][1][1] < texts_confidence[1]:
                filter_texts.pop(i)
                i -= 1
            else:
                i += 1
        img_drawed = draw_box_on_image(img, filter_texts)
        img_drawed.save("images/ford/rotate/%s_%s_%s_%s_fail_rotate.jpg" % (time.strftime("%Y-%m-%d-%H-%M-%S",t), id, compress_size, label_extract))

        img_drawed_b64 = convert_image_to_b64(img_drawed)
        data = {'code': 1, 'msg': '失败', 'data': {'img_detected': 'data:image/jpeg;base64,' + img_drawed_b64,
                                                   'speed_time': round(time.time() - start_time, 2)}}
        # list(map(lambda x: x, texts))
    else:
        if percentage > 0:
            img_drawed = draw_text_on_image(img, filter_texts)
            img_drawed.save("images/ford/rotate/%s_%s_%s_%s_success_rotate.jpg" % (uid, id, compress_size, label_extract))

        data = {'code': 0, 'msg': '成功', 'data': {'percentage': percentage,'speed_time': round(time.time() - start_time, 2)}}


    return MyORJSONResponse(content=data)


