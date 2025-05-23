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

Clone and enter the repo:

```bash
git clone https://github.com/gabecano4308/summarizer-webpage.git

cd summarizer-webpage
```

Create a virtual environment using python 3.11:

```bash
conda create --name llm-summarizer python=3.11
conda activate llm-summarizer
```

Install package/dependencies from pyproject.toml. Once the package is installed,
the ensuing commands can be run from any local directory:
```bash
# use python -m build if you want a permanent wheel in a dist folder
pip install .
```

Initialize the sql database that saves chat history. This only needs to be run once:
```bash
# should echo, "Initialized the database"
flask --app llm_app init-db
```

Run the application:
```bash
flask --app llm_app run
```

---

## 🚁 Deployment
To deploy this on the internet, check out Flask's documentation on deployment [here](https://flask.palletsprojects.com/en/stable/deploying/).

---

## ⛔️ Limitations and Future Enhancements

- The LLM currently being used is open source with no API key needed. This is good for running locally, but is slow in practice without a GPU or other optimization techniques (summaries can take up to a minute). 
    - Add support for paid hosted models and their API keys
    - Add support for GPU/CPU device configuration.
- The LLM only summarizes. 
    - Incorporate models that can answer follow-up questions to summarizations.ee 

