using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Api.Migrations
{
    /// <inheritdoc />
    public partial class CriadaEm : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateTimeOffset>(
                name: "criada_em",
                table: "solicitacoes",
                type: "timestamp with time zone",
                nullable: true);

            migrationBuilder.Sql(
                "UPDATE solicitacoes SET criada_em = now() " +
                "WHERE criada_em IS NULL;");

            migrationBuilder.AlterColumn<DateTimeOffset>(
                name: "criada_em",
                table: "solicitacoes",
                type: "timestamp with time zone",
                nullable: false,
                oldClrType: typeof(DateTimeOffset),
                oldType: "timestamp with time zone",
                oldNullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "criada_em",
                table: "solicitacoes");
        }
    }
}
