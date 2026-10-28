$medirTempo = function (array $req, callable $proximo): Resposta {
    $comeco = hrtime(true);

    $resposta = $proximo($req);

    $ms = (hrtime(true) - $comeco) / 1_000_000;
    header(sprintf('X-Tempo: %.1fms', $ms));

    return $resposta;
};

$exigirCredencial = function (array $req, callable $seg): Resposta {
    if ($req['metodo'] !== 'GET'
        && !isset($_SERVER['HTTP_AUTHORIZATION'])) {
        return new Resposta(401, ['erro' => 'Credencial ausente']);
    }

    return $seg($req);
};

$acao = fn(array $req): Resposta => $roteador->despachar(
    $req['metodo'],
    $req['caminho'],
);

$pipeline = array_reduce(
    array_reverse([$medirTempo, $exigirCredencial]),
    fn(callable $proximo, callable $atual): callable
        => fn(array $req): Resposta => $atual($req, $proximo),
    $acao,
);

enviar($pipeline([
    'metodo' => $_SERVER['REQUEST_METHOD'],
    'caminho' => parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH),
]));
