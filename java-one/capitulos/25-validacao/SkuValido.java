@Documented
@Constraint(validatedBy = SkuValidator.class)
@Target({ElementType.FIELD, ElementType.RECORD_COMPONENT})
@Retention(RetentionPolicy.RUNTIME)
public @interface SkuValido {
    String message() default "SKU inválido";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
