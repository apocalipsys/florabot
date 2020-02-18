"""modificacion temp y hum

Revision ID: 4408fc0e153f
Revises: 6077356b7e8a
Create Date: 2019-08-26 00:27:25.690738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4408fc0e153f'
down_revision = '6077356b7e8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuracion', sa.Column('humedad_max', sa.Integer(), nullable=True))
    op.add_column('configuracion', sa.Column('humedad_min', sa.Integer(), nullable=True))
    op.add_column('configuracion', sa.Column('temperatura_max', sa.Integer(), nullable=True))
    op.add_column('configuracion', sa.Column('temperatura_min', sa.Integer(), nullable=True))
    op.drop_column('configuracion', 'temperatura')
    op.drop_column('configuracion', 'humedad')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuracion', sa.Column('humedad', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('configuracion', sa.Column('temperatura', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('configuracion', 'temperatura_min')
    op.drop_column('configuracion', 'temperatura_max')
    op.drop_column('configuracion', 'humedad_min')
    op.drop_column('configuracion', 'humedad_max')
    # ### end Alembic commands ###
