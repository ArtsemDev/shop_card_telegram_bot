"""empty message

Revision ID: 04d47b6f244d
Revises: 5113e97de5dd
Create Date: 2023-11-15 12:43:16.627640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04d47b6f244d'
down_revision = '5113e97de5dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        table=sa.table(
            "shops",
            sa.Column("name", sa.VARCHAR(128)),
            sa.Column("barcode_type", sa.VARCHAR(12))
        ),
        rows=[
            {
                "name": "BIG STAR",
                "barcode_type": "upca"
            },
            {
                "name": "ALL STARS",
                "barcode_type": "itf"
            },
            {
                "name": "СОСЕДИ",
                "barcode_type": "code128"
            },
            {
                "name": "5 ЭЛЕМЕНТ",
                "barcode_type": "code128"
            },
            {
                "name": "7 КАРАТ",
                "barcode_type": "ean13"
            }
        ]
    )


def downgrade() -> None:
    pass
