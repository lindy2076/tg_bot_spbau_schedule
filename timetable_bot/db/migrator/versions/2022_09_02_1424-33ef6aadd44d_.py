"""empty message

Revision ID: 33ef6aadd44d
Revises: 11f80ab59a15
Create Date: 2022-09-02 14:24:43.364053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33ef6aadd44d'
down_revision = '11f80ab59a15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq__user__id'), 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq__user__id'), 'user', type_='unique')
    # ### end Alembic commands ###
