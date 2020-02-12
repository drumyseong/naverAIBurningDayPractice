import os
import sys
import RequestAPI
#################################################
# request parameter : speaker / speed / text    #
# 쓸 것인가요...?                               #
################################################

#mp3 병합: https://stackoverflow.com/questions/2952309/python-library-to-split-and-join-mp3-files

def getResponses(responses, rescodes):
    '''
    :param responses:
    :param rescodes:
    :return: responses_body(mp3filepath/errorcode) list
    '''
    responses_bodys = []
    for rescode, response in zip(rescodes, responses):
        if rescode == 200:  #API 정상 호출 > TTS MP3 저장
            response_body = response.read()
            with open('이거 이름 설정 어떻게 하지..','wb') as f:
                f.write(response_body)
            #responses_body.append('mp3filepath')
        else:   # Error 발생 > error 코드 저장
            responses_bodys.append(rescode)
    return responses_bodys

def getSpeechSynthesis(textList, lang, gender):
    '''
    Clova Speech Synthesis를 이용해 텍스트를 음성으로 변환
    :param textList: speech로 변환할 text list
    :param lang: 언어코드
    :param gender: 0: 여성 1: 남성
    :return: responses
    '''
    speakers = {
        # key:lang, value:speaker
        # 0: 여성 음색 1: 남성 음색
        # 회원 정보로 성별을 갖고오거나 사용자가 음성 성별 체크하도록?
        'ko': ('mingi', 'jinho'),
        'en': ('clara','matt'),
        'zh': ('shinji','mei'),
        'es': ('carmen','jose'),
        'ja': ('shinji','shingi') #일본어는 남성 음색밖에 제공 X
    }
    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
    datas = []; flag = 0
    if gender == "man":
        flag = 1
    for t in textList:
        # TO DO: 번역된 텍스트가 error 였을 때 처리
        data = "speaker="+speakers[lang][flag]+"&speed=0&text="+t
        datas.append(data)

    #Request API
    responses, rescodes = RequestAPI.requestNaverAPI(datas, url)

    #Get Response
    responses = getResponses(responses, rescodes)

    return responses