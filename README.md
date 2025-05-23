# 🧠 LLM Summarizer Web App

A lightweight Flask web app that uses a large language model (LLM) to summarize text input. It saves user prompts and generated summaries to a local SQLite database and includes basic UI and testing functionality.

---

## 🚀 Features

- Summarizes user-submitted text using the `bart-large-cnn` model via Hugging Face Transformers
- Saves prompt/response pairs to a SQLite database
- Allows users to clear the conversation history
- Configurable via environment variables or `config.py`
- Includes a pytest unit test script (`test_app.py`)
- Includes a pyproject.toml for deploying with `pip` and creating wheels

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/gabecano4308/summarizer-webpage.git

cd summarizer-webpage
```

Create a virtual environment

```bash
# For Max/Linux:
python -m venv .venv
source .venv/bin/activate
```
```bash
# For Windows Powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
```bash
# For Windows (cmd.exe):
python -m venv .venv
.venv\Scripts\Activate.ps1
```


