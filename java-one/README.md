# Materiais — Java One: Aprenda, evolua, sobreviva e se divirta

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t java-one .
docker run --rm -it -v "${PWD}:/projeto" java-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/02-primeiro-programa/App.java`

```bash
javac App.java && java App
```

## Projeto final

`projeto-final/` junta a última versão completa de cada arquivo do
sistema que o livro constrói. Recortes didáticos ficam só em
`capitulos/`. Como executar: abra `projeto-final/README.md`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `projeto-final/ (38 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `02-primeiro-programa` | `App.java`, `Saudacao.java` |
| `05-condicionais` | `Maioridade.java`, `Faixa.java` |
| `06-repeticoes` | `Precos.java`, `Soma.java` |
| `09-orientacao-a-objetos` | `Product.java` |
| `10-encapsulamento` | `Product.java` |
| `12-enums-e-records` | `Status.java`, `PaymentMethod.java`, `ProductResponse.java` |
| `13-excecoes` | `ProductNotFoundException.java` |
| `16-primeiro-projeto-spring` | `CatalogApplication.java`, `pom.xml`, `src/main/resources/application.properties`, `HelloController.java` |
| `17-primeira-api` | `ProductController.java` |
| `19-banco-de-dados` | `application.properties`, `pom.xml` |
| `20-spring-data-jpa` | `Product.java`, `application.properties` |
| `21-repository` | `ProductRepository.java`, `ProductRepositoryTest.java` |
| `22-service` | `ProductService.java`, `ProductNotFoundException.java`, `DuplicateProductException.java`, `ProductController.java` |
| `23-controller` | `ProductController.java` |
| `24-dtos` | `dto/ProductRequest.java`, `dto/ProductResponse.java`, `ProductService.java`, `ProductController.java` |
| `25-validacao` | `pom.xml`, `dto/ProductRequest.java`, `ProductController.java`, `SkuValido.java`, `SkuValidator.java` |
| `26-tratamento-de-erros` | `shared/exception/ApiExceptionHandler.java`, `shared/exception/ApiError.java`, `ApiExceptionHandler.java` |
| `27-paginacao` | `ProductController.java`, `ProductService.java`, `application.properties` |
| `28-filtros-e-buscas` | `ProductRepository.java`, `ProductSpecs.java`, `ProductService.java`, `dto/ProductFilter.java` |
| `29-relacionamentos-jpa` | `Product.java`, `Category.java`, `Order.java` |
| `31-spring-security` | `pom.xml`, `config/SecurityConfig.java`, `User.java`, `Role.java`, `AppUserDetailsService.java` |
| `32-jwt` | `pom.xml`, `security/JwtService.java`, `application.properties`, `security/JwtFilter.java`, `SecurityConfig.java`, `AuthController.java` |
| `33-usuarios-e-permissoes` | `OrderService.java`, `ApiExceptionHandler.java` |
| `35-testando-services` | `ProductServiceTest.java` |
| `36-testando-controllers` | `ProductControllerTest.java` |
| `37-testando-o-banco` | `ProductRepositoryTest.java`, `pom.xml`, `src/main/resources/db/migration/V1__criar_product.sql` |
| `38-openapi` | `pom.xml`, `ProductController.java`, `dto/ProductRequest.java`, `config/OpenApiConfig.java`, `SecurityConfig.java` |
| `39-clientes-http` | `src/test/http/products.http` |
| `42-docker-e-deploy` | `Dockerfile`, `docker-compose.yml`, `pom.xml`, `.github/workflows/ci.yml` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
