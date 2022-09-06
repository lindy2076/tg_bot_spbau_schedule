"""empty message

Revision ID: 4214cd7f6d87
Revises: 33ef6aadd44d
Create Date: 2022-09-02 14:30:24.539868

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4214cd7f6d87'
down_revision = '33ef6aadd44d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('dt_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('tg_id', sa.TEXT(), nullable=False),
    sa.Column('username', sa.TEXT(), nullable=False),
    sa.Column('group', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__user')),
    sa.UniqueConstraint('id', name=op.f('uq__user__id')),
    sa.UniqueConstraint('username', name=op.f('uq__user__username'))
    )
    op.create_index(op.f('ix__user__tg_id'), 'user', ['tg_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__user__tg_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
