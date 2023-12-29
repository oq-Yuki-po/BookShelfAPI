"""change tables

Revision ID: 339bd6a50f75
Revises: 
Create Date: 2023-12-30 00:12:15.590568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '339bd6a50f75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_authors'))
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('isbn', sa.String(length=13), nullable=True),
    sa.Column('published_at', sa.Date(), nullable=False),
    sa.Column('cover_path', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_books'))
    )
    op.create_table('book_authors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], name=op.f('fk_book_authors_author_id_authors')),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_book_authors_book_id_books')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_book_authors'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_authors')
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###