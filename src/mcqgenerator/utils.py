import PyPDF2
import docx
import io
import json


def read_file(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
            return "\n".join(text)
        except Exception:
            raise ValueError(
                "Unable to read this PDF. "
                "Please upload a text-based PDF or use TXT/DOCX."
            )

    if filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError("Unsupported file format")


def get_table_data(quiz_json):
    try:
        quiz_dict = json.loads(quiz_json)
    except Exception:
        return None

    table_data = []

    for qno, q in quiz_dict.items():

        if not isinstance(q, dict):
            continue

        options = q.get("options", {})

        row = {
            "Question": q.get("question", "—"),
            "A": options.get("a", "—"),
            "B": options.get("b", "—"),
            "C": options.get("c", "—"),
            "D": options.get("d", "—"),
            "Correct": q.get("correct", "—")
        }

        table_data.append(row)

    return table_data
