import streamlit as st
import pandas as pd

from mcq_generator import generate_questions
from text_processor import prepare_text
from validator import validate_mcq, remove_duplicates
from quiz_engine import calculate_score


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI MCQ Generator",
    page_icon="📝",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    .question-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    .result-box {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #ddd;
        text-align: center;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "questions" not in st.session_state:
    st.session_state.questions = []

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "user_answers" not in st.session_state:
    st.session_state.user_answers = []


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">AI MCQ Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate intelligent multiple-choice questions from your study material</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Settings")

question_count = st.sidebar.slider(
    "Number of Questions",
    min_value=1,
    max_value=10,
    value=5
)

difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    ["Easy", "Medium", "Hard"]
)

st.sidebar.markdown("---")

st.sidebar.subheader("Features")

st.sidebar.write("• AI Question Generation")
st.sidebar.write("• Difficulty Selection")
st.sidebar.write("• Quiz Mode")
st.sidebar.write("• Score Calculation")
st.sidebar.write("• Answer Explanation")
st.sidebar.write("• Duplicate Detection")
st.sidebar.write("• CSV Download")


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("Study Material")

input_method = st.radio(
    "Choose Input Method",
    ["Paste Text", "Upload TXT"],
    horizontal=True
)

study_text = ""


# --------------------------------------------------
# PASTE TEXT
# --------------------------------------------------

if input_method == "Paste Text":

    study_text = st.text_area(
        "Paste your study material here",
        height=250,
        placeholder="Example: Artificial Intelligence is a branch of computer science..."
    )


# --------------------------------------------------
# UPLOAD TXT
# --------------------------------------------------

else:

    uploaded_file = st.file_uploader(
        "Upload a TXT file",
        type=["txt"]
    )

    if uploaded_file is not None:
        study_text = uploaded_file.read().decode("utf-8")


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

st.markdown("---")

