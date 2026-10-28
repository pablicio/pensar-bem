package com.loja.catalog.product;

@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock
    ProductRepository repository;

    @InjectMocks
    ProductService service;

    @Test
    void deveLancarQuandoProdutoNaoExiste() {
        when(repository.findById(99L))
                .thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.buscar(99L))
                .isInstanceOf(ProductNotFoundException.class)
                .hasMessageContaining("99");
    }
}
