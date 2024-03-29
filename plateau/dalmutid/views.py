import random
import string
from datetime import datetime
import telegram

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.db.models import Count, F, Subquery, OuterRef, FloatField, Sum
from django.db.models.functions import Cast

from .models import User, Game, Gamer, Card, Honor


class LoginView(generic.ListView):
    template_name = "dalmutid/login.html"

    # 현재 활성화된 사용자 리스트를 로그인 화면에 표시
    def get(self, request):

        user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')

        user_list = list(user_only_guest) + list(user_exclude_guest)

        context = {
            'user_list': user_list,
        }

        return render(request, self.template_name, context)


class MainView(generic.ListView):
    template_name = "dalmutid/main.html"

    # 로그인 화면에서 현재 활성화된 게임들을 보여줌
    def get(self, request, username):
        game_list = Game.objects.filter(round__lt=13).order_by('-gamename')
        user = User.objects.filter(username=username).first()

        for game in game_list:
            gamer = Gamer.objects.filter(game=game, user=user)
            if not gamer:
                notingamename = game.gamename
                game_list = game_list.exclude(gamename=notingamename)

        context = {
            'user': user,
            'game_list': game_list,
        }

        return render(request, self.template_name, context)

    # 입력된 사용자 명으로 등록 처리 후, 로그인
    def post(self, request, username):
        username = request.POST.get('username')

        if len(username) == 0:
            return HttpResponseRedirect(reverse('dalmutid:login', ))

        user, created = User.objects.get_or_create(
            username=username
        )

        game_list = Game.objects.filter(round__lt=13).order_by('-gamename')

        for game in game_list:
            gamer = Gamer.objects.filter(game=game, user=user)
            if not gamer:
                notingamename = game.gamename
                game_list = game_list.exclude(gamename=notingamename)

        context = {
            'user': user,
            'game_list': game_list,
        }

        return render(request, self.template_name, context)


class RuleView(generic.DetailView):
    template_name = "dalmutid/rule.html"

    # 룰북 화면으로 전환
    def get(self, request, username):
        user = User.objects.filter(username=username).first()

        context = {
            'user': user,
        }

        return render(request, self.template_name, context)


class HonorView(generic.DetailView):
    template_name = "dalmutid/honor.html"

    # 전적 화면으로 전환
    def get(self, request, username):
        user = User.objects.filter(username=username).first()

        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')
        honors = Honor.objects.all()

        users_honor = user_exclude_guest.annotate(
            tot_count=Subquery(
                honors.values('user').annotate(tot_count=Count('user')).filter(user_id=OuterRef('id')).values(
                    'tot_count')[:1]),
            king_count=Subquery(honors.filter(position=1).values('user').annotate(king_count=Count('user')).filter(
                user_id=OuterRef('id')).values('king_count')[:1]),
            slave_count=Subquery(
                honors.filter(gamerTotCnt=F("position")).values('user').annotate(slave_count=Count('user')).filter(
                    user_id=OuterRef('id')).values('slave_count')[:1]),
            king_per=Cast(F("king_count"), FloatField())*100/Cast(F("tot_count"), FloatField()),
            slave_per=Cast(F("slave_count"), FloatField())*100/Cast(F("tot_count"), FloatField()),
        )

        users_pick_honor = user_exclude_guest.annotate(
            tot_count=Subquery(
                honors.filter(round=0).values('user').annotate(tot_count=Count('user')).filter(user_id=OuterRef('id')).values(
                    'tot_count')[:1]),
            king_count=Subquery(honors.filter(round=0, position=1).values('user').annotate(king_count=Count('user')).filter(
                user_id=OuterRef('id')).values('king_count')[:1]),
            slave_count=Subquery(
                honors.filter(round=0, gamerTotCnt=F("position")).values('user').annotate(slave_count=Count('user')).filter(
                    user_id=OuterRef('id')).values('slave_count')[:1]),
            king_per=Cast(F("king_count"), FloatField()) * 100 / Cast(F("tot_count"), FloatField()),
            slave_per=Cast(F("slave_count"), FloatField()) * 100 / Cast(F("tot_count"), FloatField()),
        )

        context = {
            'user': user,
            'honor_by_king': users_honor.order_by('-king_per'),
            'honor_by_slave': users_honor.order_by('-slave_per'),
            'pick_by_king': users_pick_honor.order_by('-king_per'),
            'pick_by_slave': users_pick_honor.order_by('-slave_per'),
        }

        return render(request, self.template_name, context)


