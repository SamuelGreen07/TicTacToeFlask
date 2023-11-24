from app import app
from game.urls import game_blueprint
from users.urls import user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(game_blueprint, url_prefix='/game')
