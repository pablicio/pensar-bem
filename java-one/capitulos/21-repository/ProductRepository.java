public interface ProductRepository
        extends JpaRepository<Product, Long> {

    List<Product> findByStatus(Status status);

    List<Product> findByNameContainingIgnoreCase(String termo);

    List<Product> findByPriceBetween(BigDecimal min, BigDecimal max);

    Optional<Product> findByNameIgnoreCase(String name);

    boolean existsByName(String name);

    long countByStatus(Status status);

    List<Product> findByStatusOrderByPriceDesc(Status status);
}
