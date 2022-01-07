import requests

from time import sleep
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.views import generic

from .models import User, Location, Egg, Abandon


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
                                    elif "/register" in str(divtag):
                                        # 세션/쿠키 사용을 위한 로그인 처리
                                        s.post(''.join([base_url, '/login']), data=login_payload)

                                # 조회된 정보 중, 하나만 사용하면 되므로 마지막 데이터만 사용
                                if len(divs) > 0:
                                    egg_url = divs[-1].find_all("a", href=True)[0]['href']

                                    # 마지막 데이터의 코드를 기준으로 에그 줍기 시도
                                    s.get(''.join([base_url, egg_url]), headers=headers, cookies=s.cookies)
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


class AbandonedView(generic.ListView):
    template_name = "dragcave/base.html"

    def get(self, request):

        user = User.objects.filter(useYn=True).first()

        if user:
            # 로그인 파라미터 정보
            login_payload = {
                "username": user.username,
                "password": user.userpswd,
                "submit": "",
            }

            eggs = Abandon.objects.filter(useYn=True)

            with requests.Session() as s:
                # 세션/쿠키 사용을 위한 로그인 처리
                s.post(''.join([base_url, '/login']), data=login_payload)

                while len(eggs) > 0:
                    req_url = ''.join([base_url, '/abandoned'])

                    # 알 조회 헤더 정보
                    headers = {
                        'referer': req_url,
                        'User-Agent': user_agent,
                    }

                    r = s.get(req_url, headers=headers, cookies=s.cookies)

                    source = BeautifulSoup(r.content, "html.parser")

                    if any(egg.eggcode in str(source) for egg in eggs):
                        # a 태그 체크를 위해 a tag에 대해서만 조회(변수명칭등은 기존 div 태그 때 명칭 유지)
                        divlist = source.find_all("a")

                        # 대상 알 관련 code 파싱 준비
                        divs = []
                        for divtag in divlist:
                            if "alt=\"egg\"" in str(divtag) and any(egg.eggcode in str(divtag) for egg in eggs):
                                divs.append(divtag)
                            elif "/register" in str(divtag):
                                # 세션/쿠키 사용을 위한 로그인 처리
                                s.post(''.join([base_url, '/login']), data=login_payload)

                        # 조회된 정보 중, 하나만 사용하면 되므로 마지막 데이터만 사용
                        if len(divs) > 0:
                            egg_url = divs[-1]['href']

                            # 마지막 데이터의 코드를 기준으로 에그 줍기 시도
                            s.get(''.join([base_url, '/', egg_url]), headers=headers, cookies=s.cookies)

                            for egg in eggs:
                                if egg.eggcode in str(egg_url):
                                    egg.useYn = False
                                    egg.save()
                                eggs = Abandon.objects.filter(useYn=True)

                            print(len(eggs), eggs, "Get Egg : ", egg_url)
                    # 하나 처리한 경우, 1초 대기
                    sleep(1)

        context = {
            'user': user
        }

        return render(request, self.template_name, context)
