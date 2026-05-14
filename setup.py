
from setuptools import setup, find_packages

setup(
    name="mcqgenerator",
    version="1.0.0",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-groq",
        "python-docx",
        "PyPDF2",
        "pandas",
        "python-dotenv"
    ]
)
