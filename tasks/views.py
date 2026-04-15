from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from tasks.models import Task
from tasks.forms import TaskForm

class HomeView(TemplateView):
    template_name = 'home.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_qs = Task.objects.select_related('category', 'priority').order_by('deadline')
        counts = task_qs.aggregate(
            pending_count=Count('id', filter=Q(status='Pending')),
            in_progress_count=Count('id', filter=Q(status='In Progress')),
            completed_count=Count('id', filter=Q(status='Completed')),
        )
        context['latest_tasks'] = task_qs.exclude(status='Completed')[:3]
        context['total_tasks'] = task_qs.count()
        context['pending_count'] = counts['pending_count']
        context['in_progress_count'] = counts['in_progress_count']
        context['completed_count'] = counts['completed_count']
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    paginate_by = 8
    ordering = ('deadline', '-created_at')

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority').order_by(*self.ordering)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('tasks')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.select_related('category', 'priority')

class MyProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'something.html'
    # ... other attributes


@login_required
@require_POST
def mark_task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'Completed'
    task.save(update_fields=['status', 'updated_at'])
    return redirect('tasks')