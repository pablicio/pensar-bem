using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Api.Migrations
{
    /// <inheritdoc />
    public partial class NumeroDoSip : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "numero_sip",
                table: "solicitacoes",
                type: "text",
                nullable: true);

            migrationBuilder.Sql(
                "UPDATE solicitacoes SET numero_sip = id || '/26';");

            migrationBuilder.Sql(
                "SELECT setval(pg_get_serial_sequence('solicitacoes', 'id'), " +
                "(SELECT coalesce(max(id), 0) + 1 FROM solicitacoes), false);");

            migrationBuilder.CreateIndex(
                name: "ix_solicitacoes_numero_sip",
                table: "solicitacoes",
                column: "numero_sip",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "ix_solicitacoes_numero_sip",
                table: "solicitacoes");

            migrationBuilder.DropColumn(
                name: "numero_sip",
                table: "solicitacoes");
        }
    }
}
