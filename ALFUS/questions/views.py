from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404

from .forms import AnswerForm
from .models import Choice, Question



def index(request):

    question_list = Question.objects.filter(
                    pub_date__lte=timezone.now()
                    ).order_by('-pub_date')[:5]
    return render(request, 'questions/index.html',{ 'question_list' : question_list})

def detail(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist")
    return render(request, 'questions/detail.html', {'question': question})

def answer(request, question_id):
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
        return render(request, 'questions/results.html', {'question': question, 'is_correct': selected_choice.is_correct})

