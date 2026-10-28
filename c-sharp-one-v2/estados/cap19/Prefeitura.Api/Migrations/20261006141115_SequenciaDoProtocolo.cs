using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Prefeitura.Api.Migrations
{
    /// <inheritdoc />
    public partial class SequenciaDoProtocolo : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateSequence<int>(
                name: "protocolo_sequencial");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropSequence(
                name: "protocolo_sequencial");
        }
    }
}
