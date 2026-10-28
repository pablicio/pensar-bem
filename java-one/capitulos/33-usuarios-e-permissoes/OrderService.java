@Transactional(readOnly = true)
public OrderResponse buscar(Long id, String emailLogado) {
    Order order = repository.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));

    boolean dono = order.getCustomer()
            .getEmail().equals(emailLogado);

    if (!dono && !ehAdmin()) {
        throw new AccessDeniedException("pedido de outro cliente");
    }
    return OrderResponse.of(order);
}
