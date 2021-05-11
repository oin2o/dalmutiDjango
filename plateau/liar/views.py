import random

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import Category, Words


class MainView(generic.ListView):
    template_name = "liar/main.html"

    def get(self, request):
        categories = Category.objects.all()

        context = {
            'categories': categories,
        }

        return render(request, self.template_name, context)


class GameView(generic.ListView):
    template_name = "liar/main.html"

    def get(self, request, categoryname):
        category = Category.objects.filter(categoryname=categoryname).first()

        context = {
            'category': category,
            'number': 3,
        }

        return render(request, self.template_name, context)

    def post(self, request, categoryname):
        category = Category.objects.filter(categoryname=categoryname).first()

        words = Words.objects.filter(category=category).all()

        number = int(request.POST.get('number'))

        word = None

        if len(words) > 0:
            word = words[random.randrange(0, len(words))]

        liar = ['citizen' for _ in range(number - 1)]
        liar.append('liar')
        if number > 5:
            liar.pop(0)
            liar.append('trickster')
        random.shuffle(liar)

        context = {
            'category': category,
            'number': number,
            'word': word,
            'liar': liar,
        }

        return render(request, self.template_name, context)


class CategoryView(generic.ListView):
    template_name = "liar/category.html"

    def get(self, request):
        categories = Category.objects.all()

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
        categories = Category.objects.all()

        context = {
            'categories': categories,
        }

        return render(request, self.template_name, context)


class WordDetailView(generic.ListView):
    template_name = "liar/word.html"

    def get(self, request, categoryname):
        category = Category.objects.filter(categoryname=categoryname).first()

        words = Words.objects.filter(category=category).all()

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

        words = Words.objects.filter(category=category).all()

        context = {
            'category': category,
            'words': words,
        }

        return render(request, self.template_name, context)
