"""empty message

Revision ID: b98a94471320
Revises: 93c0b620e1b7
Create Date: 2022-11-01 21:44:46.743990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b98a94471320'
down_revision = '93c0b620e1b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('designhours', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'designhours')
    # ### end Alembic commands ###
