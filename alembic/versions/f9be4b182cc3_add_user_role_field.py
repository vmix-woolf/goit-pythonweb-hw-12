"""add_user_role_field

Revision ID: f9be4b182cc3
Revises: 47b2e1f4019f
Create Date: 2025-12-05 23:33:03.059652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9be4b182cc3'
down_revision: Union[str, Sequence[str], None] = '47b2e1f4019f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### команди автоматично згенеровані Alembic - ПОЧАТОК ###

    # 1. Додаємо поле як nullable
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=True))

    # 2. Заповнюємо значення за замовчуванням для існуючих користувачів
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")

    # 3. Тепер робимо поле NOT NULL
    op.alter_column('users', 'role', nullable=False)

    # ### команди автоматично згенеровані Alembic - КІНЕЦЬ ###


def downgrade() -> None:
    # ### команди автоматично згенеровані Alembic - ПОЧАТОК ###
    op.drop_column('users', 'role')
    # ### команди автоматично згенеровані Alembic - КІНЕЦЬ ###
