@DataJpaTest
class ProductRepositoryTest {

    @Autowired ProductRepository repository;
    @Autowired TestEntityManager em;

    @Test
    void deveBuscarPorNomeIgnorandoCaixa() {
        em.persist(new Product("Teclado Mecânico",
                new BigDecimal("349.90"), 12));
        em.flush();

        var achados = repository
                .findByNameContainingIgnoreCase("mecânico",
                        Pageable.unpaged());

        assertThat(achados).hasSize(1);
    }

    @Test
    void naoDeveAceitarNomeDuplicado() {
        em.persist(new Product("Cabo", BigDecimal.TEN, 1));
        em.flush();

        assertThatThrownBy(() -> {
            em.persist(new Product("Cabo", BigDecimal.TEN, 1));
            em.flush();
        }).isInstanceOf(PersistenceException.class);
    }
}
