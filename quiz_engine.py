def calculate_score(
    questions,
    user_answers
):

    correct = 0

    for index, question in enumerate(
        questions
    ):

        if index < len(user_answers):

            if (
                user_answers[index]
                == question["answer"]
            ):

                correct += 1

    total = len(questions)

    wrong = total - correct

    percentage = (
        correct / total * 100
        if total > 0
        else 0
    )

    return {
        "correct": correct,
        "wrong": wrong,
        "total": total,
        "percentage": percentage
    }