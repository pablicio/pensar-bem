package com.loja.catalog.product;

public enum PaymentMethod {
    PIX("Pix", 0, 0),
    BOLETO("Boleto", 3, 0),
    CARTAO("Cartão", 0, 2.99);

    private final String rotulo;
    private final int prazoDias;
    private final double taxaPercentual;

    PaymentMethod(String rotulo, int prazoDias, double taxa) {
        this.rotulo = rotulo;
        this.prazoDias = prazoDias;
        this.taxaPercentual = taxa;
    }

    public double aplicarTaxa(double valor) {
        return valor * (1 + taxaPercentual / 100);
    }

    public String getRotulo() {
        return rotulo;
    }
}
