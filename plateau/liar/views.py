import random
import string
import operator
import telegram

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import Category, Words, User, Game, Gamer, Honor


class MainView(generic.ListView):
    template_name = "liar/main.html"

    def get(self, request):
        user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')

        user_list = list(user_only_guest) + list(user_exclude_guest)

        context = {
            'user_list': user_list,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        username = request.POST.get('username')
        gamecode = request.POST.get('gamecode')

        # 사용자 명이 없는 경우, 에러로 메인화면으로 전송
        if len(username) == 0:
            return HttpResponseRedirect(reverse('liar:main', ))

        # 사용자 명으로 신규 생성하거나, 기존 사용자 조회
        user, created = User.objects.get_or_create(username=username)

        # 신규 게임 등록시 게임코드 채번 후, 게임 생성
        if action == "newgame":
            # 숫자 + 대소문자
            gamecode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

            game, created = Game.objects.get_or_create(gamecode=gamecode, master=user)
            if not created:
                # 게임코드가 중복채번 된 경우, 재시도 유도
                context = {
                    'username': username,
                    'message': '게임 생성에 실패하였습니다.',
                }
                return render(request, self.template_name, context)

        # 기존 게임 입장 시, 기 생성 게임 조회
        elif action == "ingame":
            if len(gamecode) == 0:
                return HttpResponseRedirect(reverse('liar:main', ))

            game = Game.objects.filter(gamecode=gamecode).first()

        if game:
            total_gamer = Gamer.objects.filter(game=game)

            # 게임대기 상태인 경우만, 추가 플레이어 입장
            if game.ingameCd == 0:
                # 사용자가 해당 게임에 플레이어가 아닌 경우, 신규(무직)으로 등록
                if not total_gamer.filter(user=user):
                    gamer, created = Gamer.objects.get_or_create(game=game, user=user, job="무직")
            else:
                if total_gamer.filter(user=user):
                    return HttpResponseRedirect(reverse('liar:game', args=(gamecode, user.username,)))
                else:
                    user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
                    user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by(
                        'username')

                    user_list = list(user_only_guest) + list(user_exclude_guest)

                    context = {
                        'user_list': user_list,
                        'username': username,
                        'message': '해당 게임에 참가할 수 없습니다.',
                    }

                    return render(request, self.template_name, context)
        else:
            user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
            user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by(
                'username')

            user_list = list(user_only_guest) + list(user_exclude_guest)

            # 게임이 존재하지 않는 경우, 에러로 메인화면으로 전송
            context = {
                'user_list': user_list,
                'username': username,
                'message': '존재하지 않는 게임입니다.',
            }
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('liar:game', args=(gamecode, user.username,)))


