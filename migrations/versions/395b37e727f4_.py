"""empty message

Revision ID: 395b37e727f4
Revises: a49b58e370bc
Create Date: 2022-11-03 18:34:03.666857

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '395b37e727f4'
down_revision = 'a49b58e370bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_inventory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_inventory',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('eventid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('projectid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('quantity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['eventid'], ['events.id'], name='event_inventory_ibfk_1'),
    sa.ForeignKeyConstraint(['projectid'], ['project.id'], name='event_inventory_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
