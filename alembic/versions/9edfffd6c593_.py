"""empty message

Revision ID: 9edfffd6c593
Revises: ff2e80186c25
Create Date: 2023-04-29 15:10:03.055224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9edfffd6c593"
down_revision = "ff2e80186c25"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        "payment_providers",
        [
            {"id": 1, "name": "other", "url": "{}"},
            {"id": 2, "cashapp": "other", "url": "https://cash.app/${}"},
            {"id": 3, "venmo": "other", "url": "https://venmo.com/{}"},
            {"id": 4, "paypal": "other", "url": "https://paypal.me/{}"},
        ],
    )


def downgrade() -> None:
    pass
