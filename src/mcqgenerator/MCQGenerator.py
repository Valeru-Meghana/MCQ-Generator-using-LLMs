import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load .env
load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=GROQ_API_KEY
)

def generate_evaluate_chain(inputs):
    """
    inputs dict contains:
    - text
    - number
    - subject
    - tone (Bloom level)
    - language
    """

    subject = inputs.get("subject", "General")
    text = inputs.get("text", "")
    number = inputs.get("number", 10)
    tone = inputs.get("tone", "general")
    language = inputs.get("language", "English")

    prompt = f"""
You are an expert exam question generator and professional translator.

SUBJECT (STRICT): {subject}
DIFFICULTY (BLOOM LEVEL): {tone}
TARGET LANGUAGE: {language}

CONTEXT / USER INPUT:
{text}

TASK:
Generate exactly {number} MCQs STRICTLY related to the SUBJECT above.
You MUST write the question text and the options strictly in the TARGET LANGUAGE ({language}).

MANDATORY RULES:
- ALL questions MUST be about {subject}
- Follow the difficulty level: {tone}
- CRITICAL LANGUAGE RULE: The text for the questions and options MUST be written in {language}. For example, if {language} is Hindi, use Hindi script. If Telugu, use Telugu. If Tamil, use Tamil. Do NOT use English for the content unless {language} is English.
- The JSON keys ("1", "question", "options", "a", "b", "c", "d", "correct") MUST remain in English.
- Write clear, grammatically correct, and semantically meaningful questions.
- AVOID mixing WH-questions (why, what, how) with fill-in-the-blank statements (_____). Formulate either a direct WH-question OR a proper fill-in-the-blank statement, but not a confusing mixture of both. Ensure the question makes logical sense.

OTHER RULES:
- Exactly 4 options (a, b, c, d)
- Only ONE correct answer
- No repetition
- No general knowledge outside the subject
- Output ONLY valid JSON
- No explanations, no extra text

JSON FORMAT EXAMPLE:
{{
  "1": {{
    "question": "Question written in {language}",
    "options": {{
      "a": "Option A in {language}",
      "b": "Option B in {language}",
      "c": "Option C in {language}",
      "d": "Option D in {language}"
    }},
    "correct": "a"
  }}
}}
"""

    response = llm.invoke(prompt)

    return {
        "quiz": response.content
    }
