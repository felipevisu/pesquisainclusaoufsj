from django import forms

from ..answers.models import Response, Answer
from . import QuestionType

RANK_1 = (
    ("1", "(1) Discordo totalmente"),
    ("2", "(2) Discordo muito"),
    ("3", "(3) Discordo pouco"),
    ("4", "(4) Concordo pouco"),
    ("5", "(5) Concordo muito"),
    ("6", "(6) Concordo totalmente"),
)

RANK_2 = (
    ("1", "(1) Discordo totalmente"),
    ("2", "(2) Discordo muito"),
    ("3", "(3) Discordo pouco"),
    ("4", "(4) Concordo pouco"),
    ("5", "(5) Concordo muito"),
    ("6", "(6) Concordo totalmente"),
    ("7", "Não se aplica"),
)


def save_answers(items, response):
    for field_name, field_value in items:
        if field_name.startswith("question_"):
            question_id = int(field_name.split("_")[1])
            answer, _ = Answer.objects.get_or_create(question_id=question_id, response=response)
            answer.body = field_value
            answer.save()


class SurveyForm(forms.Form):

    def __init__(self, group, response, *args, **kwargs):
        self.group = group
        self.response = response

        super(SurveyForm, self).__init__(*args, **kwargs)
        data = kwargs.get('data')

        for question in group.questions.all():
            field_id = "question_" + str(question.pk)
            label = str(question.question)

            if question.type == QuestionType.RANK:
                self.fields[field_id] = forms.ChoiceField(label=label, widget=forms.RadioSelect, choices=RANK_1)
            if question.type == QuestionType.RANK_2:
                self.fields[field_id] = forms.ChoiceField(label=label, widget=forms.RadioSelect, choices=RANK_2)
            if question.type == QuestionType.TEXT:
                self.fields[field_id] = forms.CharField(label=label)
            if question.type == QuestionType.RADIO:
                choices = question.get_choices()
                self.fields[field_id] = forms.ChoiceField(label=label, widget=forms.RadioSelect, choices=choices)
            if question.type == QuestionType.SELECT:
                choices = question.get_choices()
                choices = tuple([('', 'Selecione uma opção')]) + choices
                self.fields[field_id] = forms.ChoiceField(label=label, widget=forms.Select, choices=choices)
            if question.type == QuestionType.DROPBOX:
                choices = question.get_choices()
                self.fields[field_id] = forms.MultipleChoiceField(label=label, widget=forms.CheckboxSelectMultiple, choices=choices)

            if not question.required:
                self.fields[field_id].required = False

            answer = response.answers.filter(question=question).first()
            if answer:
                self.fields[field_id].initial = answer.body

    def save(self):
        response = self.response
        save_answers(self.cleaned_data.items(), response)