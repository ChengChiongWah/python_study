from flask import Flask
from routes_user import registers

app = Flask(__name__)


app.register_blueprint(registers, url_prefix='/registers')


@app.route('/')
def index():
    return "index page"

if __name__ == '__main__':
    app.run()