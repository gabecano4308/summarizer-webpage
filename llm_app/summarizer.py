from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app
)
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from . import db


bp = Blueprint('summarizer', __name__)

# Load model once on startup
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")


def summarize(text):
    config = current_app.config
    inputs = tokenizer(text, return_tensors="pt", max_length=config['MAX_LEN'], 
                       truncation=True, padding="max_length")

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    outputs = model.generate(input_ids, attention_mask=attention_mask, 
                             max_length=config['MAX_OUTPUT_LEN'], 
                             num_beams=config['NUM_BEAMS'],
                             repetition_penalty=config['REPETITION_PENALTY'],
                             no_repeat_ngram_size=config['NO_REPEAT_NGRAM_SIZE'],
                             early_stopping=True)
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary


@bp.route("/", methods=["GET", "POST"])
def index():

    llmdb = db.get_db()
    
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        response = summarize(prompt)

        # add prompt and response to db
        llmdb.execute(
            'INSERT INTO chat_entries (prompt, response)'
            ' VALUES (?, ?)',
            (prompt, response)
        )
        llmdb.commit()
    
    chat_history = llmdb.execute(
         'SELECT prompt, response FROM chat_entries ORDER BY id DESC'
    ).fetchall()

    return render_template("form.html", chat_history=chat_history)


@bp.route("/clear", methods=["POST"])
def clear():
    llmdb = db.get_db()
    llmdb.execute("DELETE FROM chat_entries")
    llmdb.commit()
    return redirect(url_for("summarizer.index"))
