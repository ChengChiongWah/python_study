"""del recipe author column

Revision ID: dcfe1af606ff
Revises: f672fa517a27
Create Date: 2017-01-11 09:45:10.025954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dcfe1af606ff'
down_revision = 'f672fa517a27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipes', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipes', sa.Column('author', mysql.TINYTEXT(), nullable=True))
    # ### end Alembic commands ###
