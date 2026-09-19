import os
import json
import re

from groq import Groq
from dotenv import load_dotenv


# -----------------------------------------
# LOAD API KEY
# -----------------------------------------

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please check your .env file."
    )


# -----------------------------------------
# GROQ CLIENT
# -----------------------------------------

client = Groq(api_key=API_KEY)

# Current recommended Groq model
MODEL_NAME = "openai/gpt-oss-20b"


# -----------------------------------------
# CLEAN TEXT
# -----------------------------------------

def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------------------
# GENERATE MCQs
# -----------------------------------------

def generate_questions(
    text,
    num_questions=5,
    difficulty="Medium",
    count=None
):

    # Support count parameter also
    if count is not None:
        num_questions = count

    # Empty input
    if not text or not text.strip():
        return []

    text = clean_text(text)

    prompt = f"""
You are an expert teacher and MCQ generator.

Generate {num_questions} meaningful multiple-choice questions
about the following topic or study material:

{text}

Difficulty level: {difficulty}

IMPORTANT REQUIREMENTS:

1. Generate exactly {num_questions} questions.
2. Questions must test understanding.
3. Do not create blank or fill-in-the-blank questions.
4. Each question must have exactly 4 options.
5. Options must be A, B, C and D.
6. Only one option can be correct.
7. The answer must be A, B, C, or D.
8. Provide a short explanation.
9. Avoid duplicate questions.
10. If the user gives only a topic such as "RAG",
    create meaningful questions about that topic.
11. Return ONLY valid JSON.
12. Do not use Markdown.
13. Do not use ```.

Return exactly this format:

{{
    "questions": [
        {{
            "question": "What does RAG stand for?",
            "options": {{
                "A": "Retrieval-Augmented Generation",
                "B": "Random Answer Generation",
                "C": "Remote AI Gateway",
                "D": "Rapid Application Generator"
            }},
            "answer": "A",
            "explanation": "RAG stands for Retrieval-Augmented Generation."
        }}
    ]
}}
"""

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are an expert educational assistant "
                        "that generates accurate MCQs."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2,

            max_completion_tokens=4000,

            response_format={
                "type": "json_object"
            }
        )


        # -----------------------------------------
        # GET AI RESPONSE
        # -----------------------------------------

        result = response.choices[0].message.content

        print("\n========== GROQ RESPONSE ==========")
        print(result)
        print("===================================\n")


        if not result:
            print("Empty response from Groq.")
            return []


        # -----------------------------------------
        # PARSE JSON
        # -----------------------------------------

        try:

            data = json.loads(result)

        except json.JSONDecodeError:

            print("JSON parsing failed.")

            # Try extracting JSON manually

            start = result.find("{")
            end = result.rfind("}")

            if start == -1 or end == -1:

                print("No JSON object found.")

                return []

            result = result[start:end + 1]

            data = json.loads(result)


        # -----------------------------------------
        # GET QUESTIONS
        # -----------------------------------------

        questions = data.get("questions", [])

        if not isinstance(questions, list):

            print("Questions is not a list.")

            return []


        final_questions = []


        # -----------------------------------------
        # VALIDATE QUESTIONS
        # -----------------------------------------

        for q in questions:

            if not isinstance(q, dict):
                continue


            question = str(
                q.get("question", "")
            ).strip()


            options = q.get(
                "options",
                {}
            )


            answer = str(
                q.get("answer", "")
            ).strip().upper()


            explanation = str(
                q.get("explanation", "")
            ).strip()


            # Question check
            if not question:
                continue


            # Options check
            if not isinstance(options, dict):
                continue


            required_options = [
                "A",
                "B",
                "C",
                "D"
            ]


            if not all(
                option in options
                for option in required_options
            ):

                continue


            # Answer check
            if answer not in required_options:
                continue


            # Add valid question

            final_questions.append(

                {
                    "question": question,

                    "options": {
                        "A": str(options["A"]),
                        "B": str(options["B"]),
                        "C": str(options["C"]),
                        "D": str(options["D"])
                    },

                    "answer": answer,

                    "explanation": explanation
                }

            )


        print(
            "VALID QUESTIONS:",
            len(final_questions)
        )


        return final_questions[:num_questions]


    # -----------------------------------------
    # ERROR HANDLING
    # -----------------------------------------

    except Exception as e:

        print("\n========== GROQ ERROR ==========")

        print(
            "ERROR TYPE:",
            type(e).__name__
        )

        print(
            "ERROR:",
            str(e)
        )

        print(
            "================================\n"
        )

        return []