<?php

use App\Emprestimos\Dinheiro;

test('soma centavos sem perder precisão', function () {
    $total = Dinheiro::emCentavos(10)
        ->mais(Dinheiro::emCentavos(20));

    expect($total->centavos)->toBe(30);
});
