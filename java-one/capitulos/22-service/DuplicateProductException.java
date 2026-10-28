public class DuplicateProductException extends RuntimeException {
    public DuplicateProductException(String name) {
        super("já existe produto com o nome: " + name);
    }
}
