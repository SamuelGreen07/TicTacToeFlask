from sqlalchemy import select, and_

from app import db
from auth.services.basic_auth import security_service
from game.constants import GameStatus, GAME_BOARD
from game.models import Game, PlayersMoves
from users.models import User


class GameService:

    async def start_game(self, user):
        async with db.get_session() as session:
            # start transaction
            async with session.begin():
                query = select(Game).where(
                    and_(
                        Game.status == GameStatus.STARTING,
                        Game.player_1 != user.id
                    )
                ).with_for_update()

                result = await session.execute(query)
                game = result.scalars().first()

                if game is not None:
                    game.player_2 = user.id
                    game.status = GameStatus.IN_PROGRESS
                    game.board = GAME_BOARD
                    await session.commit()

                else:
                    game = Game(
                        player_1=user.id,
                        status=GameStatus.STARTING,
                        player_turn=user.id,

                    )
                    session.add(game)
                    await session.commit()

        return game

    async def get_game(self, game_id):
        async with db.get_session() as session:
            query = select(Game).where(Game.id == game_id)
            result = await session.execute(query)
            game = result.scalars().first()
        return game

    async def make_move(self, user, row_id, game_id):
        async with db.get_session() as session:
            # start transaction
            try:
                async with session.begin():
                    query = select(Game).where(Game.id == game_id, ).with_for_update()
                    result = await session.execute(query)
                    game = result.scalars().first()

                    if game is not None:
                        if game.player_turn == game.player_1:
                            player = 'p1'
                            game.player_turn = game.player_2
                        else:
                            player = 'p2'
                            game.player_turn = game.player_1

                        board = dict(game.board)
                        if board[str(row_id)] is not None:
                            await session.rollback()
                            return False

                        board[str(row_id)] = player
                        game.board = board

                        move = PlayersMoves(
                            player=user.id,
                            row=row_id,
                            game_id=game_id,

                        )
                        session.add(move)

                        winner, is_game_over = self.check_tic_tac_toe(board)
                        if is_game_over:
                            game.winner = user.id
                            game.status = GameStatus.FINISHED
                        await session.commit()

            except Exception as e:
                await session.rollback()
                raise e

        return True, is_game_over

    def check_tic_tac_toe(self, board):
        def convert_to_2d(board):
            return [[board[str(i * 3 + j + 1)] for j in range(3)] for i in range(3)]

        def is_winner(board, player):
            for i in range(3):
                if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                    return True
            if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
                return True
            return False

        def is_draw(board):
            return all(cell in ['p1', 'p2'] for row in board for cell in row)

        board_2d = convert_to_2d(board)
        if is_winner(board_2d, 'p1'):
            return 'p1', True
        elif is_winner(board_2d, 'p2'):
            return 'p2', True
        elif is_draw(board_2d):
            return None, True
        else:
            return None, False


game_service = GameService()
