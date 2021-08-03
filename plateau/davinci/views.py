import random
import string
import telegram

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import User, Game, Gamer, Card, Cards, Honor


class MainView(generic.ListView):
    template_name = "davinci/main.html"

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
            return HttpResponseRedirect(reverse('davinci:main', ))

        # 사용자 명으로 신규 생성하거나, 기존 사용자 조회
        user, created = User.objects.get_or_create(username=username)

        # 신규 게임 등록시 게임코드 채번 후, 게임 생성
        if action == "newgame":
            # 숫자 + 대소문자
            gamecode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

            game, created = Game.objects.get_or_create(gamecode=gamecode, turnUser=user, mastername=user.username)
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
                return HttpResponseRedirect(reverse('davinci:main', ))

            game = Game.objects.filter(gamecode=gamecode).first()

        if game:
            total_gamer = Gamer.objects.filter(game=game)

            # 게임대기 상태인 경우만, 추가 플레이어 입장
            if game.ingameCd == 0:
                # 사용자가 해당 게임에 플레이어가 아닌 경우, 신규(무직)으로 등록
                if not total_gamer.filter(user=user):
                    gamer, created = Gamer.objects.get_or_create(game=game, user=user)
            else:
                if total_gamer.filter(user=user):
                    return HttpResponseRedirect(reverse('davinci:game', args=(gamecode, user.username,)))
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

        return HttpResponseRedirect(reverse('davinci:game', args=(gamecode, user.username,)))


