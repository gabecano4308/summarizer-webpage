DROP TABLE IF EXISTS chat_entries;

CREATE TABLE chat_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL
);