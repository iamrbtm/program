"""empty message

Revision ID: d482273e01be
Revises: 395b37e727f4
Create Date: 2022-11-10 01:20:38.217345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd482273e01be'
down_revision = '395b37e727f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sales', sa.Column('cash', sa.Float(), nullable=True))
    op.add_column('sales', sa.Column('check', sa.Float(), nullable=True))
    op.add_column('sales', sa.Column('checknum', sa.Integer(), nullable=True))
    op.add_column('sales', sa.Column('card', sa.Float(), nullable=True))
    op.add_column('sales', sa.Column('account', sa.Float(), nullable=True))
    op.add_column('sales', sa.Column('other', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sales', 'other')
    op.drop_column('sales', 'account')
    op.drop_column('sales', 'card')
    op.drop_column('sales', 'checknum')
    op.drop_column('sales', 'check')
    op.drop_column('sales', 'cash')
    # ### end Alembic commands ###
