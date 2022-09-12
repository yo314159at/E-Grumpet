# Very hacky website that calls the p̶o̶l̶i̶c̶e̶ main bot
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "E-Grumpet is online!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()