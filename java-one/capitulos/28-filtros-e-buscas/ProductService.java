@Transactional(readOnly = true)
public Page<ProductResponse> buscar(ProductFilter f,
                                    Pageable pageable) {
    Specification<Product> spec = Specification
            .where(ProductSpecs.nomeContem(f.name()))
            .and(ProductSpecs.statusIgual(f.status()))
            .and(ProductSpecs.precoAte(f.maxPrice()));

    return repository.findAll(spec, pageable)
            .map(ProductResponse::of);
}
