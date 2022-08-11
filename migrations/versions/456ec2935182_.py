"""empty message

Revision ID: 456ec2935182
Revises: 2a28eb58af3b
Create Date: 2022-08-10 21:25:06.159860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '456ec2935182'
down_revision = '2a28eb58af3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('filament', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('filament', 'active')
    # ### end Alembic commands ###
