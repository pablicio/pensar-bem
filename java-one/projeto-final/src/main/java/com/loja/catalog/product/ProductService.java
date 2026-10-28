package com.loja.catalog.product;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ProductService {

    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    @Transactional(readOnly = true)
    public List<Product> listar() {
        return repository.findAll();
    }

    @Transactional(readOnly = true)
    public Product buscar(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ProductNotFoundException(id));
    }

    @Transactional
    public Product criar(Product novo) {
        if (repository.existsByNameIgnoreCase(novo.getName())) {
            throw new DuplicateProductException(novo.getName());
        }
        return repository.save(novo);
    }

    @Transactional
    public Product atualizar(Long id, Product dados) {
        Product atual = buscar(id);
        atual.setName(dados.getName());
        atual.setDescription(dados.getDescription());
        atual.setPrice(dados.getPrice());
        atual.setQuantity(dados.getQuantity());
        return atual;          // sem save: entidade gerenciada
    }

    @Transactional
    public void apagar(Long id) {
        Product atual = buscar(id);
        repository.delete(atual);
    }
}
