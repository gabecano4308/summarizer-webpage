from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app
)
from transformers import pipeline
from . import db


bp = Blueprint('summarizer', __name__)

# Load model once on startup
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize(text):
    '''
    Run the text through the pipeline, returning the summary text
    '''
    config = current_app.config

    # run text through summarizer pipeline
    summary = summarizer(text, 
                         max_length=config['MAX_LEN'], 
                         min_length=config['MIN_LEN'], 
                         do_sample=False)

    # return summary
    return summary[0]["summary_text"]


@bp.route("/", methods=["GET", "POST"])
def index():
    '''
    GET: grab chat history from DB and insert into HTML template before rendering.
    POST: same as GET, except add the new prompt/summary to the DB first.
    '''
    llmdb = db.get_db()
    
    if request.method == "POST":

        # grab prompt from request
        prompt = request.form.get("prompt", "")

        # get summary of the prompt
        response = summarize(prompt)

        # add prompt and summary to db
        llmdb.execute(
            'INSERT INTO chat_entries (prompt, response)'
            ' VALUES (?, ?)',
            (prompt, response)
        )
        llmdb.commit()
    
    # grab chat history from DB to insert into the webpage
    chat_history = llmdb.execute(
         'SELECT prompt, response FROM chat_entries ORDER BY id DESC'
    ).fetchall()

    return render_template("form.html", chat_history=chat_history)


@bp.route("/clear", methods=["POST"])
def clear():
    '''
    Delete entries from the chat_entries table and call GET on homepage
    '''
    llmdb = db.get_db()
    llmdb.execute("DELETE FROM chat_entries")
    llmdb.commit()
    return redirect(url_for("summarizer.index"))
