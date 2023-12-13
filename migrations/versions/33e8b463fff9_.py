"""empty message

Revision ID: 33e8b463fff9
Revises: 9d54294c272d
Create Date: 2023-11-08 22:20:01.400090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33e8b463fff9'
down_revision = '9d54294c272d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carteira_acoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('valor_atual_total', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('lucro_prejuizo', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))
        batch_op.drop_column('valor_atual_pago')

    with op.batch_alter_table('carteira_cripto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lucro_prejuizo', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carteira_cripto', schema=None) as batch_op:
        batch_op.drop_column('status')
        batch_op.drop_column('lucro_prejuizo')

    with op.batch_alter_table('carteira_acoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('valor_atual_pago', sa.FLOAT(), nullable=True))
        batch_op.drop_column('status')
        batch_op.drop_column('lucro_prejuizo')
        batch_op.drop_column('valor_atual_total')

    # ### end Alembic commands ###