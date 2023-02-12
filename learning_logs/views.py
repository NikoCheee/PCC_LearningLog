from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator  # відповідає за розбиття на сторінки
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """Головна сторінка журналу спостережень"""
    # реалізація пошуку
    strval = request.GET.get('search', False)  # GET - словник, get - метод
    if strval:
        query = Q(entry_name__icontains=strval)  # шукає по заголовку
        query.add(Q(text__icontains=strval), Q.OR)  # шукає по тексту
        query.add(Q(tags__name__in=[strval]), Q.OR)
        entries = Entry.objects.filter(query).select_related().order_by('-date_added').distinct()[:10]

        paginator = Paginator(entries, 10)  # показати 10 дописів на сторінці
        page_number = request.GET.get('page')  # гет реквест щоб отримати номер сторінки
        page_obj = paginator.get_page(page_number)  # отримати номер сторінки і відобразити її данні для контексту

        context = {'entries': entries, 'page': page_obj, 'search': strval}
        return render(request, 'learning_logs/topic.html', context)

    return render(request, 'learning_logs/index.html')


# def check(request):
#     if Topic.owner != request.user:
#         raise Http404


@login_required()
def topics(request):
    """Показує усі теми"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Показати одну тему та все що там введено"""
    topic = get_object_or_404(Topic, id=topic_id)
    # Пересвідчитись, що тема належить поточному користувачу
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')

    paginator = Paginator(entries, 10)  # показати 10 дописів на сторінці
    page_number = request.GET.get('page')  # гет реквест щоб отримати номер сторінки
    page_obj = paginator.get_page(page_number)  # отримати номер сторінки і відобразити її данні для контексту

    context = {'topic': topic, 'entries': entries, 'page': page_obj}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def entry(request, entry_id):
    """Показати один допис"""
    entry = get_object_or_404(Entry, id=entry_id)
    context = {'topic': topic, 'entry': entry}
    return render(request, 'learning_logs/entry.html', context)


@login_required()
def new_topic(request):
    """Додати нову тему"""
    if request.method != 'POST':
        # Жодних даних не відправлено; стоврити порожню форму
        form = TopicForm()
    else:
        # відправлений пост; обробити дані
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Показати порожню або недійсну форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    # Додати новий допис у наявну тему
    topic = Topic.objects.get(id=topic_id)
    # Пересвідчитись, що тема належить поточному користувачу
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Жодних даних не відправлено; стоврити порожню форму
        form = EntryForm()
    else:
        # Отримати дані у ПОСТ-запиті; обробити дані
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            form.save_m2m()
            return redirect('learning_logs:topic', topic_id=topic_id)
#
    # Показати порожню або недійсну форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """Редагувати існуючий допис"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    name = entry.entry_name
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # сформувати запит; вивести поточний допис
        form = EntryForm(instance=entry)
    else:
        # Отримати дані у ПОСТ-запиті; обробити дані
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'name': name, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


class EntryDeleteView(DeleteView):
    model = Entry
    template_name = 'learning_logs/entry_delete.html'

    def get_success_url(self):
        topic = self.object.topic
        return reverse('learning_logs:topic', args=[topic.pk])
