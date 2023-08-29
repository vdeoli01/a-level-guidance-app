"""Initial migration

Revision ID: 0fab20d92393
Revises: 
Create Date: 2023-08-29 11:09:00.350960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fab20d92393'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('slot',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('advisor_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('subject',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('salt', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('question',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_str', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('quiz_attempt',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz_attempt')
    op.drop_table('question')
    op.drop_table('user')
    op.drop_table('subject')
    op.drop_table('slot')
    op.drop_table('quiz')
    # ### end Alembic commands ###