class RankView(generic.DetailView):
    template_name = "dalmutid/ranking.html"

    # 전적 화면으로 전환
    def get(self, request, username):
        user = User.objects.filter(username=username).first()

        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')
        honors = Honor.objects.exclude(round=0)

        users_ranking = user_exclude_guest.annotate(
            tot_count=Subquery(
                honors.values('user').annotate(tot_count=Count('user')).filter(user_id=OuterRef('id')).values(
                    'tot_count')[:1]),
            king_count=Subquery(honors.filter(position=1).values('user').annotate(king_count=Count('user')).filter(
                user_id=OuterRef('id')).values('king_count')[:1]),
            slave_count=Subquery(
                honors.filter(gamerTotCnt=F("position")).values('user').annotate(slave_count=Count('user')).filter(
                    user_id=OuterRef('id')).values('slave_count')[:1]),
            score=Subquery(
                honors.values('user').annotate(tot_count=Sum(F('gamerTotCnt') - F('position') -2)).filter(user_id=OuterRef('id')).values(
                    'tot_count')[:1]),
        )

        context = {
            'user': user,
            'users_ranking': users_ranking.order_by('-score','tot_count','-king_count','slave_count'),
        }

        return render(request, self.template_name, context)


class NewGameView(generic.DetailView):

    # 새로운 게임을 생성하고, 생성한 사용자를 첫 참가자로 입력
    # 대기화면 페이지로 리다이렉트
    def get(self, request, username):
        user = User.objects.filter(username=username).first()

        gamename = datetime.today().strftime("%Y%m%d%H%M%S")[2:]
        nextgamename = gamename[:-2] + '60'

        # 숫자 + 대소문자
        gamecode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        new_game = Game.objects.create(gamename=gamename, turnUser=user, nextgamename=nextgamename, gamecode=gamecode)

        gamer = Gamer.objects.create(game=new_game, user=user)

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class PrivateGameView(generic.DetailView):
    template_name = "dalmutid/main.html"

    # 게임코드 ingame 입장
    def post(self, request, gamename, username):

        gamecode = request.POST.get('gamecode').upper()

        user = User.objects.filter(username=username).first()
        game = Game.objects.filter(gamecode=gamecode).first()

        if game:
            return HttpResponseRedirect(reverse('dalmutid:ingame', args=(game.gamename, user.username,)))
        else:
            game_list = Game.objects.filter(round__lt=13).order_by('-gamename')

            for game in game_list:
                gamer = Gamer.objects.filter(game=game, user=user)
                if not gamer:
                    notingamename = game.gamename
                    game_list = game_list.exclude(gamename=notingamename)

            context = {
                'user': user,
                'game_list': game_list,
                'message': '존재하지 않는 게임입니다.',
            }

            return render(request, self.template_name, context)


