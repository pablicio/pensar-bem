using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Infraestrutura.Migrations
{
    /// <inheritdoc />
    public partial class Credenciais : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "credenciais",
                columns: table => new
                {
                    matricula = table.Column<string>(type: "text", nullable: false),
                    hash_da_senha = table.Column<string>(type: "text", nullable: false),
                    papel = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("pk_credenciais", x => x.matricula);
                    table.ForeignKey(
                        name: "fk_credenciais_servidores_matricula",
                        column: x => x.matricula,
                        principalTable: "servidores",
                        principalColumn: "matricula",
                        onDelete: ReferentialAction.Cascade);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "credenciais");
        }
    }
}
