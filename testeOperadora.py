import pytest 
from operadora import TipoDePlano, PlanoControle, PlanoPosPago, LinhaTelefonica, FaturaMensal, OperadoraDeTelefonia

class TestTiposDePlano:
    def test_plano_controle_calculo_fatura(self):
        plano = PlanoControle("Controle Teste", 60.00)
        assert plano.nome_do_plano == "Controle Teste"
        assert plano.tarifa == 60.00
        assert plano.calcular_valor_fatura(minutos_consumidos=100, dados_consumidos=500) == 360.00
        assert plano.calcular_valor_fatura() == 60.00

    def test_plano_pos_pago_calculo_fatura(self):
        plano = PlanoPosPago("Pós Teste", 100.00)
        assert plano.nome_do_plano == "Pós Teste"
        assert plano.tarifa == 100.00
        assert plano.calcular_valor_fatura(minutos_consumidos=200, dados_consumidos=1024) == 252.40
        assert plano.calcular_valor_fatura() == 130.00

class TestLinhaTelefonica:
    def test_instanciacao_e_propriedades(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        assert linha.numero == "1111-2222"
        assert linha.tecnologia == "4G"
        assert linha.tipo_de_plano is None

    def test_associar_plano_valido(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        plano = PlanoControle("Controle Teste", 50.00)
        linha.associar_plano(plano)
        assert linha.tipo_de_plano == plano

    def test_associar_plano_invalido(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        with pytest.raises(Exception, match="Tipo de plano inválido. Informe uma instância de TipoDePlano."):
            linha.associar_plano("string_invalida")

    def test_calcular_fatura_com_plano(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        plano = PlanoControle("Controle Teste", 50.00)
        linha.associar_plano(plano)
        assert linha.calcular_fatura(minutos_consumidos=10, dados_consumidos=20) == 65.00

    def test_calcular_fatura_sem_plano(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        with pytest.raises(Exception, match="Nenhum plano associado à linha telefônica."):
            linha.calcular_fatura(minutos_consumidos=10, dados_consumidos=20)

class TestOperadoraDeTelefonia:
    def test_instanciacao(self):
        operadora = OperadoraDeTelefonia()
        assert operadora.linhas_telefonicas == []
        assert operadora.historico_faturas == []

    def test_adicionar_linha_telefonica(self):
        operadora = OperadoraDeTelefonia()
        linha = LinhaTelefonica("1111-2222", "4G")
        operadora.adicionar_linha_telefonica(linha)
        assert linha in operadora.linhas_telefonicas

    def test_adicionar_linha_invalida(self):
        operadora = OperadoraDeTelefonia()
        with pytest.raises(Exception, match="Linha inválida. Informe uma instância de LinhaTelefonica."):
            operadora.adicionar_linha_telefonica("string_invalida")
    
    def test_gerar_faturamento_mensal(self):
        operadora = OperadoraDeTelefonia()
        linha = LinhaTelefonica("1111-2222", "4G")
        plano = PlanoControle("Controle Teste", 50.00)
        linha.associar_plano(plano)

class TestFaturaMensal:
    def test_instanciacao_e_propriedades(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        fatura = FaturaMensal(linha, 75.00)
        assert fatura.linha_telefonica == linha
        assert fatura.valor_total == 75.00
    
    def test_calcular_valor_total(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        fatura = FaturaMensal(linha, 75.00)
        assert fatura.calcular_valor_total() == 75.00   

    def test_fatura_com_valor_zero(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        fatura = FaturaMensal(linha, 0.00)
        assert fatura.calcular_valor_total() == 0.00    

    def test_exibir_resumo(self):
        linha = LinhaTelefonica("1111-2222", "4G")
        fatura = FaturaMensal(linha, 75.00)
        resumo = fatura.exibir_resumo()
        assert resumo == "Fatura Mensal - Linha: 1111-2222, Valor Total: R$ 75.00"
        