class InGameView(generic.DetailView):
    template_name = "dalmutid/ingame.html"

    # 대기화면에서 게임을 선택하는 경우, 자동으로 참가 진행
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        total_gamer = Gamer.objects.filter(game=game)


        if not total_gamer.filter(user=user) and (len(total_gamer) >= 12 or game.ingameCd!=0):
            template_name = "dalmutid/main.html"

            game_list = Game.objects.filter(round__lte=13).order_by('-gamename')

            for game in game_list:
                gamer = Gamer.objects.filter(game=game, user=user)
                if not gamer:
                    if game.round != 0:
                        notingamename = game.gamename
                        game_list = game_list.exclude(gamename=notingamename)

            context = {
                'user': user,
                'game_list': game_list,
                'message': '해당 게임에 더이상 참가할 수 없습니다.',
            }

            return render(request, template_name, context)
        else:
            gamer, created = Gamer.objects.get_or_create(
                game=game,
                user=user
            )

            gamer_list = total_gamer.filter(position=0)
            ready_gamer_list = total_gamer.exclude(position=0).order_by('position')
            my_cards = Card.objects.filter(game=game, user=user).order_by('card')

            num_list = [x + 1 for x in range(12)]
            already_list = list(ready_gamer_list.values_list('position', flat=True))

            card_list = list(set(num_list) - set(already_list))

            random.shuffle(card_list)

            tax_list = ready_gamer_list.filter(taxYn=True).order_by('position')

            honor_list = []

            for i in range(game.round + 1):
                game_honor = Honor.objects.filter(game=game, round=i).order_by('position')
                if game_honor:
                    honor_list.append(game_honor)

            context = {
                'user': user,
                'gamer': gamer,
                'total_gamer': total_gamer,
                'gamer_list': gamer_list,
                'ready_gamer_list': ready_gamer_list,
                'card_list': card_list,
                'tax_list': tax_list,
                'my_cards': my_cards,
                'honor_list': honor_list,
            }
            return render(request, self.template_name, context)

    # 카드선택 후, 액션 처리(세금수령, 세금면제, 카드제출)
    def post(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()
        gamers = Gamer.objects.filter(game=game).order_by('position')

        action = request.POST.get('action')

        if game.ingameCd == 3:
            ingamers = gamers.exclude(cardTotCnt=0)

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

            if action == "carddraw":
                selectedCards = list(filter(None, request.POST.get('cardlist').replace("dalmutiImg", "").split(";")))
                lastCard = 0
                lastCardCnt = 0
                lastJokerCnt = 0
                for selectedCard in selectedCards:
                    deleteCard, _ = selectedCard.split("_")
                    deleteSelectCard = Card.objects.filter(game=game, user=user, card=deleteCard).first()
                    deleteSelectCard.delete()

                    gamer.cardTotCnt -= 1
                    gamer.save()

                    lastCardCnt += 1
                    if int(deleteCard) != 13:
                        lastCard = int(deleteCard)
                    else:
                        lastJokerCnt += 1

                if lastCard == 0:
                    lastCard = 13

                game.drawusername = user.username
                game.lastCard = lastCard
                game.lastCardCnt = lastCardCnt
                game.lastJokerCnt = lastJokerCnt
                game.save()

                gamer.jokerCnt -= lastJokerCnt
                gamer.save()

                if gamer.cardTotCnt == 0:
                    gamer.nextPosition = len(gamers.exclude(nextPosition=0)) + 1
                    gamer.save()

                    if game.lastCard == 1 or game.lastCardCnt > game.lastCard:
                        game.drawusername = game.turnUser.username
                    game.save()

                else:
                    if game.lastCard == 1 or game.lastCardCnt > game.lastCard:
                        game.turnUser = user
                    game.save()

            elif action == "turnpass":
                drawgamer = gamers.filter(user=User.objects.filter(username=game.drawusername).first()).first()

                if drawgamer.cardTotCnt == 0:
                    indrawgamers = list(ingamers.values_list('position', flat=True))
                    indrawgamers.append(drawgamer.position)
                    indrawgamers = sorted(indrawgamers)
                    drawindex = indrawgamers.index(drawgamer.position)

                    predrawposition = 0
                    nextdrawposition = 0

                    if drawindex == 0:
                        predrawposition = indrawgamers[len(indrawgamers) - 1]
                        nextdrawposition = indrawgamers[drawindex + 1]
                    elif drawindex == len(indrawgamers) - 1:
                        predrawposition = indrawgamers[drawindex - 1]
                        nextdrawposition = indrawgamers[0]
                    else:
                        predrawposition = indrawgamers[drawindex - 1]
                        nextdrawposition = indrawgamers[drawindex + 1]

                    if predrawposition == gamer.position:
                        nextdrawGamer = gamers.filter(position=nextdrawposition).first()
                        game.drawusername = nextdrawGamer.user.username
                        game.save()

        elif game.ingameCd == 2:
            taxuser = User.objects.filter(username=request.POST.get('username')).first()
            taxgamer = Gamer.objects.filter(game=game, user=taxuser).first()

            if action == "taxreceipt":
                taxcards = list(filter(None, request.POST.get('cardlist').replace("dalmutiImg", "").split(";")))
                taxuserCards = Card.objects.values_list('card', flat=True).filter(game=game, user=taxuser).order_by('card')[::1]

                for taxcard in taxcards:
                    deletetaxcard = taxuserCards.pop(0)
                    addMyCard = Card.objects.create(game=game, user=user, card=deletetaxcard)
                    deleteTaxCard = Card.objects.filter(game=game, user=taxuser, card=deletetaxcard).first()
                    deleteTaxCard.delete()

                    addTaxcard, _ = taxcard.split("_")
                    addTaxuserCard = Card.objects.create(game=game, user=taxuser, card=addTaxcard)
                    deleteMyCard = Card.objects.filter(game=game, user=user, card=addTaxcard).first()
                    deleteMyCard.delete()

            gamer.status = 2
            gamer.save()

            taxgamer.status = 2
            taxgamer.save()

            if not gamers.exclude(status=2):
                game.ingameCd = 3
                game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class PickView(generic.DetailView):

    # 게임 최초 시작시, 선 정할 때 카드를 선택하는 경우, 선택된 카드의 정보를 저장
    def get(self, request, gamename, username, card):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        gamer = Gamer.objects.filter(game=game, user=user).first()
        gamer.position = int(card)
        gamer.save()

        game.turnUser = Gamer.objects.filter(game=game).exclude(position=0).order_by('position').first().user
        game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class ShuffleView(generic.DetailView):

    # 카드 분배(게임 시작) 시, 카드 덱을 생성하여 랜덤하게 카드를 분배
    def get(self, request, gamename, username):
        card_deck = [13, 13]

        for i in range(12):
            card_deck += [i + 1 for x in range(i + 1)]

        random.shuffle(card_deck)

        game = Game.objects.filter(gamename=gamename).first()

        gamers = Gamer.objects.filter(game=game).order_by('position')

        not_ready_gamer = gamers.filter(position=0)

        if len(not_ready_gamer) > 0:
            return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))

        if game.round == 0 and game.ingameCd == 0:
            position = 1
            for gamer in gamers:
                honor = Honor.objects.create(game=game, user=gamer.user, gamerTotCnt=len(gamers), position=position)
                gamer.position = position
                gamer.save()
                position += 1

        while card_deck:
            for gamer in gamers:
                card = Card.objects.create(game=game, user=gamer.user, card=card_deck.pop())

                if card.card == 13:
                    gamer.jokerCnt += 1
                gamer.cardTotCnt += 1
                gamer.save()

                if not card_deck:
                    break

        game.round += 1
        game.ingameCd = 1
        game.revYn = False
        game.revusername = ""
        game.drawusername = gamers[0].user.username
        game.lastCard = 0
        game.lastCardCnt = 0
        game.lastJokerCnt = 0
        game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class CardOKView(generic.DetailView):

    # 카드 분배 후, 개별 확인 처리
    # 왕,대주교,농노,노예는 조공 단계로 진입
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        gamers = Gamer.objects.filter(game=game).order_by('position')
        gamer = gamers.filter(user=user).first()

        taxuser = [gamers[i].user.username for i in [0, 1,len(gamers) - 1, len(gamers) - 2]]

        gamer.status = 2
        if username in taxuser:
            if game.round != 1:
                gamer.status = 1
                gamer.taxYn = True
            else:
                if not game.pickHonorYn:
                    gamer.status = 1
                    gamer.taxYn = True
        gamer.save()

        if not gamers.filter(status=0):
            if not gamers.filter(status=1):
                game.ingameCd = 3
            else:
                game.ingameCd = 2
            game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class RevolutionView(generic.DetailView):

    # 카드 분배 후, 레볼루션 처리
    # 조공 단계 패스, 처리유저가 노예일 시, 신분 역전
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        gamers = Gamer.objects.filter(game=game).order_by('position')
        gamer = gamers.filter(user=user).first()

        for ingamer in gamers:
            ingamer.status = 2
            ingamer.save()

        game.ingameCd = 3
        game.revYn = True
        game.revusername = user.username
        game.save()

        if gamers.last().user.username == gamer.user.username:
            position = len(gamers)
            for ingamer in gamers:
                ingamer.position = position
                ingamer.save()
                position -= 1
            game.drawusername = user.username
            game.turnUser = user
            game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class GameEndView(generic.DetailView):

    # 현재 진행중인 게임 종료
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()

        game.round = 13
        game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class GameQuitView(generic.DetailView):

    # 진행전인 게임 나가기
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        gamers = Gamer.objects.filter(game=game).order_by('position')
        gamer = gamers.filter(user=user).first()

        gamer.delete()

        if not gamers:
            game.delete()

        return HttpResponseRedirect(reverse('dalmutid:main', args=(username,)))


