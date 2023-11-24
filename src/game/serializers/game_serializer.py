from marshmallow import Schema, fields, post_dump
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Email, Length, NumberRange

from settings import settings


class MoveRequestSerializer(Schema):
    row_id = fields.Integer(required=True, validate=from_wtforms([NumberRange(min=1, max=9)], locales=settings.locales))


class StartGameSerializer(Schema):
    id = fields.Str(required=True)


class BoardBeautySerializer(Schema):
    board = fields.Raw(required=True)

    @post_dump
    def beautify_board(self, data: dict, **kwargs):
        symbols = {'p1': 'X', 'p2': 'O', None: ' '}
        board_str = ""
        for i in range(1, 10):

            board_str += symbols.get(data['board'][str(i)], ' ')

            if i % 3 == 0:
                if i != 9:
                    board_str += '\n---------\n'
            else:
                board_str += ' | '
        return board_str
