"""empty message

Revision ID: 173cb58e68a0
Revises: 5e5effb4fced
Create Date: 2019-09-25 12:49:35.714310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '173cb58e68a0'
down_revision = '5e5effb4fced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('contact', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('design_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('image_file', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'image_file')
    op.drop_column('users', 'design_name')
    op.drop_column('users', 'contact')
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###
