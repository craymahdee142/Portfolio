"""Added fullname to track invoice activities

Revision ID: d1e7382357e7
Revises: d589cbc553f2
Create Date: 2023-12-14 22:04:00.383810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1e7382357e7'
down_revision = 'd589cbc553f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customer_name', sa.String(length=100), nullable=True))
        batch_op.drop_column('name')

    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_fullname', sa.String(length=80), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.drop_column('user_fullname')

    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_column('customer_name')

    # ### end Alembic commands ###