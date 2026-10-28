revision = "a1b2c3"
down_revision = None


def upgrade() -> None:
    op.create_table(
        "produtor",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("cidade", sa.String(100), nullable=False),
    )
    op.create_table(
        "produto",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("preco", sa.Numeric(10, 2), nullable=False),
        sa.Column("produtor_id", sa.BigInteger(), nullable=False),
    )
    op.create_foreign_key(
        "fk_produto_produtor", "produto", "produtor",
        ["produtor_id"], ["id"],
    )


def downgrade() -> None:
    op.drop_table("produto")
    op.drop_table("produtor")
