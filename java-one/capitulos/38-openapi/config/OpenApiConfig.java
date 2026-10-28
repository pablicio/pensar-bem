@Configuration
public class OpenApiConfig {

    @Bean
    OpenAPI api() {
        return new OpenAPI()
            .info(new Info()
                .title("Aurora Comércio — Catálogo")
                .version("1.0")
                .description("API de produtos, pedidos e clientes."))
            .addSecurityItem(
                new SecurityRequirement().addList("bearer"))
            .components(new Components()
                .addSecuritySchemes("bearer",
                    new SecurityScheme()
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")));
    }
}
