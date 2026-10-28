@WebMvcTest(ProductController.class)
class ProductControllerTest {

    @Autowired
    MockMvc mvc;

    @MockitoBean
    ProductService service;

    @Test
    void deveDevolver200EOProdutoQuandoExiste() throws Exception {
        when(service.buscar(1L)).thenReturn(
                new ProductResponse(1L, "Teclado", null,
                        new BigDecimal("349.90"), 12,
                        Status.ATIVO, Instant.now()));

        mvc.perform(get("/products/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Teclado"))
                .andExpect(jsonPath("$.price").value(349.90));
    }
}
