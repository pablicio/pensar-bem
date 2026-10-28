def upgrade() -> None:
    op.alter_column(
        "produto",
        "estoque",
        new_column_name="quantidade_disponivel",
    )


def downgrade() -> None:
    op.alter_column(
        "produto",
        "quantidade_disponivel",
        new_column_name="estoque",
    )
