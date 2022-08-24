"""empty message

Revision ID: ad89018e7717
Revises: 589f21b890c6
Create Date: 2022-08-19 14:51:39.828080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad89018e7717'
down_revision = '589f21b890c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('catagory', sa.String(length=50), nullable=True))
    op.drop_constraint('project_ibfk_4', 'project', type_='foreignkey')
    op.create_foreign_key(None, 'project', 'printobject', ['objectfk'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.create_foreign_key('project_ibfk_4', 'project', 'printobject', ['objectfk'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('project', 'catagory')
    # ### end Alembic commands ###