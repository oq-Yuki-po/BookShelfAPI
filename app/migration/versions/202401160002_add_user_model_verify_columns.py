"""add user_model verify columns

Revision ID: 5900796f79b6
Revises: 0179f0e9dca0
Create Date: 2024-01-16 00:02:15.696473

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5900796f79b6'
down_revision = '0179f0e9dca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('verification_token', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'verification_token')
    op.drop_column('users', 'is_verified')
    # ### end Alembic commands ###
