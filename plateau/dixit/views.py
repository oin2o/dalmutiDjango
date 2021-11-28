import random
import string
import telegram

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import User, Game, Gamer, Card, Cards, Honor


class MainView(generic.ListView):
    template_name = "dixit/main.html"

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
            return HttpResponseRedirect(reverse('dixit:main', ))

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
                return HttpResponseRedirect(reverse('dixit:main', ))

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
                    return HttpResponseRedirect(reverse('dixit:game', args=(gamecode, user.username,)))
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

        return HttpResponseRedirect(reverse('dixit:game', args=(gamecode, user.username,)))


class GameView(generic.ListView):
    template_name = "dixit/ingame.html"

    def get(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()

        wait_gamers = Gamer.objects.filter(game=game, status=0)
        ready_gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
        view_gamers = Gamer.objects.filter(game=game, status=2)

        vote_gamers = Gamer.objects.filter(game=game, status=1, storyCard__isnull=False).exclude(
            pickusername='').order_by('position')

        story_card_ordered = Gamer.objects.filter(game=game, status=1, storyCard__isnull=False).order_by('position')
        player_cards = Card.objects.filter(game=game, user=user, check=0).order_by('order')

        story_cards = [o for o in story_card_ordered]
        random.shuffle(story_cards)

        context = {
            'gamecode': gamecode,
            'username': username,
            'gamer': gamer,
            'wait_gamers': wait_gamers,
            'ready_gamers': ready_gamers,
            'view_gamers': view_gamers,
            'vote_gamers': vote_gamers,
            'story_cards': story_cards,
            'player_cards': player_cards,
        }

        return render(request, self.template_name, context)

    def post(self, request, gamecode, username):
        game = Game.objects.filter(gamecode=gamecode).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()

        action = request.POST.get('action')
        keyword = request.POST.get('keyword')
        card = request.POST.get('card')
        pickusername = request.POST.get('pickusername')

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
                _player.storyCard = None
                _player.pickusername = ''
                _player.point = 0
                _player.addpoint = 0
                _player.save()

                # 1번째 플레이어 저장
                if _player.position == 1:
                    turnuser = _player.user

            # 플레이어 수에 따른 초기 카드 수 설정(초기카드 6장)
            card_cnt = 6

            # 플레이어 카드 정보를 랜덤하게 저장
            card_all = Cards.objects.all()
            cards = [o for o in card_all]
            random.shuffle(cards)

            for i in range(1, card_cnt + 1):
                for _player in round_gamers:
                    player_card = cards.pop()
                    card, created = Card.objects.get_or_create(game=_player.game, user=_player.user, card=player_card,
                                                               order=i)

            # 게임 라운드 증가 및 게임상태코드 게임중, 1번째 유저 턴으로 변경
            game.round += 1
            game.ingameCd = 1
            game.turnUser = turnuser
            game.save()

        elif action == "keyword":
            category, name = card.split(',')
            storyCard = Cards.objects.filter(name=name, category=category).first()

            gamer.storyCard = storyCard
            gamer.save()

            game.keyword = keyword
            game.save()

        elif action == "storycard":
            category, name = card.split(',')
            storyCard = Cards.objects.filter(name=name, category=category).first()

            gamer.storyCard = storyCard
            gamer.save()

        elif action == "votecard":
            gamer.pickusername = pickusername
            gamer.save()

            not_vote_gamers = Gamer.objects.filter(game=game, status=1, storyCard__isnull=False,
                                                   pickusername='').exclude(user=game.turnUser)

            # 모두 투표를 종료한 경우, 점수계산을 한다.
            # 모두 맞거나 틀린 경우, 술래는 0점. 술래 외에는 내 카드 선택한 사람수 만큼 1점(그리고 2점)
            # 그 외에는, 술래는 3점. 술래 외에는 내 카드 선택한 사람수 만큼 1점(술래를 맞췄으면 +3점)
            if not not_vote_gamers:
                gamers_without_turn = Gamer.objects.filter(game=game, status=1).exclude(user=game.turnUser)
                correct_vote = gamers_without_turn.filter(pickusername=gamer.game.turnUser.username)
                not_correct_vote = gamers_without_turn.exclude(pickusername=gamer.game.turnUser.username)
                # 모두 맞거나 틀린 경우
                if len(correct_vote) == 0 or len(not_correct_vote) == 0:
                    add_point = 2
                    point_gamers_not_turn = Gamer.objects.filter(game=game, status=1).exclude(user=game.turnUser)
                    for point_player in point_gamers_not_turn:
                        # 모두 틀린 경우, 각각 플레이어의 카드를 선택한 사람 계산
                        vote_point = 0
                        if len(correct_vote) == 0:
                            vote_to_players = Gamer.objects.filter(game=game, status=1,
                                                                   pickusername=point_player.user.username)
                            vote_point += len(vote_to_players)
                        point_player.point += add_point + vote_point
                        point_player.addpoint = add_point + vote_point
                        point_player.save()
                else:
                    add_point = 3
                    point_gamers = Gamer.objects.filter(game=game, status=1)
                    for point_player in point_gamers:
                        vote_point = 0
                        if point_player.user.username != gamer.game.turnUser.username:
                            vote_to_players = Gamer.objects.filter(game=game, status=1,
                                                                   pickusername=point_player.user.username)
                            vote_point += len(vote_to_players)
                        if point_player.user.username == gamer.game.turnUser.username or point_player.pickusername == gamer.game.turnUser.username:
                            point_player.point += add_point + vote_point
                            point_player.addpoint = add_point + vote_point
                        else:
                            point_player.point += vote_point
                            point_player.addpoint = vote_point
                        point_player.save()

        elif action == "endturn":

            ingamers = Gamer.objects.filter(game=game, status=1).order_by('position')

            idx = 0
            while True:
                if gamer == ingamers[idx]:
                    break
                idx += 1
            idx += 1

            if idx == len(ingamers):
                idx = 0

            game.turnUser = ingamers[idx].user
            game.keyword = ''
            game.save()

            # 플레이어 카드 정보를 랜덤하게 저장
            card_ids = []
            ingamers_cards = Card.objects.filter(game=game)
            for ingamers_card in ingamers_cards:
                card_ids.append(ingamers_card.card.id)

            card_ready = Cards.objects.exclude(id__in=card_ids)
            cards = [o for o in card_ready]
            random.shuffle(cards)

            goto_result = False

            for ingamer in ingamers:
                uncheck_card = Card.objects.filter(game=game, user=ingamer.user, card=ingamer.storyCard).first()
                uncheck_card.check = 1
                uncheck_card.save()

                player_card = cards.pop()
                card, created = Card.objects.get_or_create(game=game, user=ingamer.user, card=player_card,
                                                           order=len(card_ids) / len(ingamers) + 1)

                ingamer.storyCard = None
                ingamer.pickusername = ''
                ingamer.addpoint = 0
                ingamer.save()

                if ingamer.point >= len(ingamers) * 5:
                    goto_result = True

            # (플레이어수 * 5)점 초과 플레이어가 있는 경우, 게임 종료
            if goto_result:
                gamers = Gamer.objects.filter(game=game, status=1).order_by('position')
                for gamer in gamers:
                    _honor, created = Honor.objects.get_or_create(game=game, user=user, round=game.round,
                                                                  point=gamer.point)
                game.ingameCd = 2
                game.save()

        elif action == "resultgame":
            game.ingameCd = 2
            game.keyword = ''
            game.save()

            # 강제로 게임을 종료한 경우(마스터 플레이어가 버튼으로 종료한 경우, 별도 전적을 저장하지 않음)

        elif action == "endgame":
            # 플레이어 정보 초기화
            total_gamers = Gamer.objects.filter(game=game)

            for _gamer in total_gamers:
                _gamer.position = 0
                _gamer.storyCard = None
                _gamer.pickusername = ''
                _gamer.point = 0
                _gamer.addpoint = 0
                _gamer.save()

            # 해당 게임 카드 정보 초기화
            cards = Card.objects.filter(game=game)
            cards.delete()

            game.ingameCd = 0
            game.save()

        return HttpResponseRedirect(reverse('dixit:game', args=(gamecode, username,)))


class CardView(generic.ListView):
    template_name = "dixit/card.html"

    def get(self, request):
        cards = Cards.objects.all().order_by('category', 'name')

        context = {
            'cards': cards,
        }

        return render(request, self.template_name, context)


class InitCardView(generic.ListView):

    def get(self, request):
        cards = Cards.objects.all().order_by('category', 'name')

        image_cnt = [84, 85, 81, 84, 67, 84, 6, 6, 6, 15, 11]

        if not cards:
            for idx, images in enumerate(image_cnt):
                for idx_image in range(images):
                    card_name = 'DIXIT_' + str(idx+1) + '_' + str(idx_image + 1)
                    card, created = Cards.objects.get_or_create(name=card_name, category='dixit')

        return HttpResponseRedirect(reverse('dixit:card', args=None))


class RuleView(generic.DetailView):
    template_name = "dixit/rule.html"

    # 룰북 화면으로 전환
    def get(self, request):
        user = User.objects.filter(username='손님').first()

        context = {
            'user': user,
        }

        return render(request, self.template_name, context)


class LoginView(generic.ListView):
    template_name = "dixit/main.html"

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
                        text='[딕싯:' + game.gamecode + '](http://35.230.124.241:8080/dixit/login/' + game.gamecode + '/)',
                        parse_mode='Markdown', disable_web_page_preview=True)

        return HttpResponseRedirect(reverse('dixit:game', args=(gamecode, username,)))
