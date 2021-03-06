"""ecdb2

Revision ID: 4ec12bc020c6
Revises: 8b7488a05e8f
Create Date: 2019-12-17 21:54:22.854987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ec12bc020c6'
down_revision = '8b7488a05e8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('configuracion', sa.Column('ec_max', sa.Float(), nullable=True))
    op.add_column('configuracion', sa.Column('ec_min', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('configuracion', 'ec_min')
    op.drop_column('configuracion', 'ec_max')
    # ### end Alembic commands ###
