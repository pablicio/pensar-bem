using Microsoft.EntityFrameworkCore;
using Prefeitura.Dominio;

namespace Prefeitura.Api;

public class PrefeituraDbContext(
    DbContextOptions<PrefeituraDbContext> options)
    : DbContext(options)
{
    public DbSet<Secretaria> Secretarias => Set<Secretaria>();
    public DbSet<Cidadao> Cidadaos => Set<Cidadao>();
    public DbSet<Servidor> Servidores => Set<Servidor>();
    public DbSet<Solicitacao> Solicitacoes => Set<Solicitacao>();

    protected override void OnModelCreating(ModelBuilder modelo)
    {
        modelo.Entity<Secretaria>().HasKey(s => s.Sigla);

        modelo.HasSequence<int>("protocolo_sequencial");

        modelo.Entity<Cidadao>(c =>
        {
            c.HasKey(x => x.Id);
            c.HasIndex(x => x.Cpf).IsUnique();
            c.ComplexProperty(x => x.Endereco);
        });

        modelo.Entity<Servidor>(v =>
        {
            v.HasKey(x => x.Matricula);
            v.HasOne(x => x.Pessoa).WithMany()
                .OnDelete(DeleteBehavior.Restrict);
            v.HasOne(x => x.Lotacao).WithMany()
                .OnDelete(DeleteBehavior.Restrict);
        });

        modelo.Entity<Solicitacao>(s =>
        {
            s.HasKey(x => x.Id);
            s.Property(x => x.Assunto);
            s.Property(x => x.CriadaEm);
            s.Property(x => x.Situacao).HasConversion<string>();
            s.Property(x => x.Protocolo).HasConversion(
                p => p!.ToString(),
                texto => Protocolo.Ler(texto));
            s.HasIndex(x => x.Protocolo).IsUnique();
            s.HasIndex(x => x.NumeroSip).IsUnique();
            s.HasIndex("SecretariaAtualSigla", "Situacao", "CriadaEm");

            s.HasOne(x => x.Solicitante).WithMany()
                .OnDelete(DeleteBehavior.Restrict);
            s.HasOne(x => x.SecretariaAtual).WithMany()
                .OnDelete(DeleteBehavior.Restrict);

            s.OwnsMany(x => x.Atendimentos, a =>
            {
                a.ToTable("atendimentos");
                a.HasOne(x => x.Quem).WithMany()
                    .OnDelete(DeleteBehavior.Restrict);
            });
        });
    }
}
