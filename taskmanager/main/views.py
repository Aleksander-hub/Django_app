from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Advertisement
from .forms import TaskForm, RegisterUserForm, LoginUserForm, AdvertisementForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import DataMixin


def index(request):
    advertisements = Advertisement.objects.order_by('-created_at')
    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'advertisements': advertisements})


def about(request):
    return render(request, 'main/about.html')
    

@login_required(login_url='login')
def create(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('index')
        else:
            error = 'Форма была не валидна'
        
    form = TaskForm()
    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'main/create.html', context)
    
    
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация успешна! Теперь вы можете войти в систему.')
        return response


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return reverse_lazy('index')
    

@login_required(login_url='login')
def cabinet(request):
    user_advertisements = Advertisement.objects.filter(user=request.user)
    context = {
        'title': 'Личный кабинет',
        'advertisements': user_advertisements,
    }
    return render(request, 'main/cabinet.html', context)


@login_required(login_url='login')
def add_advertisement(request):
    if request.user.advertisement_set.count() >= 3:
        messages.error(request, 'Вы достигли лимита в 3 объявления. Удалите старое объявление, чтобы добавить новое.')
        return redirect('cabinet')

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            messages.success(request, 'Объявление успешно добавлено!')
            return redirect('cabinet')
        else:
            messages.error(request, 'Форма была не валидна.')
    else:
        form = AdvertisementForm()

    context = {
        'title': 'Добавить объявление',
        'form': form,
    }
    return render(request, 'main/add_advertisement.html', context)


@login_required(login_url='login')
def edit_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('cabinet')
        else:
            messages.error(request, 'Форма была не валидна.')
    else:
        form = AdvertisementForm(instance=advertisement)

    context = {
        'title': 'Редактировать объявление',
        'form': form,
    }
    return render(request, 'main/edit_advertisement.html', context)


@login_required(login_url='login')
def delete_advertisement(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk, user=request.user)
    if request.method == 'POST':
        advertisement.delete()
        messages.success(request, 'Объявление успешно удалено!')
        return redirect('cabinet')
    context = {
        'title': 'Удалить объявление',
        'advertisement': advertisement,
    }
    return render(request, 'main/confirm_delete.html', context)
    
    
