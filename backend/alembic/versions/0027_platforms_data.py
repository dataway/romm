"""platforms_data

Revision ID: 0027_platforms_data
Revises: 0026_romuser_status_fields
Create Date: 2024-11-17 23:05:31.038917

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0027_platforms_data"
down_revision = "0026_romuser_status_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("platforms", schema=None) as batch_op:
        batch_op.add_column(sa.Column("category", sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column("generation", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column("family_name", sa.String(length=1000), nullable=True)
        )
        batch_op.add_column(
            sa.Column("family_slug", sa.String(length=1000), nullable=True)
        )
        batch_op.add_column(sa.Column("url", sa.String(length=1000), nullable=True))
        batch_op.add_column(
            sa.Column("url_logo", sa.String(length=1000), nullable=True)
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("platforms", schema=None) as batch_op:
        batch_op.drop_column("url_logo")
        batch_op.drop_column("url")
        batch_op.drop_column("family_name")
        batch_op.drop_column("family_slug")
        batch_op.drop_column("generation")
        batch_op.drop_column("category")
    # ### end Alembic commands ###
