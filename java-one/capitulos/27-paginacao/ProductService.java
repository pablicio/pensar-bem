@Transactional(readOnly = true)
public Page<ProductResponse> listar(Pageable pageable) {
    return repository.findAll(pageable)
            .map(ProductResponse::of);
}
