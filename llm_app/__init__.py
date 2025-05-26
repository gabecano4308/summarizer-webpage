import os
from flask import Flask
from . import db

def create_app(test_config=None):
    '''
    - Creates and configures the Flask app.
    - Loads default and optional test configuration.
    - Ensures the instance folder exists.
    - Registers the summarizer blueprint and initializes the database.

    Args:
        test_config (dict, optional): Configuration dictionary used during testing.
                                       Overrides default and file-based settings.

    Returns:
        Flask: The configured Flask application.
    '''
    app = Flask(__name__)
    
    app.config.from_mapping(
    SECRET_KEY="dev",   # will get replaced with secret in conf if not testing
    DATABASE=os.path.join(app.instance_path, "llm_sumry.sqlite"),
    MAX_LEN=200,       # the rest of these are params for LLM model
    MIN_LEN = 30,
    MAX_OUTPUT_LEN=200,
    NUM_BEAMS=4,
    REPETITION_PENALTY=1.2,
    NO_REPEAT_NGRAM_SIZE=3)

    if test_config:
        # running tests, pass test config in
        app.config.from_mapping(test_config)
    else:
        # pass actual config in (contains secret key)
        #--------------------------------------------------------#
        # run python -c 'import secrets; print(secrets.token_hex())'
        # and paste this into config.py: SECRET_KEY=<output_of_above>
        app.config.from_pyfile("config.py", silent=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import summarizer
    app.register_blueprint(summarizer.bp)

    db.init_app(app)

    return app