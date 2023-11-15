"""empty message

Revision ID: 5113e97de5dd
Revises: a0fd89e56361
Create Date: 2023-11-15 10:35:45.769048

"""
from alembic import op
import sqlalchemy as sa
from barcode import PROVIDED_BARCODES

# revision identifiers, used by Alembic.
revision = '5113e97de5dd'
down_revision = 'a0fd89e56361'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        table=sa.table(
            "barcode_types",
            sa.Column("name", sa.VARCHAR(12))
        ),
        rows=[
            {"name": barcode}
            for barcode in PROVIDED_BARCODES
        ]
    )


def downgrade() -> None:
    pass
