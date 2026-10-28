using System.ComponentModel.DataAnnotations;

namespace Prefeitura.Api;

public class OpcoesSip
{
    [Required]
    public string CaminhoCsv { get; set; } = "";

    [Range(1, 65001)]
    public int Encoding { get; set; } = 1252;
}
