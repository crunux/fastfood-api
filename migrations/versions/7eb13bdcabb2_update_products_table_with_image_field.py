"""update products table with image field

Revision ID: 7eb13bdcabb2
Revises: 73fef376dc26
Create Date: 2024-09-22 11:24:23.462173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7eb13bdcabb2'
down_revision: Union[str, None] = '73fef376dc26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'image')
    # ### end Alembic commands ###
