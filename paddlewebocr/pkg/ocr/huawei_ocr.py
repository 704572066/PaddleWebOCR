from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkocr.v1 import *
ak = "UCUXQ4AIVBNG9LJRYICE"
sk = "Ny08BD9o94JcWDuK8eRgpXPh0SxiVVOHX4MN9FBn"
def huawei_ocr(b64):
    credentials = BasicCredentials(ak, sk)
    client = OcrClient.new_builder().with_credentials(credentials).with_region(OcrRegion.value_of("cn-north-4")).build()
    texts = []
    try:
        request = RecognizeGeneralTextRequest()
        request.body = GeneralTextRequestBody(
            language="zh",
            character_mode=False,
            quick_mode=False,
            detect_direction=False,
            image=b64
        )
        response = client.recognize_general_text(request)
        words_block_list = response.result.words_block_list
        i = 0
        while i < len(words_block_list):
            texts.append([words_block_list[i].location, (words_block_list[i].words, words_block_list[i].confidence)])
            i += 1
        return texts

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

