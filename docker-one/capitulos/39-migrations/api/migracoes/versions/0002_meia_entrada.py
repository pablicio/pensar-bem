"""meia entrada nas reservas"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"


def upgrade():
    op.add_column(
        "reservas",
        sa.Column("meia_entrada", sa.Boolean(), nullable=False,
                  server_default=sa.false()),
    )


def downgrade():
    op.drop_column("reservas", "meia_entrada")
