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
            session.close()
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
                        await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

        return True


game_service = GameService()
