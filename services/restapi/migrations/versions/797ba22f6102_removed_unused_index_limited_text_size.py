"""Removed unused index, limited text size

Revision ID: 797ba22f6102
Revises: cbd9c9bba163
Create Date: 2024-07-07 12:24:24.102132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '797ba22f6102'
down_revision: Union[str, None] = 'cbd9c9bba163'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_game_title', table_name='game')
    op.drop_index('ix_publisher_name', table_name='publisher')
    op.create_unique_constraint(None, 'publisher', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'publisher', type_='unique')
    op.create_index('ix_publisher_name', 'publisher', ['name'], unique=True)
    op.create_index('ix_game_title', 'game', ['title'], unique=False)
    # ### end Alembic commands ###
