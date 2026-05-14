
# 📚 MCQ Generator Application with Langchain

[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

## 📝 Description

The MCQ Generator is a Python application that generates multiple-choice questions (MCQs) using the powerful Langchain library. It allows users to create customized MCQs based on input text, making it suitable for various subjects and complexity levels. The application provides a user-friendly interface built with Streamlit, enabling easy interaction and seamless MCQ generation.

## 🎯 Features

- 📂 File Upload: Users can upload PDF or text files containing the input text for MCQ generation.
- 🎛️ Customization: Specify the number of MCQs, subject, and complexity level of questions.
- 🧠 Intelligent Generation: Leverages the Langchain library and OpenAI API for advanced natural language processing.
- 📊 Review Generated MCQs: View the generated MCQs in a table format along with a review in the Streamlit app.
- 📝 Logging: Application events are logged for easy tracking and debugging.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/AkshaySatasiya/mcqgen.git
   cd mcqgen
   ```

2. Create a virtual environment (optional but recommended):
   

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the API key:
   - Obtain an API key from OpenAI.
   - Create a `.env` file in the project root directory.
   - Add the following line to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## 🏃‍♂️ Usage

1. Run the Streamlit application:
   ```
   streamlit run StreamlitAPP.py
   ```

2. Access the application in your web browser at `http://localhost:8501`.

3. Upload a PDF or text file containing the input text for MCQ generation.

4. Specify the desired number of MCQs, subject, and complexity level.

5. Click the "Create MCQs" button to generate the MCQs.

6. Review the generated MCQs in the Streamlit app.

## 📁 File Descriptions

- `StreamlitAPP.py`: Main script containing the Streamlit application for the MCQ Generator.
- `mcqgenerator.py`: Script handling the generation and evaluation of MCQs using Langchain.
- `logger.py`: Logging setup to record application events.
- `utils.py`: Utility functions for reading files and extracting table data from the generated MCQs.
- `requirements.txt`: List of required Python packages for the application.

## 📝 Logging

Application events are logged in the `logs` directory. Each log file is timestamped for easy reference and debugging.

## 🙌 Acknowledgments

The MCQ Generator application utilizes the [Langchain](https://github.com/hwchase17/langchain) library and [OpenAI API](https://openai.com/) for natural language processing. We express our gratitude to the developers and contributors of these amazing tools.

## 🤝 Contribution

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. Make sure to follow the [contribution guidelines](CONTRIBUTING.md) when contributing to this project.

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).



Feel free to reach out for any queries or support regarding this project. Happy coding! 🚀

# MCQ-Generator-using-LLMs
An intelligent multilingual MCQ generation system combining ontology, machine learning (SVM, KNN, Decision Tree), and LLMs to generate Bloom’s Taxonomy-based questions with meaningful distractors using NLP, embeddings, ensemble learning, semantic similarity, and cross-lingual generation techniques.
