#import os
#import sys
import urllib.request

def PreprocessSourceText(original_Text):
    '''
    source Text를 전처리함
        1. 문단 별로 Text를 구분하여 저장
        2. 4000자가 넘는 문단 처리
    :param original_Text: 사용자가 입력한 원본 텍스트(string)
    :return: 문단 별로 전처리된 텍스트 리스트(string list)
    '''

def requestPapagoNMT(datas):
    #request Papago NMT
    client_id = "아이디"
    client_secret = "비밀번호"
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation" #API URL(N2MT)

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    responses = []; rescodes = []
    for i, data in enumerate(datas):
        responses.append(urllib.request.urlopen(request, data=data.encode("utf-8")))
        rescodes.append(responses[i].getcode())
    return responses, rescodes

def getResponse(rescodes, responses):
    responses_bodys = []
    for rescode, response in zip(rescodes, responses):
        if rescode == 200:  #API 정상 호출 > 번역 텍스트 decode 후 저장
            response_body = response.read()
            responses_bodys.append(response_body.decode('uff-8'))
        else:   # Error 발생 > error 코드 저장
            responses_bodys.append(rescode)
    return responses_bodys

def TranslateSourceText(original_Text, source_lang, target_lang):
    '''
    Naver API인 Papago NMT를 이용해 Original Text를 번역한 후 return
    :param original_Text: 사용자가 입력한 원본 텍스트(string)
    :param source_lang: 원본 텍스트의 언어 코드(string)
    :param target_lang: 타겟(번역될) 언어 코드(string)
    :return: 문단 별로 번역된 텍스트(or 오류코드) 리스트(string list)
    '''
    #orginal_Text preprocess
    preprocessedText = PreprocessSourceText(original_Text)  # preprocessed paragraphs

    datas = []
    for pt in preprocessedText:
        datas.append("source=" + source_lang + "&target=" + target_lang + "&text=" + pt)

    #request Papago NMT
    responses, rescodes = requestPapagoNMT(datas)

    #get response
    responses_bodys = getResponse(responses,rescodes)

    return responses_bodys
