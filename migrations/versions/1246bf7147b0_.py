"""empty message

Revision ID: 1246bf7147b0
Revises: d1e602c26f50
Create Date: 2023-12-02 15:59:28.238926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1246bf7147b0'
down_revision = 'd1e602c26f50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_conta')
    with op.batch_alter_table('conta', schema=None) as batch_op:
        batch_op.add_column(sa.Column('saldo', sa.String(), nullable=True))
        batch_op.drop_column('valor_total')

    with op.batch_alter_table('hist_acao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('acao_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'acao', ['acao_id'], ['id'])

    with op.batch_alter_table('hist_cripto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ticker', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('descricao', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('preco', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('valor', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('tipo', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('data', sa.Date(), nullable=True))

    with op.batch_alter_table('hist_transacoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descricao', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('valor', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('tipo', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('data', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hist_transacoes', schema=None) as batch_op:
        batch_op.drop_column('data')
        batch_op.drop_column('tipo')
        batch_op.drop_column('valor')
        batch_op.drop_column('descricao')

    with op.batch_alter_table('hist_cripto', schema=None) as batch_op:
        batch_op.drop_column('data')
        batch_op.drop_column('tipo')
        batch_op.drop_column('valor')
        batch_op.drop_column('preco')
        batch_op.drop_column('descricao')
        batch_op.drop_column('ticker')

    with op.batch_alter_table('hist_acao', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('acao_id')

    with op.batch_alter_table('conta', schema=None) as batch_op:
        batch_op.add_column(sa.Column('valor_total', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('saldo')

    op.create_table('_alembic_tmp_conta',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('usuario_id', sa.INTEGER(), nullable=False),
    sa.Column('criacao', sa.DATE(), nullable=True),
    sa.Column('saldo', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
