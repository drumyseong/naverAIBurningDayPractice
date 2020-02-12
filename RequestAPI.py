import os
import sys
import urllib.request

def requestNaverAPI(datas,url):
    '''
    Request Naver API > response와 rescode가 담긴 list 반환
    :param datas:
    :return: responses, rescodes
    '''
    client_id = "아이디"
    client_secret = "비밀번호"
    url = url

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    responses = []; rescodes = []

    for i, data in enumerate(datas):
        responses.append(urllib.request.urlopen(request, data=data.encode("utf-8")))
        rescodes.append(responses[i].getcode())

    return responses, rescodes
