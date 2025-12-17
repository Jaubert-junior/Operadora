import pytest 
from operadora import TipoDePlano, PlanoControle, PlanoPosPago, LinhaTelefonica, FaturaMensal

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

class TestFaturaMensal:
    def setup_method(self):
        self.plano_controle = PlanoControle("Controle Fatura", 70.00)
        self.plano_pos = PlanoPosPago("Pós Fatura", 120.00)
        self.linha_com_controle = LinhaTelefonica("3333-4444", "4G")
        self.linha_com_controle.associar_plano(self.plano_controle)
        self.linha_com_pos = LinhaTelefonica("5555-6666", "5G")
        self.linha_com_pos.associar_plano(self.plano_pos)
        self.linha_sem_plano = LinhaTelefonica("7777-8888", "4G")

    def test_instanciacao_e_propriedades(self):
        fatura = FaturaMensal("FAT003", self.linha_com_controle, "Julho", 2023, 0, 0)
        assert fatura.id_fatura == "FAT003"
        assert fatura.linha_telefonica == self.linha_com_controle
        assert fatura.mes == "Julho"
        assert fatura.ano == 2023
        assert fatura.minutos_consumidos == 0
        assert fatura.dados_consumidos == 0

    def test_registrar_consumo(self):
        fatura = FaturaMensal("FAT004", self.linha_com_controle, "Agosto", 2023)
        fatura.registrar_consumo(minutos=50, dados=100)
        assert fatura.minutos_consumidos == 50
        assert fatura.dados_consumidos == 100
        fatura.registrar_consumo(minutos=20, dados=30)
        assert fatura.minutos_consumidos == 70
        assert fatura.dados_consumidos == 130

    def test_calcular_valor_total_plano_controle(self):
        fatura = FaturaMensal("FAT005", self.linha_com_controle, "Setembro", 2023, 50, 100)
        assert fatura.calcular_valor_total() == 145.00

    def test_calcular_valor_total_plano_pos_pago(self):
        fatura = FaturaMensal("FAT006", self.linha_com_pos, "Outubro", 2023, 100, 500)
        assert fatura.calcular_valor_total() == 216.00

    def test_calcular_valor_total_sem_plano_na_linha(self):
        fatura = FaturaMensal("FAT007", self.linha_sem_plano, "Novembro", 2023)
        with pytest.raises(ValueError, match=f"A linha {self.linha_sem_plano.numero} não possui um plano ativo para calcular a fatura."):
            fatura.calcular_valor_total()
