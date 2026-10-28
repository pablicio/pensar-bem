@PutMapping("/{id}")
public ResponseEntity<Product> atualizar(
        @PathVariable Long id,
        @RequestBody Product dados) {

    Product atual = banco.get(id);
    if (atual == null) {
        return ResponseEntity.notFound().build();
    }
    dados.setId(id);
    banco.put(id, dados);
    return ResponseEntity.ok(dados);
}

@DeleteMapping("/{id}")
public ResponseEntity<Void> apagar(@PathVariable Long id) {
    if (banco.remove(id) == null) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.noContent().build();
}
