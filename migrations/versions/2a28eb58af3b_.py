"""empty message

Revision ID: 2a28eb58af3b
Revises: a1f32666e00a
Create Date: 2022-08-10 12:36:52.178301

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2a28eb58af3b'
down_revision = 'a1f32666e00a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('settings_log')
    op.drop_constraint('address_ibfk_1', 'address', type_='foreignkey')
    op.create_foreign_key(None, 'address', 'people', ['peoplefk'], ['id'])
    op.drop_constraint('people_ibfk_1', 'people', type_='foreignkey')
    op.drop_constraint('people_ibfk_2', 'people', type_='foreignkey')
    op.create_foreign_key(None, 'people', 'address', ['ship_addressfk'], ['id'])
    op.create_foreign_key(None, 'people', 'address', ['main_addressfk'], ['id'])
    op.add_column('type', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('type', 'active')
    op.drop_constraint(None, 'people', type_='foreignkey')
    op.drop_constraint(None, 'people', type_='foreignkey')
    op.create_foreign_key('people_ibfk_2', 'people', 'address', ['ship_addressfk'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('people_ibfk_1', 'people', 'address', ['main_addressfk'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'address', type_='foreignkey')
    op.create_foreign_key('address_ibfk_1', 'address', 'people', ['peoplefk'], ['id'], onupdate='SET NULL', ondelete='SET NULL')
    op.create_table('settings_log',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('settingsID', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('old_row_data', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False),
    sa.Column('new_row_data', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False),
    sa.Column('type', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('timestamp', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp()'), nullable=False),
    sa.Column('created_by', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###