class GameView(generic.ListView):
    template_name = "davinci/ingame.html"

    def get(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()
        turnGamer = Gamer.objects.filter(game=game, user=game.turnUser).first()

        wait_gamers = Gamer.objects.filter(game=game, status=0)
        ready_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
        view_gamers = Gamer.objects.filter(game=game, status=2)

        all_cards = Cards.objects.all()
        players_cards = Card.objects.filter(game=game).order_by('user', 'order')

        already_cards = list(players_cards.values_list('card', flat=True))
        ready_cards = []
        for card in all_cards:
            if card.id not in already_cards:
                ready_cards.append(card)
        random.shuffle(ready_cards)

        context = {
            'gamecode': gamecode,
            'username': username,
            'gamer': gamer,
            'wait_gamers': wait_gamers,
            'ready_gamers': ready_gamers,
            'view_gamers': view_gamers,
            'ready_cards': ready_cards,
            'players_cards': players_cards,
            'lastCard': turnGamer.lastCard,
        }

        return render(request, self.template_name, context)

    def post(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()

        action = request.POST.get('action')
        card = request.POST.get('card')

        if action == "readygame":
            gamer.status = 1
            gamer.save()

        elif action == "viewgame":
            gamer.status = 2
            gamer.save()

        elif action == "startgame":

            # 이번 라운드 참가 플레이어 순번 지정
            round_gamers = Gamer.objects.filter(game=game, status=1)
            position = [o + 1 for o in range(len(round_gamers))]
            random.shuffle(position)

            for _player in round_gamers:
                # 랜덤하게 지정된 순번을 저장.
                _player.position = position.pop()
                _player.lastCard = None
                _player.result = 0
                _player.save()

                # 1번째 플레이어 저장
                if _player.position == 1:
                    turnuser = _player.user

            # 플레이어 수에 따른 초기 카드 수 설정(4명은 3장, 그외 4장)
            card_cnt = 4
            if round_gamers.count() == 4:
                card_cnt = 3

            # 플레이어 카드 정보를 랜덤하게 저장(조커 카드는 초기 배분 제외)
            cards_not_joker = Cards.objects.exclude(number=13)
            cards = [o for o in cards_not_joker]
            random.shuffle(cards)

            for i in range(1, card_cnt + 1):
                for _player in round_gamers:
                    player_card = cards.pop()
                    card, created = Card.objects.get_or_create(game=_player.game, user=_player.user, card=player_card,
                                                               order=((player_card.number * 2 + (
                                                                           player_card.type - 1)) * 2))

            # 플레이어별 할당된 카드 순번 정리
            for _player in round_gamers:
                player_cards = Card.objects.filter(game=_player.game, user=_player.user).order_by('order')
                for idx, player_card in enumerate(player_cards):
                    player_card.order = (idx + 1) * 2
                    player_card.save()

            # 게임 라운드 증가 및 게임상태코드 게임중, 1번째 유저 턴으로 변경
            game.round += 1
            game.ingameCd = 1
            game.turnUser = turnuser
            game.save()

        elif action == "pickcard":
            type, number, order = card.split(',')
            print(type, ' ', number, ' ', order)

            player_cards = Card.objects.filter(game=game, user=user).order_by('order')
            card = Cards.objects.filter(number=number, type=type).first()

            injected = False

            for player_card in player_cards:
                if injected:
                    player_card.order += 2
                    player_card.save()
                else:
                    if int(order) < player_card.order:
                        _card, created = Card.objects.get_or_create(game=game, user=user, card=card,
                                                                    order=player_card.order)
                        player_card.order += 2
                        player_card.save()

                        gamer.lastCard = card
                        gamer.save()

                        injected = True

            if not injected:
                _card, created = Card.objects.get_or_create(game=game, user=user, card=card,
                                                            order=(len(player_cards) + 1) * 2)

                gamer.lastCard = card
                gamer.save()

        elif action == "checkcard":
            tgamecode, tusername, checknumber, type, number = card.split(',')

            if checknumber == number:
                tuser = User.objects.filter(username=tusername).first()
                tcards = Cards.objects.filter(number=number, type=type).first()
                tcard = Card.objects.filter(game=game, user=tuser, card=tcards).first()
                tcard.check = 1
                tcard.save()

                tgamer = Gamer.objects.filter(game=game, user=tuser).first()
                unresult_gamers = Gamer.objects.filter(game=game, result=0)
                unchecked_cards = Card.objects.filter(game=game, user=tuser, check=0)
                if len(unchecked_cards) == 0:
                    tgamer.result = len(unresult_gamers)
                    tgamer.save()

                    if len(unresult_gamers) == 2:
                        gamer.result = 1
                        gamer.save()

                        gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
                        for gamer in gamers:
                            _honor, created = Honor.objects.get_or_create(game=game, user=user, round=game.round,
                                                                          result=gamer.result,
                                                                          winYn=True if gamer.result == 1 else False)
                        game.ingameCd = 2
                        game.save()

            else:
                tcard = Card.objects.filter(game=game, user=user, card=gamer.lastCard).first()

                if not tcard:
                    tcards_unchecked = Card.objects.filter(game=game, user=user, check=0)
                    tcards = [o for o in tcards_unchecked]
                    random.shuffle(tcards)
                    tcard = tcards.pop()

                tcard.check = 1
                tcard.save()

                gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
                unresult_gamers = Gamer.objects.filter(game=game, result=0)
                unchecked_cards = Card.objects.filter(game=game, user=user, check=0)

                if len(unchecked_cards) == 0 and len(unresult_gamers) == 2:
                    gamer.result = len(unresult_gamers)
                    gamer.save()

                    for _gamer in gamers:
                        if _gamer.result == 0:
                            _gamer.result = 1
                            _gamer.save()

                        _honor, created = Honor.objects.get_or_create(game=game, user=_gamer.user, round=game.round,
                                                                      result=_gamer.result,
                                                                      winYn=True if _gamer.result == 1 else False)
                    game.ingameCd = 2
                    game.save()
                else:
                    ingamers = gamers.exclude(result__gt=0)

                    idx = 0
                    while True:
                        if gamer == ingamers[idx]:
                            break
                        idx += 1
                    idx += 1

                    if idx == len(ingamers):
                        idx = 0

                    game.turnUser = ingamers[idx].user
                    game.save()

                    if len(unchecked_cards) == 0:
                        gamer.result = len(unresult_gamers)

                    gamer.lastCard = None
                    gamer.save()

        elif action == "endturn":

            gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
            ingamers = gamers.exclude(result__gt=0)

            idx = 0
            while True:
                if gamer == ingamers[idx]:
                    break
                idx += 1
            idx += 1

            if idx == len(ingamers):
                idx = 0

            game.turnUser = ingamers[idx].user
            game.save()

            gamer.lastCard = None
            gamer.save()

        elif action == "resultgame":
            game.ingameCd = 2
            game.save()

            # 강제로 게임을 종료한 경우(마스터 플레이어가 버튼으로 종료한 경우, 별도 전적을 저장하지 않음)

        elif action == "endgame":
            # 플레이어 정보 초기화
            total_gamers = Gamer.objects.filter(game=game)

            for _gamer in total_gamers:
                _gamer.position = 0
                _gamer.lastCard = None
                _gamer.result = 0
                _gamer.save()

            # 해당 게임 카드 정보 초기화
            cards = Card.objects.filter(game=game)
            cards.delete()

            game.ingameCd = 0
            game.save()

        return HttpResponseRedirect(reverse('davinci:game', args=(gamecode, username,)))


class RuleView(generic.DetailView):
    template_name = "davinci/rule.html"

    # 룰북 화면으로 전환
    def get(self, request):
        user = User.objects.filter(username='손님').first()

        context = {
            'user': user,
        }

        return render(request, self.template_name, context)


class LoginView(generic.ListView):
    template_name = "davinci/main.html"

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
                        text='[다빈치코드:' + game.gamecode + '](http://3.35.239.74:8000/davinci/login/' + game.gamecode + '/)',
                        parse_mode='Markdown', disable_web_page_preview=True)

        return HttpResponseRedirect(reverse('davinci:game', args=(gamecode, username,)))
