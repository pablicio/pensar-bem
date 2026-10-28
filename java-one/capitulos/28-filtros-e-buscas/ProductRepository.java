Page<Product> findByNameContainingIgnoreCase(
        String termo, Pageable pageable);

Page<Product> findByStatusAndPriceBetween(
        Status status, BigDecimal min, BigDecimal max,
        Pageable pageable);
