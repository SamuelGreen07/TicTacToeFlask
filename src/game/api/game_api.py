from flask import request

from marshmallow import ValidationError

from auth.services.basic_auth import auth
from game.serializers.game_serializer import StartGameSerializer, BoardBeautySerializer, MoveRequestSerializer
from game.services.game_service import game_service


@auth.login_required
async def start_game():
    game = await game_service.start_game(request.user)
    if game is None:
        return {'error': "somth wrong"}, 400
    response_serializer = StartGameSerializer()
    data = response_serializer.dump(game)
    return data, 200


@auth.login_required
async def show_board(game_id):
    game = await game_service.get_game(game_id)
    if game is None:
        return {'error': "somth wrong"}, 400
    response_serializer = BoardBeautySerializer()
    data = response_serializer.dump(game)
    return data, 200


@auth.login_required
async def make_move(game_id):
    try:
        move_serializer = MoveRequestSerializer()
        data = move_serializer.load(request.get_json())

    except ValidationError as err:
        return {'error': err.messages}, 400

    game = await game_service.get_game(game_id)
    if game is None:
        return {'error': "somth wrong"}, 400

    if game.player_turn != request.user.id:
        return {'error': 'Turn of second player, just wait a minute or still wait a minute'}, 400

    move = await game_service.make_move(request.user, data['row_id'], game_id)
    if move is None:
        return {'error': "somth wrong"}, 400
    if move is False:
        return {'error': "Row busy"}, 400

    return {}, 201
