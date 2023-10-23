"""empty message

Revision ID: 4271f7a7b015
Revises: d1c060433836
Create Date: 2023-10-24 00:57:17.186849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4271f7a7b015'
down_revision: Union[str, None] = 'd1c060433836'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('phone_number', sa.String(length=32), nullable=False))
    op.drop_column('clients', 'phone_numer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('phone_numer', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.drop_column('clients', 'phone_number')
    # ### end Alembic commands ###
