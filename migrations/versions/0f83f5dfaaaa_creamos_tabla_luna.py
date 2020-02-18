"""creamos tabla luna

Revision ID: 0f83f5dfaaaa
Revises: 493dbdbad5f9
Create Date: 2019-08-28 21:08:24.847323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f83f5dfaaaa'
down_revision = '493dbdbad5f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('luna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(), nullable=True),
    sa.Column('ciudad', sa.String(), nullable=True),
    sa.Column('provincia', sa.String(), nullable=True),
    sa.Column('pais', sa.String(), nullable=True),
    sa.Column('latitud', sa.String(), nullable=True),
    sa.Column('longitud', sa.String(), nullable=True),
    sa.Column('fase', sa.String(), nullable=True),
    sa.Column('fecha', sa.String(), nullable=True),
    sa.Column('hora', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('luna')
    # ### end Alembic commands ###
