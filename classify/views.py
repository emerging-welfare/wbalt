from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import TextFile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .forms import UserForm


# Create your views here.


def index(request):
    all_texts = TextFile.objects.all()
    context = {'all_texts': all_texts}
    return render(request, 'classify/index.html', context)

def detail(request, text_id):
    all_texts = TextFile.objects.get(pk=text_id)
    context = {'all_texts': all_texts}
    return render(request, 'classify/detail.html', context)

def filtered(request):
    # İşaretlenmemiş datalardan biri verilecek.
    # İşaretlenmiş ilk eleman veriliyor.
    if request.user.is_authenticated:
        username = request.user.username
    all_new_texts = TextFile.objects.filter(info__contains={username: False})[0]
    context= {'all_new_texts': all_new_texts}
    return render(request, 'classify/filtered.html', context)


def agreed(request):
    if request.user.is_authenticated:
        username = request.user.username
    all_new_texts = TextFile.objects.filter(info__contains={username: False})[0]
    all_new_texts.info[username] = True
    all_new_texts.save()
    context = {'all_new_texts': all_new_texts}
    #return render(request, 'classify/agreed.html', context)
    return redirect('filtered')

def nonagreed(request):
    if request.user.is_authenticated:
        username = request.user.username
    all_new_texts = TextFile.objects.filter(info__contains={username: False})[0]
    all_new_texts.info[username] = False
    all_new_texts.save()
    context = {'all_new_texts': all_new_texts}
    #return render(request, 'classify/nonagreed.html', context)
    return redirect('filtered')

def protest(request, text_id):
    if request.user.is_authenticated:
        username = request.user.username
    all_new_texts = TextFile.objects.get(pk=text_id)
    all_new_texts.info[username] = True
    all_new_texts.save()
    context = {'all_new_texts': all_new_texts}
    #return render(request, 'classify/changeprotest.html', context)
    return redirect('tagged')

def nonprotest(request, text_id):
    if request.user.is_authenticated:
        username = request.user.username
    all_new_texts = TextFile.objects.get(pk=text_id)
    all_new_texts.info[username] = False
    all_new_texts.save()
    context = {'all_new_texts': all_new_texts}
    #return render(request, 'classify/changenonprotest.html', context)
    return redirect('tagged')

def tagged(request):
    if request.user.is_authenticated:
        username = request.user.username
    all_true_texts = TextFile.objects.filter(info__contains={username: True})
    all_false_texts = TextFile.objects.filter(info__contains={username: False})
    context = {'all_true_texts': all_true_texts,
               'all_false_texts': all_false_texts}
    return render(request, 'classify/tagged.html', context)

class UserFormView(View):
    form_class = UserForm
    template_name = 'classify/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('classify/')

        return render(request, self.template_name, {'form': form})
