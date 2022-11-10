"""empty message

Revision ID: 4592e0fdfe9f
Revises: d482273e01be
Create Date: 2022-11-10 02:25:52.099359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4592e0fdfe9f'
down_revision = 'd482273e01be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sales', sa.Column('balance', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sales', 'balance')
    # ### end Alembic commands ###