""" Added relationship to the invoice and customer

Revision ID: 15f49afd4442
Revises: ae18d8650a0b
Create Date: 2023-12-12 21:26:39.388938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15f49afd4442'
down_revision = 'ae18d8650a0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_invoice_customer', 'customer', ['customer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.drop_constraint('fk_invoice_customer', type_='foreignkey')
        batch_op.drop_column('customer_id')

    # ### end Alembic commands ###
