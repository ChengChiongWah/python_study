from flask import Flask
import time

app = Flask(__name__)

from messages import messages

app.register_blueprint(messages, url_prefix='/messages')


@app.route("/")
def main():
    return "hello, wold!"


if __name__ == '__main__':
    app.run()