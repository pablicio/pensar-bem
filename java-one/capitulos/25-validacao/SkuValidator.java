public class SkuValidator
        implements ConstraintValidator<SkuValido, String> {

    private static final Pattern FORMATO =
            Pattern.compile("^[A-Z]{3}-\\d{4}$");

    @Override
    public boolean isValid(String valor,
                           ConstraintValidatorContext ctx) {
        if (valor == null) {
            return true;      // nulidade é assunto do @NotNull
        }
        return FORMATO.matcher(valor).matches();
    }
}
