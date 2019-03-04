"""empty message

Revision ID: 6bf5875ae2e1
Revises: 
Create Date: 2019-03-02 16:30:41.474303

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6bf5875ae2e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blacklist',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('user_identity', sa.String(length=50), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('name_lower', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notebook',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'name', name='_user_notebook_uc')
    )
    op.create_table('note',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('description', sa.String(length=2048), nullable=False),
    sa.Column('notebook_id', postgresql.UUID(), nullable=True),
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['notebook_id'], ['notebook.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    op.drop_table('notebook')
    op.drop_table('user')
    op.drop_table('token_blacklist')
    # ### end Alembic commands ###
