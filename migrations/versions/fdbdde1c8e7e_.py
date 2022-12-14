"""empty message

Revision ID: fdbdde1c8e7e
Revises: 
Create Date: 2022-11-03 15:07:59.159348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdbdde1c8e7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('handbook', sa.String(length=300), nullable=True))
    op.add_column('events', sa.Column('file1', sa.String(length=300), nullable=True))
    op.add_column('events', sa.Column('file2', sa.String(length=300), nullable=True))
    op.add_column('events', sa.Column('file3', sa.String(length=300), nullable=True))
    op.add_column('events', sa.Column('file4', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'file4')
    op.drop_column('events', 'file3')
    op.drop_column('events', 'file2')
    op.drop_column('events', 'file1')
    op.drop_column('events', 'handbook')
    # ### end Alembic commands ###
