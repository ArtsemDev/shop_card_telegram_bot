"""empty message

Revision ID: 10c012a33fe4
Revises: 04d47b6f244d
Create Date: 2023-11-15 12:48:10.447703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10c012a33fe4'
down_revision = '04d47b6f244d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        table=sa.table(
            "users",
            sa.Column("id", sa.BIGINT),
            sa.Column("is_admin", sa.BOOLEAN)
        ),
        rows=[
            {"id": 608287610, "is_admin": True}
        ]
    )


def downgrade() -> None:
    pass
