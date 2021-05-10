import random

from django.shortcuts import render
from django.views import generic


class MainView(generic.ListView):
    template_name = "lotto/main.html"

    def get(self, request):

        context = {
            'action': 'all',
            'data': [],
            'ball_list': [],
        }

        return render(request, self.template_name, context)

    def post(self, request):

        action = request.POST.get('action')
        data = request.POST.get('data')
        if data:
            data = list(map(int, data.split(',')))

        balls = list(set(list(range(1, 46))).difference(data))

        ball_list = []

        random.shuffle(balls)


        if action == 'exclude':
            # balls 에서 6개 선택 5회
            for _ in range(5):
                rand_lotto = random.sample(balls, 6)
                rand_lotto.sort()
                ball_list.append(rand_lotto)
        else:
            # balls 에서 6 - len(data) 선택 5회
            for _ in range(5):
                rand_lotto = list(set().union(data, random.sample(balls, 6 - len(data))))
                rand_lotto.sort()
                ball_list.append(rand_lotto)

        context = {
            'action': action,
            'data': data,
            'ball_list': ball_list,
        }

        return render(request, self.template_name, context)
