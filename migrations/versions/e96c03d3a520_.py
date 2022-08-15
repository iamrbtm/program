"""empty message

Revision ID: e96c03d3a520
Revises: 1a7c93b8c040
Create Date: 2022-08-14 00:32:37.557629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e96c03d3a520'
down_revision = '1a7c93b8c040'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('events', sa.Column('end_date', sa.Date(), nullable=True))
    op.add_column('events', sa.Column('start_time', sa.Time(), nullable=True))
    op.add_column('events', sa.Column('end_time', sa.Time(), nullable=True))
    op.add_column('events', sa.Column('location', sa.String(length=100), nullable=True))
    op.add_column('events', sa.Column('title', sa.String(length=50), nullable=True))
    op.add_column('events', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'description')
    op.drop_column('events', 'title')
    op.drop_column('events', 'location')
    op.drop_column('events', 'end_time')
    op.drop_column('events', 'start_time')
    op.drop_column('events', 'end_date')
    op.drop_column('events', 'start_date')
    # ### end Alembic commands ###