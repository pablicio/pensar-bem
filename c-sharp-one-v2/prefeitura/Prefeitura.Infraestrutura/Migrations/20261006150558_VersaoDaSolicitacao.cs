using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Infraestrutura.Migrations
{
    /// <inheritdoc />
    public partial class VersaoDaSolicitacao : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<uint>(
                name: "xmin",
                table: "solicitacoes",
                type: "xid",
                rowVersion: true,
                nullable: false,
                defaultValue: 0u);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "xmin",
                table: "solicitacoes");
        }
    }
}
