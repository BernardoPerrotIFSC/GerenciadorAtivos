"""empty message

Revision ID: a19169adb425
Revises: 088c4ec229f8
Create Date: 2023-12-03 15:04:51.886171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a19169adb425'
down_revision = '088c4ec229f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hist_cripto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantidade', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hist_cripto', schema=None) as batch_op:
        batch_op.drop_column('quantidade')

    # ### end Alembic commands ###