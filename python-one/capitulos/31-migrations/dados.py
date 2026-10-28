from sqlalchemy import table, column, String
import sqlalchemy as sa


def upgrade() -> None:
    op.add_column(
        "produto",
        sa.Column("categoria", sa.String(20), nullable=True),
    )

    produto = table("produto", column("categoria", String))
    op.execute(
        produto.update().values(categoria="legume")
    )

    op.alter_column("produto", "categoria", nullable=False)
