from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from . import forms
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta

# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def profile(request):
    return redirect('landing')

class TodoList(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name='tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user =self.request.user)
        context['type']= 'All Tasks'
        return context
    
class TodoList_7days(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name='tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user =self.request.user)
        one_week_from_now= datetime.today() + timedelta(days=7)
        context['tasks']= context['tasks'].filter(date__lte=one_week_from_now)
        context['type']= 'Next 7 Days of Tasks'
        return context

class TodoList_incomplete(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name='tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user =self.request.user)
        context['tasks']= context['tasks'].filter(complete = False)
        context['type']= 'Incomplete Tasks'
        return context
    
class TodoList_completed(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name='tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user =self.request.user)
        context['tasks']= context['tasks'].filter(complete = True)
        context['type']= 'Completed Tasks'
        return context
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = forms.TaskForm
    def get_success_url(self):
        return reverse('todolist')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = forms.TaskForm
    def get_success_url(self):
        return reverse('todolist')
    
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name= 'task'
    success_url= reverse_lazy('todolist')

class RegisterPage(FormView):
    template_name= 'Tasks/register.html'
    form_class =UserCreationForm
    redirect_authenticated_user = True
    success_url= reverse_lazy('landing')
    
    def form_valid(self, form):
        user =form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('landing')
        return super(RegisterPage,self).get(*args,**kwargs)