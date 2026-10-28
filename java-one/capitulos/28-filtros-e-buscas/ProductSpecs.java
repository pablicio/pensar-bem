public class ProductSpecs {

    public static Specification<Product> nomeContem(String termo) {
        return (root, query, cb) -> termo == null ? null
                : cb.like(cb.lower(root.get("name")),
                          "%" + termo.toLowerCase() + "%");
    }

    public static Specification<Product> statusIgual(Status s) {
        return (root, query, cb) -> s == null ? null
                : cb.equal(root.get("status"), s);
    }

    public static Specification<Product> precoAte(BigDecimal teto) {
        return (root, query, cb) -> teto == null ? null
                : cb.lessThanOrEqualTo(root.get("price"), teto);
    }
}
