"""Seed providers table

Revision ID: 762c4143a9b4
Revises: cbb75fb098fa
Create Date: 2024-09-15 12:27:28.428118

"""

from typing import Sequence, Union

from db.ProviderSeeder import create_providers, delete_records

# revision identifiers, used by Alembic.
revision: str = "762c4143a9b4"
down_revision: Union[str, None] = "cbb75fb098fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    delete_records()
    create_providers()


def downgrade() -> None:
    delete_records()