class CardAllInView(generic.DetailView):

    # 꼴지 카드 전체 제출 및 게임 종료
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()
        gamer = Gamer.objects.filter(game=game, user=user).first()
        gamers = Gamer.objects.filter(game=game).order_by('position')

        my_cards = Card.objects.filter(game=game, user=user).order_by('card')
        my_cards.delete()

        gamer.cardTotCnt = 0
        gamer.jokerCnt = 0
        gamer.nextPosition = len(gamers.exclude(nextPosition=0)) + 1
        gamer.save()

        nextgamers = gamers.order_by('nextPosition')

        game.ingameCd = 4
        game.turnUser = nextgamers[0].user
        game.save()

        for nextgamer in nextgamers:
            if nextgamer.user.username == game.revusername:
                honor = Honor.objects.create(game=game, user=nextgamer.user, round=game.round,
                                             gamerTotCnt=len(nextgamers), prePosition=nextgamer.position,
                                             position=nextgamer.nextPosition, revYn=True)
            else:
                honor = Honor.objects.create(game=game, user=nextgamer.user, round=game.round,
                                             gamerTotCnt=len(nextgamers), prePosition=nextgamer.position,
                                             position=nextgamer.nextPosition)

            nextgamer.autopassYn = False
            nextgamer.position = nextgamer.nextPosition
            nextgamer.jokerCnt = 0
            nextgamer.status = 0
            nextgamer.taxYn = False
            nextgamer.nextPosition = 0
            nextgamer.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class AutoPassView(generic.DetailView):

    # autopass 기능
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        gamer = Gamer.objects.filter(game=game, user=user).first()

        if gamer.autopassYn:
            gamer.autopassYn = False
        else:
            gamer.autopassYn = True

        gamer.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class RoundRenewView(generic.DetailView):

    # 라운드 취소 기능
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        cards = Card.objects.filter(game=game)
        cards.delete()

        bfgamers = Gamer.objects.filter(game=game).order_by('position')

        if game.revusername == user.username:
            position = len(bfgamers)
            for ingamer in bfgamers:
                ingamer.position = position
                ingamer.save()
                position -= 1

        gamers = Gamer.objects.filter(game=game).order_by('position')

        game.drawusername = gamers[0].user.username
        game.turnUser = gamers[0].user
        game.round -= 1
        game.ingameCd = 4
        game.revYn = False
        game.revusername = ""
        game.save()

        for gamer in gamers:
            gamer.autopassYn = False
            gamer.cardTotCnt = 0
            gamer.jokerCnt = 0
            gamer.status = 0
            gamer.taxYn = False
            gamer.nextPosition = 0
            gamer.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class IntrusionView(generic.DetailView):

    # 평민 난입 기능
    def get(self, request, gamename, username):

        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        new_gamers = Honor.objects.filter(game=game, round=game.round).order_by('position')

        currentgamename = game.nextgamename
        nextgamename = gamename[:-2] + str(int(currentgamename[-2:]) + 1)

        # 숫자 + 대소문자
        gamecode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        new_game = Game.objects.create(gamename=currentgamename, turnUser=new_gamers[0].user, pickHonorYn=False,
                                       nextgamename=nextgamename, gamecode=gamecode)

        for gamer in new_gamers:
            new_gamer = Gamer.objects.create(game=new_game, user=gamer.user, position=gamer.position)

            if new_gamer.position > len(new_gamers) - 2:
                new_gamer.position = 12 - (len(new_gamers) - new_gamer.position)
                new_gamer.save()

        game.round = 13
        game.ingameCd = 4
        game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(currentgamename, username,)))


