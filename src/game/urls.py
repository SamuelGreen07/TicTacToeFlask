from flask import Blueprint

from game.api.game_api import start_game, show_board, make_move

game_blueprint = Blueprint('game_blueprint', __name__ ,)

game_blueprint.add_url_rule('/start_game/', 'start_game', start_game, methods=['POST'])
game_blueprint.add_url_rule('<game_id>/make_move/', 'make_move', make_move, methods=['POST'])
game_blueprint.add_url_rule('<game_id>/show_board/', 'show_board', show_board, methods=['GET'])
