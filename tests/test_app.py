import os
import tempfile
import re
import pytest
from llm_app import create_app
from llm_app.db import init_db

#TODO: let know in blog that this app/client/runner structure is taken from tutorial
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True,
                     'DATABASE': db_path})
    
    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_get_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data  # crude check: form is rendered


def test_post_prompt(client):
    response = client.post("/", data={"prompt": "What is AI?"})
    print(response)
    print(response.data)
    assert response.status_code == 200

    html = response.data.decode("utf-8") # byte to string
    match = re.search(r"Bot:</strong>(.*?)</div>", html, re.DOTALL)
    
    assert "What is AI?" in html
    assert match is not None, "Bot response not found"
    assert match.group(1).strip() != "", "Bot response is empty"
    

def test_clear_history(client):
    # Insert a prompt
    client.post("/", data={"prompt": "Clear me"})
    # Clear all
    response = client.post("/clear")
    assert response.status_code == 302  # Redirect
    followup = client.get("/")
    assert b"Clear me" not in followup.data


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('llm_app.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called