class ImageChangeView(generic.DetailView):

    # 이미지 변경 기능
    def get(self, request, gamename, username):

        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        game.image = int((game.image + 1)%2)
        game.save()

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))


class TelegramLoginView(generic.ListView):
    template_name = "dalmutid/telegramlogin.html"

    # 현재 활성화된 사용자 리스트를 로그인 화면에 표시
    def get(self, request, gamename, gamecode):

        game = Game.objects.filter(gamename=gamename).first()

        user_only_guest = User.objects.filter(delYn=False, username__startswith='손님').order_by('username')
        user_exclude_guest = User.objects.filter(delYn=False).exclude(username__startswith='손님').order_by('username')

        user_list = list(user_only_guest) + list(user_exclude_guest)

        context = {
            'game': game,
            'user_list': user_list,
        }

        return render(request, self.template_name, context)


class TelegramView(generic.DetailView):

    # 텔레그램 전송
    def get(self, request, gamename, username):
        game = Game.objects.filter(gamename=gamename).first()
        user = User.objects.filter(username=username).first()

        bot = telegram.Bot(token='1480423142:AAHkkAlgShepdoXFW2HP8TzZAiRfCN8WpHI')
        bot.sendMessage(chat_id='-413309173',
                        text='[게임코드(달무티팀):' + game.gamecode + '](http://35.230.124.241:8080/dalmutid/telegram/login/' + game.gamename + '/' + game.gamecode + '/)',
                        parse_mode='Markdown', disable_web_page_preview=True)

        return HttpResponseRedirect(reverse('dalmutid:ingame', args=(gamename, username,)))
