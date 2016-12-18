"""empty message

Revision ID: 0c273a87e923
Revises: 82c718b468d2
Create Date: 2016-12-18 15:16:19.239200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c273a87e923'
down_revision = '82c718b468d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('materials', sa.Column('material_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('materials', 'material_number')
    # ### end Alembic commands ###