class GameView(generic.ListView):
    template_name = "liar/ingame.html"

    def get(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()

        wait_gamers = Gamer.objects.filter(game=game, status=0)
        ready_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
        view_gamers = Gamer.objects.filter(game=game, status=2)

        categories = Category.objects.all().order_by('categoryname')

        words = []
        if game.categoryname:
            category = Category.objects.filter(categoryname=game.categoryname).first()
            words = Words.objects.filter(category=category).order_by('word')

        total_players = Gamer.objects.filter(game=game, status=1)
        player_category = {}
        for _player in total_players:
            if _player.categoryname:
                if _player.categoryname in player_category:
                    player_category[_player.categoryname] = player_category[_player.categoryname] + 1
                else:
                    player_category[_player.categoryname] = 1

        liar = total_players.filter(job='liar').first()

        context = {
            'gamecode': gamecode,
            'username': username,
            'gamer': gamer,
            'wait_gamers': wait_gamers,
            'ready_gamers': ready_gamers,
            'view_gamers': view_gamers,
            'categories': categories,
            'words': words,
            'liar': liar,
            'player_categories': sorted(player_category.items(), key=operator.itemgetter(1), reverse=True),
        }

        return render(request, self.template_name, context)

    def post(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()

        action = request.POST.get('action')

        if action == "readygame":
            gamer.status = 1
            gamer.save()

        elif action == "viewgame":
            gamer.status = 2
            gamer.save()

        elif action == "trickster":
            game.tricksterYn = not game.tricksterYn
            game.save()

        elif action == "whistleblower":
            game.whistleblowerYn = not game.whistleblowerYn
            game.save()

        elif action == "startgame":
            # 플레이어 정보 초기화
            total_gamers = Gamer.objects.filter(game=game)

            # 게임 라운드가 0이 아닌 경우, 이력정보 적재

            # 플레이어 정보 초기화
            for _gamer in total_gamers:
                _gamer.job = "무직"
                _gamer.position = 0
                _gamer.categoryname = ''
                _gamer.speech1 = ''
                _gamer.speech2 = ''
                _gamer.vote = 0
                _gamer.targetusername = ''
                _gamer.save()

            # 게임 라운드 증가 및 게임상태코드 단어선택 상태로 변경
            game.round += 1
            game.ingameCd = 1
            game.categoryname = ''
            game.word = ''
            game.turnusername = ''
            game.vote = 0
            game.targetusername = ''
            game.winner = ''
            game.liarlock = 0
            game.liarkey = ''
            game.save()

        elif action == "gamecategory":
            # 플레이어 선택 카테고리 저장
            gamer.categoryname = request.POST.get('categoryname')
            gamer.save()

            no_category_players = Gamer.objects.filter(game=game, status=1, categoryname='')
            # 모든 참가 플레이어가 카테고리를 선택한 경우
            if not no_category_players:
                total_players = Gamer.objects.filter(game=game, status=1)
                position = [o + 1 for o in range(len(total_players))]
                random.shuffle(position)
                player_category = {}

                liar = ['citizen' for _ in range(len(total_players) - 1)]
                liar.append('liar')
                if game.tricksterYn:
                    liar.pop(0)
                    liar.append('trickster')
                if game.whistleblowerYn:
                    liar.pop(0)
                    liar.append('whistleblower')
                random.shuffle(liar)

                for _player in total_players:
                    # 각 직업과 랜덤하게 지정된 순번을 저장.
                    _player.position = position.pop()
                    _player.job = liar.pop()
                    _player.save()

                    # 1번째 플레이어 저장
                    if _player.position == 1:
                        turnusername = _player.user.username

                    # 카테고리 우선순위를 위해 딕셔너리 생성 및 카운트
                    if _player.categoryname:
                        if _player.categoryname in player_category:
                            player_category[_player.categoryname] = player_category[_player.categoryname] + 1
                        else:
                            player_category[_player.categoryname] = 1

                # 게임상태코드 설명등록으로 변경 및 제시어 선정
                game.categoryname = sorted(player_category.items(), key=operator.itemgetter(1), reverse=True)[0][0]
                game.ingameCd = 2

                # 카테고리 기준으로 단어 생성
                category = Category.objects.filter(categoryname=game.categoryname).first()
                words = Words.objects.filter(category=category).all()

                game.word = words[random.randrange(0, len(words))].word
                game.turnusername = turnusername
                game.save()

        elif action == "speech":
            # 입력한 발언 내용을 각 플레이어별 발언으로 등록
            if not gamer.speech1:
                gamer.speech1 = request.POST.get('speech')
            elif not gamer.speech2:
                gamer.speech2 = request.POST.get('speech')
            gamer.save()

            # 다음 플레이어 저장을 위한 순번 확인
            ready_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')

            # 플레이어의 두번째 발언이 등록되었고, 현재 순번이 플레이어 숫자와 동일한 경우(마지막 플레이어의 두번째 발언인 경우)
            if gamer.speech2 and gamer.position == len(ready_gamers):
                # 해당 게임의 단계를 발언종료 후, 투표 단계로 변경(검거대상이 라이어만 있는 경우)
                if not game.tricksterYn:
                    for _gamer in ready_gamers:
                        _gamer.vote = 1
                        _gamer.save()

                    game.vote = 1
                game.ingameCd = 3
                game.save()
            else:
                game.turnusername = ready_gamers[gamer.position % len(ready_gamers)].user.username
                game.save()

        elif action == "votegame":
            if not game.tricksterYn:
                ready_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
                for _gamer in ready_gamers:
                    _gamer.vote = 1
                    _gamer.save()

                game.vote = 1
            game.ingameCd = 3
            game.save()

        elif action == "vote":
            vote = request.POST.get('vote')
            if vote == "liar":
                gamer.vote = 1
            else:
                gamer.vote = 2
            gamer.save()

            no_vote_players = Gamer.objects.filter(game=game, status=1, vote=0)
            # 모든 참가 플레이어가 검거 대상을 투표한 경우
            if not no_vote_players:
                total_players = Gamer.objects.filter(game=game, status=1)
                vote_liar = total_players.filter(vote=1)
                if len(vote_liar) >= len(total_players) - len(vote_liar):
                    game.vote = 1
                else:
                    game.vote = 2
                game.save()

        elif action == "target":
            gamer.targetusername = request.POST.get('targetusername')
            gamer.save()

            # 전체 플레이어가 타겟을 지정하면 게임 타겟으로 지정
            no_target_players = Gamer.objects.filter(game=game, status=1, targetusername='')

            # 타겟을 모두 고른 경우에만 표기
            if not no_target_players:
                target_category = {}
                total_players = Gamer.objects.filter(game=game, status=1)

                for _player in total_players:

                    # 카테고리 우선순위를 위해 딕셔너리 생성 및 카운트
                    if _player.targetusername:
                        if _player.targetusername in target_category:
                            target_category[_player.targetusername] = target_category[_player.targetusername] + 1
                        else:
                            target_category[_player.targetusername] = 1

                sorted_target_category = sorted(target_category.items(), key=operator.itemgetter(1), reverse=True)

                # 상위 타겟이 투표점수 동점인 경우, 라이어 승
                if len(sorted_target_category) > 1 and sorted_target_category[0][1] == sorted_target_category[1][1]:
                    game.targetusername = 'TIE'
                    game.winner = 'liar'
                    game.ingameCd = 5
                    game.save()

                    # 게임 결과 저장
                    honor_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')

                    for _gamer in honor_gamers:
                        winYn = False
                        if game.winner == 'liar':
                            if _gamer.job in ['liar', 'trickster']:
                                winYn = True
                        else:
                            if _gamer.job not in ['liar', 'trickster']:
                                winYn = True
                        honor = Honor.objects.create(
                            game=_gamer.game,
                            user=_gamer.user,
                            round=_gamer.game.round,
                            categoryname=_gamer.game.categoryname,
                            word=_gamer.game.word,
                            tricksterYn=_gamer.game.tricksterYn,
                            whistleblowerYn=_gamer.game.whistleblowerYn,
                            job=_gamer.job,
                            winYn=winYn
                        )
                else:
                    game.targetusername = sorted_target_category[0][0]
                    target_user = User.objects.filter(username=game.targetusername).first()
                    target_gamer = Gamer.objects.filter(game=game, user=target_user).first()

                    if game.vote == 1:
                        if target_gamer.job == 'liar':
                            # 타겟 대상이 라이어이고, 지정된 타겟이 라이어라면 마지막 찬스 단계로 이동
                            game.ingameCd = 4
                            game.save()
                        else:
                            # 타겟 대상이 라이어이고, 지정된 타겟이 라이어가 아니라면 라이어 승
                            game.winner = 'liar'
                            game.ingameCd = 5
                            game.save()

                            # 게임 결과 저장
                            honor_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')

                            for _gamer in honor_gamers:
                                winYn = False
                                if game.winner == 'liar':
                                    if _gamer.job in ['liar', 'trickster']:
                                        winYn = True
                                else:
                                    if _gamer.job not in ['liar', 'trickster']:
                                        winYn = True
                                honor = Honor.objects.create(
                                    game=_gamer.game,
                                    user=_gamer.user,
                                    round=_gamer.game.round,
                                    categoryname=_gamer.game.categoryname,
                                    word=_gamer.game.word,
                                    tricksterYn=_gamer.game.tricksterYn,
                                    whistleblowerYn=_gamer.game.whistleblowerYn,
                                    job=_gamer.job,
                                    winYn=winYn
                                )
                    else:
                        if target_gamer.job == 'trickster':
                            # 타겟 대상이 사기꾼이고, 지정된 사기꾼이라면 시민 승
                            game.winner = 'citizen'
                            game.ingameCd = 5
                            game.save()
                        else:
                            # 타겟 대상이 사기꾼이고, 지정된 타겟이 라이어가 아니라면 라이어 승
                            game.winner = 'liar'
                            game.ingameCd = 5
                            game.save()

                        # 게임 결과 저장
                        honor_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')

                        for _gamer in honor_gamers:
                            winYn = False
                            if game.winner == 'liar':
                                if _gamer.job in ['liar', 'trickster']:
                                    winYn = True
                            else:
                                if _gamer.job not in ['liar', 'trickster']:
                                    winYn = True
                            honor = Honor.objects.create(
                                game=_gamer.game,
                                user=_gamer.user,
                                round=_gamer.game.round,
                                categoryname=_gamer.game.categoryname,
                                word=_gamer.game.word,
                                tricksterYn=_gamer.game.tricksterYn,
                                whistleblowerYn=_gamer.game.whistleblowerYn,
                                job=_gamer.job,
                                winYn=winYn
                            )

        elif action == "liargame":
            game.ingameCd = 4
            game.save()

        elif action == "lock":
            lock = request.POST.get('lock')
            if lock == "word":
                game.liarlock = 1
            elif lock == "whistleblower":
                game.liarlock = 2
            game.save()

        elif action == "runaway":
            lock = request.POST.get('lock')
            key = request.POST.get('key')
            game.liarkey = key

            if lock == "word":
                game.liarlock = 1
                if key == game.word:
                    game.winner = 'liar'
            elif lock == "whistleblower":
                game.liarlock = 2
                runaway_user = User.objects.filter(username=key).first()
                runaway_gamer = Gamer.objects.filter(game=game, user=runaway_user).first()
                if runaway_gamer.job == "whistleblower":
                    game.winner = 'liar'

            if not game.winner:
                game.winner = 'citizen'

            game.ingameCd = 5
            game.save()

            # 게임 결과 저장
            honor_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')

            for _gamer in honor_gamers:
                winYn = False
                if game.winner == 'liar':
                    if _gamer.job in ['liar', 'trickster']:
                        winYn = True
                else:
                    if _gamer.job not in ['liar', 'trickster']:
                        winYn = True
                honor = Honor.objects.create(
                    game=_gamer.game,
                    user=_gamer.user,
                    round=_gamer.game.round,
                    categoryname=_gamer.game.categoryname,
                    word=_gamer.game.word,
                    tricksterYn=_gamer.game.tricksterYn,
                    whistleblowerYn=_gamer.game.whistleblowerYn,
                    job=_gamer.job,
                    winYn=winYn
                )

        elif action == "resultgame":
            game.ingameCd = 5
            game.save()

            # 강제로 게임을 종료한 경우(마스터 플레이어가 버튼으로 종료한 경우, 별도 전적을 저장하지 않음)

        elif action == "endgame":
            game.ingameCd = 0
            game.save()

        return HttpResponseRedirect(reverse('liar:game', args=(gamecode, username,)))


class OfflineView(generic.ListView):
    template_name = "liar/offline.html"

    def get(self, request):
        categories = Category.objects.all().order_by('categoryname')

        context = {
            'categories': categories,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        categoryname = request.POST.get('categoryname')

        if action == "category":
            category = Category.objects.filter(categoryname=categoryname).first()

            context = {
                'category': category,
                'categoryname': categoryname,
                'number': 3,
            }
        elif action == "startgame":
            number = int(request.POST.get('player'))

            category = Category.objects.filter(categoryname=categoryname).first()

            words = Words.objects.filter(category=category).all()

            word = None

            if len(words) > 0:
                word = words[random.randrange(0, len(words))]

            liar = ['citizen' for _ in range(number - 1)]
            liar.append('liar')
            if number > 5:
                liar.pop(0)
                liar.pop(0)
                liar.append('trickster')
                liar.append('whistleblower')
            random.shuffle(liar)

            guest = [o + 1 for o in range(number)]
            random.shuffle(guest)

            context = {
                'category': category,
                'categoryname': categoryname,
                'number': number,
                'word': word,
                'liar': liar,
                'guest': guest,
                'whistle': guest[liar.index('liar')],
            }

        return render(request, self.template_name, context)


class CategoryView(generic.ListView):
    template_name = "liar/category.html"

    def get(self, request):
        categories = Category.objects.all().order_by('categoryname')

        context = {
            'categories': categories,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        categoryname = request.POST.get('categoryname')

        if len(categoryname) != 0:
            category, created = Category.objects.get_or_create(
                categoryname=categoryname
            )

        return HttpResponseRedirect(reverse('liar:category', ))


class WordView(generic.ListView):
    template_name = "liar/word.html"

    def get(self, request):
        categories = Category.objects.all().order_by('categoryname')

        context = {
            'categories': categories,
        }

        return render(request, self.template_name, context)


class WordDetailView(generic.ListView):
    template_name = "liar/word.html"

    def get(self, request, categoryname):
        category = Category.objects.filter(categoryname=categoryname).first()

        words = Words.objects.filter(category=category).all().order_by('word')

        context = {
            'category': category,
            'words': words,
        }

        return render(request, self.template_name, context)

    def post(self, request, categoryname):

        category = Category.objects.filter(categoryname=categoryname).first()

        word = request.POST.get('word')
        action = request.POST.get('action')

        if len(word) != 0:
            if action == 'add':
                _word, created = Words.objects.get_or_create(
                    category=category,
                    word=word
                )
            elif action == 'del':
                deleteWord = Words.objects.filter(category=category, word=word).first()
                deleteWord.delete()

        words = Words.objects.filter(category=category).all().order_by('word')

        context = {
            'category': category,
            'words': words,
        }

        return render(request, self.template_name, context)


class LoginView(generic.ListView):
    template_name = "liar/main.html"

    def get(self, request, gamecode):
        user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')

        user_list = list(user_only_guest) + list(user_exclude_guest)

        context = {
            'user_list': user_list,
            'gamecode': gamecode,
        }

        return render(request, self.template_name, context)


class TelegramView(generic.DetailView):

    # 텔레그램 전송
    def get(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()

        bot = telegram.Bot(token='1480423142:AAHkkAlgShepdoXFW2HP8TzZAiRfCN8WpHI')
        bot.sendMessage(chat_id='-413309173',
                        text='[라이어코드:' + game.gamecode + '](https://35.230.124.241:8443/liar/login/' + game.gamecode + '/)',
                        parse_mode='Markdown', disable_web_page_preview=True)

        return HttpResponseRedirect(reverse('liar:game', args=(gamecode, username,)))
