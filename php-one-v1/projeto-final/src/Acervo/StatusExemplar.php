<?php

declare(strict_types=1);

namespace CasaAmarela\Acervo;

enum StatusExemplar: string
{
    case Bom = 'bom';
    case Emprestado = 'emprestado';
    case Restauro = 'restauro';
    case Extraviado = 'extraviado';
}
