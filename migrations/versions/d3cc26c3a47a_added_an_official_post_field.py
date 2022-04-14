"""added an official post field

Revision ID: d3cc26c3a47a
Revises: efac6c78ae95
Create Date: 2022-04-14 23:23:13.383409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3cc26c3a47a'
down_revision = 'efac6c78ae95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instagram_embeddeds', sa.Column('official_post', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instagram_embeddeds', 'official_post')
    # ### end Alembic commands ###