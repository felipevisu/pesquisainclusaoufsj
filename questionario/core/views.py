from django.db import reset_queries
from questionario.core.forms import SendForm
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.sessions.models import Session
from django.contrib import messages

from ..answers.models import Response
from ..questions.models import Group
from ..questions.forms import SurveyForm

from .forms import SendForm
from .utils import get_results

class IntroView(TemplateView):
    template_name = "intro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FinalizedView(TemplateView):
    template_name = "finalized.html"

    def get_response(self):
        pk = self.kwargs.get('pk')
        response = Response.objects.get(pk=pk)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = self.get_response()
        results = get_results(response)

        context['response'] = response
        context["results"] = results

        return context

    def dispatch(self, request, *args, **kwargs):
        response = self.get_response()
        if not response.finalized:
            group = Group.objects.last()
            return redirect(reverse_lazy('survey_form', kwargs={'pk': group.pk}))
        return super().dispatch(request, *args, **kwargs)


class SurveyView(FormView):
    form_class = SurveyForm
    template_name = "survey.html"

    def get_group(self):
        group_pk = self.kwargs['pk']
        group = Group.objects.get(pk=group_pk)
        return group

    def get_response(self):
        session_key = self.request.session.session_key
        session = Session.objects.filter(session_key=session_key).first()

        if not session:
            try:
                del self.request.session['session_key']
                self.request.session.modified = True
            except:
                pass
            self.request.session.create()
            session_key = self.request.session.session_key
            session = Session.objects.filter(session_key=session_key).first()

        response, _ = Response.objects.get_or_create(session=session)
        return response

    def dispatch(self, request, *args, **kwargs):
        response = self.get_response()
        if response.finalized:
            return redirect(reverse_lazy('finalized', kwargs={"pk": response.pk}))
        group = self.get_group()
        prev = Group.objects.filter(order__lt=group.order).order_by('order').last()
        if prev:
            response = self.get_response()
            response_questions = response.answers.values_list('question_id', flat=True)
            prev_questions = prev.questions.values_list('id', flat=True)
            for item in prev_questions:
                if item not in response_questions:
                    return redirect(reverse_lazy('survey_form', kwargs={'pk': prev.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        group = self.get_group()
        context['high'] = group.questions.first().number
        context['group'] = group
        context['groups'] = groups
        context["next"] = Group.objects.filter(order__gt=group.order).order_by('order').first()
        context["prev"] = Group.objects.filter(order__lt=group.order).order_by('order').last()
        context['is_first'] = groups.first() == group
        context['is_last'] = groups.last() == group
        return context

    def get_form_kwargs(self):
        response = self.get_response()
        group = self.get_group()
        kwargs = super().get_form_kwargs()
        kwargs.update({'group': group, 'response': response})
        return kwargs

    def form_valid(self, form):
        form.save()
        group = self.get_group()
        new_group = Group.objects.filter(order__gt=group.order).order_by('order').first()
        if new_group:
            messages.add_message(self.request, messages.SUCCESS, f"{group.name} preenchida com sucesso!")
            return redirect(reverse_lazy('survey_form', kwargs={'pk': new_group.pk}))
        response = self.get_response()
        response.finalized = True
        response.save()
        response.session.delete()
        return redirect(reverse_lazy('finalized', kwargs={'pk': response.pk}))

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('survey_form', kwargs={'pk': self.kwargs['pk']})


class RestartView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        try:
            del self.request.session['session_key']
            request.session.modified = True
        except:
            pass
        request.session.create()
        return redirect(reverse_lazy('intro'))


class SendView(FormView):
    form_class = SendForm
    template_name = "send.html"

    def get_response(self):
        session_key = self.request.session.session_key
        session = Session.objects.filter(session_key=session_key).first()
        if session:
            response = Response.objects.filter(session=session).first()
            return response
        return None

    def form_valid(self, form):
        response = self.get_response()
        if response:
            results = get_results(response)
            form.send(results)
            messages.add_message(self.request, messages.SUCCESS, "Email enviado com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('send')