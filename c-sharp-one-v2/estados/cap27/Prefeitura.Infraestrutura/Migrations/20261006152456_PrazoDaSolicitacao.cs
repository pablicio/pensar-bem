using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Infraestrutura.Migrations
{
    /// <inheritdoc />
    public partial class PrazoDaSolicitacao : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateOnly>(
                name: "prazo_em",
                table: "solicitacoes",
                type: "date",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "prazo_em",
                table: "solicitacoes");
        }
    }
}
