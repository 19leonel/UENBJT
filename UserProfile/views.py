from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import login_required
from .import form
from api.models import Theme

# Create your views here.


class LoginViews(LoginView):
    template_name = "registration/login.html"
    form_class = form.loginForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visible'] = 'invisible'
        context['title'] = 'Iniciar Session'
        return context


class UserViews(LoginRequiredMixin, ListView):
    template_name = "src/user.html"
    model = User


class UserCreateView(FormView):
    template_name = "registration/Signup1.html"
    form_class = form.UserCreationForm2
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        print('desde dispatch \n\n')
        print(self.dispatch)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = form.save()
        print(usuario)
        login(self.request, usuario)
        return super().form_valid(form)

    def form_invalid(self, form):
        print('desde form_invalid')
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def perfil(request):
    return render(request, "src/index.html")


@login_required
def taskView(request):
    return HttpResponse('TasK')


def SigNout(request):
    logout(request)
    return redirect('login')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "option/cambiar_img.html"
    form_class = form.ImgUpdateForm
    success_url = reverse_lazy('index')


@login_required
def index(request):
    return redirect('index')
