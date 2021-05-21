from ..questions.models import Category

def get_results(response):
    results = []

    for category in Category.objects.all():
        result = {}
        total = 0
        questions = category.questions.values_list('pk', flat=True)
        answers = response.answers.filter(question_id__in=questions)
        for answer in answers:
            total = total + int(answer.body)

        result["total"] = round(total/questions.count(), 2)
        result["name"] = category.name
        result["description"] = category.description

        if total <= 2.5:
            result["text"] = category.text_3
        elif total > 2.5 and total < 5:
            result["text"] = category.text_2
        else:
            result["text"] = category.text_1

        results.append(result)

    return results