"""empty message

Revision ID: eb48e45c5b7b
Revises: 980a4642e8ee
Create Date: 2020-07-23 14:29:29.406403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb48e45c5b7b'
down_revision = '980a4642e8ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###