from flask import Flask
from main.views import main


app = Flask(__name__)
app.secret_key = 'The Python Language'
app.register_blueprint(main)


if __name__ == '__main__':
    app.run()