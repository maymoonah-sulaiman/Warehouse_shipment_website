"""empty message

Revision ID: d26b09ba10fc
Revises: 
Create Date: 2020-06-30 21:28:24.186512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd26b09ba10fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shipment_items', 'quantity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shipment_items', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
