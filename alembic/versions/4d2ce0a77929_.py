"""empty message

Revision ID: 4d2ce0a77929
Revises: 5f0c7b89d90a
Create Date: 2023-04-29 14:33:49.633878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4d2ce0a77929"
down_revision = "5f0c7b89d90a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    payment_providers = op.create_table(
        "payment_providers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_payment_providers_id"), "payment_providers", ["id"], unique=False
    )
    op.bulk_insert(
        payment_providers,
        [
            {"id": 1, "name": "other", "url": "{}"},
            {"id": 2, "cashapp": "other", "url": "https://cash.app/${}"},
            {"id": 3, "venmo": "other", "url": "https://venmo.com/{}"},
            {"id": 4, "paypal": "other", "url": "https://paypal.me/{}"},
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_payment_providers_id"), table_name="payment_providers")
    op.drop_table("payment_providers")
    # ### end Alembic commands ###
