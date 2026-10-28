revision = "0042"
down_revision = "0041"

def upgrade():
    op.create_table(
        "avisos_atraso",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("viagem_id", sa.ForeignKey("viagens.id")),
        sa.Column("minutos", sa.Integer, nullable=False),
    )

def downgrade():
    op.drop_table("avisos_atraso")
