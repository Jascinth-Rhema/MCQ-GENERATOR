def validate_mcq(mcq):

    if not mcq:
        return False

    if "question" not in mcq:
        return False

    if not mcq["question"]:
        return False

    if "options" not in mcq:
        return False

    options = mcq["options"]

    if not isinstance(options, dict):
        return False

    required_options = ["A", "B", "C", "D"]

    if not all(
        option in options
        for option in required_options
    ):
        return False

    if "answer" not in mcq:
        return False

    if mcq["answer"] not in required_options:
        return False

    return True


def remove_duplicates(questions):

    unique_questions = []
    seen = set()

    for question in questions:

        question_text = (
            question["question"]
            .lower()
            .strip()
        )

        if question_text not in seen:

            seen.add(question_text)

            unique_questions.append(
                question
            )

    return unique_questions