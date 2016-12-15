from flask import Flask
from main.views import main
from recipe.views import recipe


app = Flask(__name__)
app.secret_key = 'The Python Language'
app.register_blueprint(main)
app.register_blueprint(recipe, url_prefix='/recipe')


if __name__ == '__main__':
    app.run()
