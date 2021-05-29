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

        total = round(total/questions.count(), 2)

        result["total"] = total
        result["name"] = category.name
        result["description"] = category.description

        print(total)

        if total >= 5:
            result["text"] = category.text_1

        if total > 2.5 and total < 5:
            result["text"] = category.text_2

        if total <= 2.5:
            result["text"] = category.text_3

        results.append(result)

    return results