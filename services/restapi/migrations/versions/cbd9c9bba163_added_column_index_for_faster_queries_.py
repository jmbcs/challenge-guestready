"""Added column index for faster queries in requested filtering fields

Revision ID: cbd9c9bba163
Revises: 50bb26d08e71
Create Date: 2024-07-03 12:06:59.762271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbd9c9bba163'
down_revision: Union[str, None] = '50bb26d08e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('developer_name_key', 'developer', type_='unique')
    op.create_index(op.f('ix_developer_name'), 'developer', ['name'], unique=True)
    op.create_index(op.f('ix_game_genre'), 'game', ['genre'], unique=False)
    op.create_index(op.f('ix_game_release_date'), 'game', ['release_date'], unique=False)
    op.create_index(op.f('ix_game_title'), 'game', ['title'], unique=False)
    op.drop_constraint('platform_name_key', 'platform', type_='unique')
    op.create_index(op.f('ix_platform_name'), 'platform', ['name'], unique=True)
    op.drop_constraint('publisher_name_key', 'publisher', type_='unique')
    op.create_index(op.f('ix_publisher_name'), 'publisher', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_publisher_name'), table_name='publisher')
    op.create_unique_constraint('publisher_name_key', 'publisher', ['name'])
    op.drop_index(op.f('ix_platform_name'), table_name='platform')
    op.create_unique_constraint('platform_name_key', 'platform', ['name'])
    op.drop_index(op.f('ix_game_title'), table_name='game')
    op.drop_index(op.f('ix_game_release_date'), table_name='game')
    op.drop_index(op.f('ix_game_genre'), table_name='game')
    op.drop_index(op.f('ix_developer_name'), table_name='developer')
    op.create_unique_constraint('developer_name_key', 'developer', ['name'])
    # ### end Alembic commands ###