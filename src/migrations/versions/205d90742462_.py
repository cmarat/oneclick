"""empty message

Revision ID: 205d90742462
Revises: None
Create Date: 2014-02-05 15:22:59.002233

"""

# revision identifiers, used by Alembic.
revision = '205d90742462'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('role', sa.SmallInteger(), nullable=True),
    sa.Column('oauth_token', sa.String(length=66), nullable=True),
    sa.Column('oauth_token_secret', sa.String(length=22), nullable=True),
    sa.Column('xoauth_figshare_id', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')
    ### end Alembic commands ###
