import os
import sys
import urllib.request

def PreprocessSourceText(original_Text):
    '''
    source Text를 전처리함
        1. 문단 별로 Text를 구분하여 저장
        2. 4000자가 넘는 문단 처리
    :param original_Text: 사용자가 입력한 원본 텍스트(string)
    :return: 문단 별로 전처리된 텍스트 리스트(string list)

    rough idea?
        1. 문단 별로 나눠서 list에 저장한 후 반환한다.
        문단을 나누는 기준: \n
        문제? 한 문단에 4000자가 넘으면 에러 발생(Papago NMT)
        4000자가 넘으면 안되지만 4000자가 넘는다고 중간에 문장이 끊기는 것도 안됨 ... > 번역 품질 나빠질 것
        3000자를 넘기면 flag를 1로, 이후 문장이 종결된다면 ('.' , '?', '!', '\"', '\'', ...) 문단을 임의로 나눈다..
        근데 경우의 수가 너무 많지 않나....
        2. 그냥 이것을 고려하지 않고 그냥 문단 단위로만 나눠서 반환..
    '''
    paragraph = ""; preprocessed_Text = []
    for s in original_Text:
        if s == '\n':
            preprocessed_Text.append(paragraph)
            paragraph = ""
        else:
            paragraph += s
    '''
        수정이 필요한 부분
        max_len = 3000  #한 문단의 최대 길이
        paragraph = ""; cnt = 0; preprocessed_Text = []; flag = 0
        end_of_sentence = ['.','\"', '!', '?', '\'',')']
        for s in original_Text:
            if cnt >= max_len:
                flag = 1

            if s == '\n':
                preprocessed_Text.append(paragraph)
                paragraph = ""
                cnt = 0
                flag = 0
                continue
    '''
    return preprocessed_Text

    
def requestPapagoNMT(datas):
    '''
    Request Papago NMT > response와 rescode가 담긴 list 반환
    :param datas:
    :return: responses, rescodes
    '''
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
    '''
    :param rescodes: 
    :param responses: 
    :return: PapagoNMT로 번역된 텍스트를 문단 별로 리스트에 담아 반환, 오류시 오류코드 반환
    '''
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