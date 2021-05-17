import random
import string
import operator
import telegram

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import Category, Words, User, Game, Gamer


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
                _gamer.vote = 0
                _gamer.save()

            # 게임 라운드 증가 및 게임상태코드 단어선택 상태로 변경
            game.round += 1
            game.ingameCd = 1
            game.categoryname = ''
            game.word = ''
            game.turnusername = ''
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

        elif action == "votegame":
            game.ingameCd = 3
            game.save()

        elif action == "resultgame":
            game.ingameCd = 4
            game.save()

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
                        text='[게임코드:' + game.gamecode + '](http://3.35.239.74:8000/liar/telegram/login/' + game.gamecode + '/)',
                        parse_mode='Markdown', disable_web_page_preview=True)

        return HttpResponseRedirect(reverse('liar:game', args=(gamecode, username,)))
