@DataJpaTest
class ProductRepositoryTest {

    @Autowired
    ProductRepository repository;

    @Test
    void deveEncontrarPorStatus() {
        repository.save(new Product("Teclado",
                new BigDecimal("349.90"), 12));

        List<Product> ativos =
                repository.findByStatus(Status.ATIVO);

        assertThat(ativos).hasSize(1);
    }
}
