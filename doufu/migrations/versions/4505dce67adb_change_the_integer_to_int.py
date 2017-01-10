"""change the Integer to INT

Revision ID: 4505dce67adb
Revises: 9c72232f8f14
Create Date: 2017-01-09 09:19:47.680565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4505dce67adb'
down_revision = '9c72232f8f14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('materials', sa.Column('test', sa.Text(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('materials', 'test')
    # ### end Alembic commands ###
