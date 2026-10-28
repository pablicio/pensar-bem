final class DinheiroTest extends TestCase
{
    public function test_soma_centavos_sem_perder_precisao(): void
    {
        $total = Dinheiro::emCentavos(10)
            ->mais(Dinheiro::emCentavos(20));

        $this->assertSame(30, $total->centavos);
    }
}
