package com.loja.catalog.product;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {

    private final ProductService service;

    public ProductController(ProductService service) {
        this.service = service;
    }

    @GetMapping
    public List<Product> listar() {
        return service.listar();
    }

    @GetMapping("/{id}")
    public Product buscar(@PathVariable Long id) {
        return service.buscar(id);
    }

    @PostMapping
    public ResponseEntity<Product> criar(@RequestBody Product novo) {
        Product salvo = service.criar(novo);
        URI local = URI.create("/products/" + salvo.getId());
        return ResponseEntity.created(local).body(salvo);
    }

    @PutMapping("/{id}")
    public Product atualizar(@PathVariable Long id,
                             @RequestBody Product dados) {
        return service.atualizar(id, dados);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void apagar(@PathVariable Long id) {
        service.apagar(id);
    }
}
