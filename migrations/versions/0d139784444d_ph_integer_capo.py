"""ph integer capo

Revision ID: 0d139784444d
Revises: 7fffa37f5ee5
Create Date: 2019-10-09 02:56:25.118885

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0d139784444d'
down_revision = '7fffa37f5ee5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('configuracion', 'ph_max')
    op.drop_column('configuracion', 'ph_min')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuracion', sa.Column('ph_min', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('configuracion', sa.Column('ph_max', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
