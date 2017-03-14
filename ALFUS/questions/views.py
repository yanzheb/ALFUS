from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils import timezone
from django.http import Http404
from .models import Choice, Question
from random import randint
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def search(request):
    try:
        q = request.GET['q']
        topics = Question.objects.filter(topic_text__icontains=q)
        return render_to_response('questions/search.html', {'topics': topics, 'q':q})
    except KeyError:
        return render_to_response('questions/search.html')

@login_required(login_url="/login/")
def index(request):
    question_list = Question.objects.all
    return render(request, 'questions/index.html', {'question_list': question_list})


@login_required(login_url="/login/")
def detail(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist")
    return render(request, 'questions/detail.html', {'question': question})


@login_required(login_url="/login/")
def answer(request, question_id):
    all_question_id = Question.objects.values_list('id', flat=True)
    random_number = randint(1, len(all_question_id))
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'questions/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        return render(request, 'questions/results.html', {'question': question, 'is_correct': selected_choice.is_correct, 'random_q': random_number})
