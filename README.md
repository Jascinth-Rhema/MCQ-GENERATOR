# AI MCQ Generator

An AI-powered Multiple Choice Question Generator that creates meaningful quiz questions from a given topic or study material. The application uses the Groq API with an AI language model to understand the input, generate four-option MCQs, provide correct answers and explanations, and calculate quiz scores through an interactive Streamlit interface.

## Live Application

[Open AI MCQ Generator](https://mcq-generator.streamlit.app/)

## GitHub Repository

[View Source Code](https://github.com/Jascinth-Rhema/MCQ-GENERATOR)

## Features

- AI-powered MCQ generation
- Topic-based question generation
- Study-material-based question generation
- Four options for every question
- Easy, Medium, and Hard difficulty levels
- Custom number of questions
- Correct answer identification
- Explanation for each answer
- Duplicate question removal
- Question validation
- Interactive quiz interface
- Automatic score calculation
- Answer review after quiz submission
- Secure API key handling
- Streamlit-based user interface

## Technologies Used

- Python
- Streamlit
- Groq API
- OpenAI GPT-OSS-20B
- Python Dotenv
- Pandas
- Git and GitHub

## How It Works

```text
User
  |
  v
Streamlit Interface
  |
  v
Topic / Study Material
  |
  v
Text Processing
  |
  v
Groq AI Model
  |
  v
MCQ Generation
  |
  v
Question Validation
  |
  v
Duplicate Removal
  |
  v
Quiz Display
  |
  v
User Answers
  |
  v
Score Calculation
  |
  v
Answer Review
```

The user enters a topic or study material through the Streamlit interface. The input is cleaned and prepared before being sent to the Groq API. The AI model generates meaningful multiple-choice questions with four options, a correct answer, and an explanation.

The generated questions are validated to ensure that they contain the required structure. Duplicate questions are removed before the quiz is displayed to the user.

After answering all questions, the user can submit the quiz to view the score, correct answers, wrong answers, and explanations.

## Question Generation

The application supports two types of input.

### Topic-Based Input

Users can enter a simple topic such as:

```text
RAG
```

The AI model understands the topic and generates relevant questions based on the concept.

### Study Material Input

Users can also provide detailed study material such as:

```text
RAG (Retrieval-Augmented Generation) combines
information retrieval with language generation.
It retrieves relevant information from a knowledge
base and provides the retrieved information to a
language model to generate a more accurate response.
```

The AI model uses the provided material to generate questions related to the given content.

## Quiz Features

Each generated question contains:

- Question
- Option A
- Option B
- Option C
- Option D
- Correct answer
- Explanation

The user selects an answer for each question and submits the quiz.

The application then calculates:

- Correct answers
- Wrong answers
- Total questions
- Percentage score

## Project Structure

```text
MCQ-GENERATOR/
│
├── app.py
├── mcq_generator.py
├── text_processor.py
├── validator.py
├── quiz_engine.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `app.py`

Contains the main Streamlit application. It handles the user interface, quiz settings, study material input, question display, quiz submission, and result display.

### `mcq_generator.py`

Handles the Groq API connection and AI-based MCQ generation. It processes the AI response and converts it into a structured question format.

### `text_processor.py`

Cleans and prepares the user-provided study material before it is passed to the AI model.

### `validator.py`

Validates the generated MCQs and removes duplicate questions.

### `quiz_engine.py`

Handles quiz evaluation and calculates the final score, number of correct answers, wrong answers, and percentage.

### `requirements.txt`

Contains the Python packages required to run the application.

## Installation

Clone the repository:

```bash
git clone https://github.com/Jascinth-Rhema/MCQ-GENERATOR.git
cd MCQ-GENERATOR
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

The API key is required to communicate with the Groq API.

The `.env` file should not be uploaded to GitHub. It should be included in `.gitignore`.

## Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in the browser.

Enter a topic or study material, select the number of questions and difficulty level, and click **Generate MCQs**.

## Deployment

The application can be deployed using Streamlit Community Cloud.

For deployment:

1. Push the project to GitHub.
2. Connect the GitHub repository to Streamlit Community Cloud.
3. Select the `main` branch.
4. Set `app.py` as the main file.
5. Add the `GROQ_API_KEY` using Streamlit Secrets.
6. Deploy the application.

For Streamlit deployment, the API key should be stored securely using:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

The API key should never be committed to the GitHub repository.

## AI Model

The application uses the Groq API to access the AI model:

```text
openai/gpt-oss-20b
```

The model is used to understand the user's topic or study material and generate structured multiple-choice questions.

The application requests the AI response in JSON format so that the generated questions can be validated and displayed consistently.

## Question Validation

Generated questions are validated before being displayed.

The application checks that:

- A question is present
- Four options are available
- Options are labeled A, B, C, and D
- A valid answer is provided
- The question contains valid content

Invalid questions are ignored.

Duplicate questions are also removed before displaying the quiz.

## Score Calculation

The quiz engine compares the user's selected answers with the correct answers generated by the AI.

The score is calculated using:

```text
Percentage = (Correct Answers / Total Questions) × 100
```

The final result displays the user's correct answers, wrong answers, and percentage score.

## Security

The Groq API key is stored using environment variables during local development.

```env
GROQ_API_KEY=your_groq_api_key
```

The `.env` file is excluded from GitHub using `.gitignore`.

For Streamlit deployment, the API key is stored securely using Streamlit Secrets.

The API key should never be included directly in the source code or publicly shared.

## Future Enhancements

- PDF and document upload
- Generate questions directly from uploaded notes
- Subject and topic categories
- Timed quizzes
- Question difficulty analysis
- Quiz history
- Student performance tracking
- Export quizzes as PDF
- Download generated questions
- User authentication
- Database integration
- Personalized quiz generation
- Multi-language question generation

## Conclusion

The AI MCQ Generator demonstrates how artificial intelligence can be used to automate quiz creation and support interactive learning. By combining a language model with text processing, question validation, and a Streamlit interface, the application provides an easy way to generate and practice multiple-choice questions from different topics and study materials.

## Author

**Jascinth Rhema R**

GitHub: https://github.com/Jascinth-Rhema
