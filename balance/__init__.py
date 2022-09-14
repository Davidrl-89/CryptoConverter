from flask import Flask

apikey1 = "F1542F81-6D87-4CCF-9891-0E0F7DD465AD"
apikey1 = "FA9C7633-A868-4913-A78C-FA6341D9F6DF"
apikey = "04ECB8E0-609D-43D0-8515-18E5DE55FE41"

app = Flask(__name__)
app.config.from_prefixed_env()

monedas_disponibles = ["BTC", "EUR", "ETH", "LINK", "LUNA"]
