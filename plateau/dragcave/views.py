import requests

from time import sleep
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.views import generic

from .models import User, Location, Egg


# 기본 링크
base_url = 'https://dragcave.net'

# agent 데이터
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36'


class EggsView(generic.ListView):
    template_name = "dragcave/base.html"

    def get(self, request):

        tryCnt = 5

        user = User.objects.filter(useYn=True).first()

        if user:
            # 로그인 파라미터 정보
            login_payload = {
                "username": user.username,
                "password": user.userpswd,
                "submit": "",
            }

            locations = Location.objects.filter(useYn=True)

            if locations:

                egg = Egg.objects.filter(useYn=True).first()

                with requests.Session() as s:
                    # 세션/쿠키 사용을 위한 로그인 처리
                    s.post(''.join([base_url, '/login']), data=login_payload)

                    while tryCnt > 0:
                        #  각 개별 location 별로 에그 조회
                        for location in locations:
                            req_url = ''.join([base_url, '/locations/', location.loctnum])

                            # 알 조회 헤더 정보
                            headers = {
                                'referer': req_url,
                                'User-Agent': user_agent,
                            }

                            r = s.get(req_url, headers=headers, cookies=s.cookies)

                            source = BeautifulSoup(r.content, "html.parser")

                            # 조회된 알 중, 대상 알 설명이 있는 경우만 조회
                            if egg.eggdesc in str(source):
                                divlist = source.find_all("div")

                                # 대상 알 관련 code 파싱 준비
                                divs = []
                                for divtag in divlist:
                                    if "alt=\"Egg\"" in str(divtag) and egg.eggdesc in str(divtag):
                                        divs.append(divtag)

                                # 조회된 정보 중, 하나만 사용하면 되므로 마지막 데이터만 사용
                                if len(divs) > 0:
                                    egg_url = divs[-1].find_all("a", href=True)[0]['href']
                                    if egg_url == "/register":
                                        # 세션/쿠키 사용을 위한 로그인 처리
                                        s.post(''.join([base_url, '/login']), data=login_payload)

                                    # 마지막 데이터의 코드를 기준으로 에그 줍기 시도
                                    s.get(''.join([base_url, egg_url]),
                                          headers=headers, cookies=s.cookies)
                                    print(tryCnt, "Get Egg : ", egg_url)
                                    tryCnt -= 1
                                    if tryCnt == 0:
                                        break
                        # 하나 처리한 경우, 10초 대기
                        sleep(10)
        context = {
            'user': user
        }

        return render(request, self.template_name, context)
