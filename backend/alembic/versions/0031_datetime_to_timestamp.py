"""empty message

Revision ID: 0031_datetime_to_timestamp
Revises: 0030_user_email_null
Create Date: 2025-01-14 04:13:33.209508

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "0031_datetime_to_timestamp"
down_revision = "0030_user_email_null"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("collections", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("firmware", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("platforms", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("rom_user", schema=None) as batch_op:
        batch_op.alter_column(
            "last_played",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("roms", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("saves", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("screenshots", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("states", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "last_login",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "last_active",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "created_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=mysql.DATETIME(),
            type_=sa.TIMESTAMP(timezone=True),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "last_active",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "last_login",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=True,
        )

    with op.batch_alter_table("states", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("screenshots", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("saves", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("roms", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("rom_user", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "last_played",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=True,
        )

    with op.batch_alter_table("platforms", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("firmware", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    with op.batch_alter_table("collections", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.TIMESTAMP(timezone=True),
            type_=mysql.DATETIME(),
            existing_nullable=False,
            existing_server_default=sa.text("now()"),
        )

    # ### end Alembic commands ###
