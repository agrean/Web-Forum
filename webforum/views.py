from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm, PostForm
from django.http import Http404
from .models import Forum, Topic, Post


# Create your views here.

def home(request):
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums': forums})


def forum_topics(request, pk):
    try:
        forum = Forum.objects.get(pk=pk)
    except Forum.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'forum': forum})


@login_required
def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'forum': forum, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})