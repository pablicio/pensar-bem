using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Infraestrutura.Migrations
{
    /// <inheritdoc />
    public partial class IndiceDaLista : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "ix_solicitacoes_secretaria_atual_sigla",
                table: "solicitacoes");

            migrationBuilder.CreateIndex(
                name: "ix_solicitacoes_secretaria_atual_sigla_situacao_criada_em",
                table: "solicitacoes",
                columns: new[] { "secretaria_atual_sigla", "situacao", "criada_em" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "ix_solicitacoes_secretaria_atual_sigla_situacao_criada_em",
                table: "solicitacoes");

            migrationBuilder.CreateIndex(
                name: "ix_solicitacoes_secretaria_atual_sigla",
                table: "solicitacoes",
                column: "secretaria_atual_sigla");
        }
    }
}