generate_button = st.button(
    "Generate MCQs",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# GENERATE QUESTIONS
# --------------------------------------------------

if generate_button:

    if not study_text.strip():

        st.warning("Please enter or upload study material first.")

    else:

        with st.spinner("AI is generating your questions..."):

            try:

                # Clean and prepare text
                prepared_text = prepare_text(study_text)

                # Generate questions
                generated_questions = generate_questions(
                    prepared_text,
                    count=question_count,
                    difficulty=difficulty
                )

                # Validate questions
                valid_questions = []

                for question in generated_questions:

                    if validate_mcq(question):
                        valid_questions.append(question)

                # Remove duplicate questions
                valid_questions = remove_duplicates(valid_questions)

                # Store questions
                st.session_state.questions = valid_questions

                # Reset quiz
                st.session_state.submitted = False
                st.session_state.user_answers = []

                if len(valid_questions) > 0:

                    st.success(
                        f"{len(valid_questions)} MCQ(s) generated successfully!"
                    )

                else:

                    st.warning(
                        "The AI could not generate valid questions. "
                        "Please try again with different study material."
                    )

            except Exception as e:

                st.error("Something went wrong while generating questions.")

                st.code(str(e))


# --------------------------------------------------
# DISPLAY GENERATED QUESTIONS
# --------------------------------------------------

questions = st.session_state.questions


if questions:

    st.markdown("---")

    st.header("Generated Questions")

    for index, question in enumerate(questions):

        st.markdown(
            f"""
            <div class="question-box">
            <h3>Question {index + 1}</h3>
            <p><b>{question["question"]}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(f"A. {question['options']['A']}")
        st.write(f"B. {question['options']['B']}")
        st.write(f"C. {question['options']['C']}")
        st.write(f"D. {question['options']['D']}")

        with st.expander("Show Answer & Explanation"):

            st.write(
                f"**Correct Answer:** {question['answer']}"
            )

            st.write(
                f"**Explanation:** {question['explanation']}"
            )


    # --------------------------------------------------
    # QUIZ MODE
    # --------------------------------------------------

    st.markdown("---")

    st.header("Quiz Mode")

    st.write(
        "Answer the questions below and submit the quiz to see your score."
    )


    # Make sure answers list has correct length
    if len(st.session_state.user_answers) != len(questions):

        st.session_state.user_answers = [
            None for _ in questions
        ]


    # --------------------------------------------------
    # QUIZ QUESTIONS
    # --------------------------------------------------

    for index, question in enumerate(questions):

        st.subheader(
            f"Question {index + 1}"
        )

        st.write(
            question["question"]
        )

        options = [
            f"A. {question['options']['A']}",
            f"B. {question['options']['B']}",
            f"C. {question['options']['C']}",
            f"D. {question['options']['D']}"
        ]

        selected_option = st.radio(
            "Choose your answer:",
            options,
            key=f"question_{index}",
            index=None
        )

        if selected_option:

            selected_letter = selected_option[0]

            st.session_state.user_answers[index] = selected_letter


    # --------------------------------------------------
    # SUBMIT QUIZ
    # --------------------------------------------------

    submit_button = st.button(
        "Submit Quiz",
        type="primary",
        use_container_width=True
    )


    if submit_button:

        if any(
            answer is None
            for answer in st.session_state.user_answers
        ):

            st.warning(
                "Please answer all questions before submitting."
            )

        else:

            st.session_state.submitted = True


    # --------------------------------------------------
    # QUIZ RESULT
    # --------------------------------------------------

    if st.session_state.submitted:

        result = calculate_score(
            questions,
            st.session_state.user_answers
        )

        st.markdown("---")

        st.header("Quiz Result")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Questions",
                result["total"]
            )

        with col2:
            st.metric(
                "Correct",
                result["correct"]
            )

        with col3:
            st.metric(
                "Wrong",
                result["wrong"]
            )

        with col4:
            st.metric(
                "Score",
                f"{result['percentage']:.1f}%"
            )


        # --------------------------------------------------
        # RESULT MESSAGE
        # --------------------------------------------------

        st.markdown(
            f"""
            <div class="result-box">

            <h2>Your Score: {result['percentage']:.1f}%</h2>

            <p>
            You answered {result['correct']} out of
            {result['total']} questions correctly.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # --------------------------------------------------
        # ANSWER REVIEW
        # --------------------------------------------------

        st.markdown("---")

        st.header("Answer Review")

        for index, question in enumerate(questions):

            user_answer = st.session_state.user_answers[index]

            correct_answer = question["answer"]

            st.subheader(
                f"Question {index + 1}"
            )

            st.write(
                question["question"]
            )

            if user_answer == correct_answer:

                st.success(
                    f"Your Answer: {user_answer} — Correct"
                )

            else:

                st.error(
                    f"Your Answer: {user_answer} — Wrong"
                )

                st.info(
                    f"Correct Answer: {correct_answer}"
                )

            st.write(
                f"Explanation: {question['explanation']}"
            )


    # --------------------------------------------------
    # DOWNLOAD CSV
    # --------------------------------------------------

    st.markdown("---")

    st.header("Download Questions")

    csv_data = []

    for index, question in enumerate(questions):

        csv_data.append(
            {
                "Question Number": index + 1,
                "Question": question["question"],
                "Option A": question["options"]["A"],
                "Option B": question["options"]["B"],
                "Option C": question["options"]["C"],
                "Option D": question["options"]["D"],
                "Correct Answer": question["answer"],
                "Explanation": question["explanation"]
            }
        )


    df = pd.DataFrame(csv_data)

    csv_file = df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="Download MCQs as CSV",
        data=csv_file,
        file_name="generated_mcqs.csv",
        mime="text/csv",
        use_container_width=True
    )


# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

else:

    st.info(
        "Enter your study material above and click "
        "**Generate MCQs** to get started."
    )