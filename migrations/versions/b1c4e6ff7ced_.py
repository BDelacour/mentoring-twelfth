"""empty message

Revision ID: b1c4e6ff7ced
Revises: 3362d341697e
Create Date: 2023-10-24 21:47:51.828259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1c4e6ff7ced'
down_revision: Union[str, None] = '3362d341697e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('contracts_sale_user_id_fkey', 'contracts', type_='foreignkey')
    op.drop_column('contracts', 'sale_user_id')
    op.alter_column('events', 'support_user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'support_user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('contracts', sa.Column('sale_user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('contracts_sale_user_id_fkey', 'contracts', 'users', ['sale_user_id'], ['id'])
    # ### end Alembic commands ###
