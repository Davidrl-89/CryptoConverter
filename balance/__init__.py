from flask import Flask

apikey = "F1542F81-6D87-4CCF-9891-0E0F7DD465AD"

app = Flask(__name__)
app.config.from_prefixed_env()
