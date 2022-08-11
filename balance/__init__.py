from flask import Flask

apikey ="a0d6923fb53446d583e72dc7a65f1037"

app = Flask(__name__)
app.config.from_prefixed_env()
