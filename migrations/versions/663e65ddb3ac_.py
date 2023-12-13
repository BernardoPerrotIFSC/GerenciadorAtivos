"""empty message

Revision ID: 663e65ddb3ac
Revises: e2c6903e182a
Create Date: 2023-11-27 00:25:37.293859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '663e65ddb3ac'
down_revision = 'e2c6903e182a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carteira_acoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_update', sa.Date(), nullable=True))
        batch_op.drop_column('last_udpate')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carteira_acoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_udpate', sa.DATE(), nullable=True))
        batch_op.drop_column('last_update')

    # ### end Alembic commands ###