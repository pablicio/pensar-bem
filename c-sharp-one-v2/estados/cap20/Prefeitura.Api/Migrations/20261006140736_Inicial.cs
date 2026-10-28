using System;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

#nullable disable

namespace Prefeitura.Api.Migrations
{
    /// <inheritdoc />
    public partial class Inicial : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "cidadaos",
                columns: table => new
                {
                    id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    nome = table.Column<string>(type: "text", nullable: false),
                    cpf = table.Column<string>(type: "text", nullable: true),
                    email = table.Column<string>(type: "text", nullable: true),
                    celular = table.Column<string>(type: "text", nullable: true),
                    endereco_bairro = table.Column<string>(type: "text", nullable: true),
                    endereco_logradouro = table.Column<string>(type: "text", nullable: true),
                    endereco_numero = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("pk_cidadaos", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "secretarias",
                columns: table => new
                {
                    sigla = table.Column<string>(type: "text", nullable: false),
                    nome = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("pk_secretarias", x => x.sigla);
                });

            migrationBuilder.CreateTable(
                name: "servidores",
                columns: table => new
                {
                    matricula = table.Column<string>(type: "text", nullable: false),
                    pessoa_id = table.Column<int>(type: "integer", nullable: false),
                    lotacao_sigla = table.Column<string>(type: "text", nullable: false),
                    ativo = table.Column<bool>(type: "boolean", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("pk_servidores", x => x.matricula);
                    table.ForeignKey(
                        name: "fk_servidores_cidadaos_pessoa_id",
                        column: x => x.pessoa_id,
                        principalTable: "cidadaos",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "fk_servidores_secretarias_lotacao_sigla",
                        column: x => x.lotacao_sigla,
                        principalTable: "secretarias",
                        principalColumn: "sigla",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "solicitacoes",
                columns: table => new
                {
                    id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    solicitante_id = table.Column<int>(type: "integer", nullable: false),
                    assunto = table.Column<string>(type: "text", nullable: false),
                    situacao = table.Column<string>(type: "text", nullable: false),
                    protocolo = table.Column<string>(type: "text", nullable: true),
                    secretaria_atual_sigla = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("pk_solicitacoes", x => x.id);
                    table.ForeignKey(
                        name: "fk_solicitacoes_cidadaos_solicitante_id",
                        column: x => x.solicitante_id,
                        principalTable: "cidadaos",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "fk_solicitacoes_secretarias_secretaria_atual_sigla",
                        column: x => x.secretaria_atual_sigla,
                        principalTable: "secretarias",
                        principalColumn: "sigla",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "atendimentos",
                columns: table => new
                {
                    solicitacao_id = table.Column<int>(type: "integer", nullable: false),
                    id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    quando = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    quem_matricula = table.Column<string>(type: "text", nullable: false),
                    descricao = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("pk_atendimentos", x => new { x.solicitacao_id, x.id });
                    table.ForeignKey(
                        name: "fk_atendimentos_servidores_quem_matricula",
                        column: x => x.quem_matricula,
                        principalTable: "servidores",
                        principalColumn: "matricula",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "fk_atendimentos_solicitacoes_solicitacao_id",
                        column: x => x.solicitacao_id,
                        principalTable: "solicitacoes",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "ix_atendimentos_quem_matricula",
                table: "atendimentos",
                column: "quem_matricula");

            migrationBuilder.CreateIndex(
                name: "ix_cidadaos_cpf",
                table: "cidadaos",
                column: "cpf",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "ix_servidores_lotacao_sigla",
                table: "servidores",
                column: "lotacao_sigla");

            migrationBuilder.CreateIndex(
                name: "ix_servidores_pessoa_id",
                table: "servidores",
                column: "pessoa_id");

            migrationBuilder.CreateIndex(
                name: "ix_solicitacoes_protocolo",
                table: "solicitacoes",
                column: "protocolo",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "ix_solicitacoes_secretaria_atual_sigla",
                table: "solicitacoes",
                column: "secretaria_atual_sigla");

            migrationBuilder.CreateIndex(
                name: "ix_solicitacoes_solicitante_id",
                table: "solicitacoes",
                column: "solicitante_id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "atendimentos");

            migrationBuilder.DropTable(
                name: "servidores");

            migrationBuilder.DropTable(
                name: "solicitacoes");

            migrationBuilder.DropTable(
                name: "cidadaos");

            migrationBuilder.DropTable(
                name: "secretarias");
        }
    }
}
