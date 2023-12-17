"""Drop _alembic_tmp_customer table

Revision ID: d589cbc553f2
Revises: 09f2109abd36
Create Date: 2023-12-14 21:51:24.114087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd589cbc553f2'
down_revision = '09f2109abd36'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('_alembic_tmp_customer')


def downgrade():
    op.drop_table('_alembic_tmp_customer')
