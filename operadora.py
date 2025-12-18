class TipoDePlano:
    def __init__(self, nome_do_plano, tarifa_mensal_base):
        self.__nome_do_plano = nome_do_plano
        self.__tarifa_mensal_base = tarifa_mensal_base

    @property
    def nome_do_plano(self):
        return self.__nome_do_plano

    @property
    def tarifa(self):
        return self.__tarifa_mensal_base

    def calcular_valor_fatura(self, minutos_consumidos=0, dados_consumidos=0):
        pass

class PlanoControle(TipoDePlano):
    def __init__(self, nome_do_plano, tarifa_mensal_base):
        super().__init__(nome_do_plano, tarifa_mensal_base)

    def calcular_valor_fatura(self, minutos_consumidos=0, dados_consumidos=0):
        tarifa_final = self.tarifa + (minutos_consumidos * 0.5) + (dados_consumidos * 0.5)
        return tarifa_final

class PlanoPosPago(TipoDePlano):
    def __init__(self, nome_do_plano, tarifa_mensal_base):
        super().__init__(nome_do_plano, tarifa_mensal_base)

    def calcular_valor_fatura(self, minutos_consumidos=0, dados_consumidos=0):
        tarifa_final = (1.3 * self.tarifa) + (minutos_consumidos * 0.1) + (dados_consumidos * 0.1)
        return tarifa_final

class LinhaTelefonica:
    def __init__(self, numero, tecnologia):
        self.__numero = numero
        self.__tecnologia = tecnologia
        self.__plano_associado = None

    def associar_plano(self, plano_associado):
        if not isinstance(plano_associado, TipoDePlano):
            raise Exception("Tipo de plano inválido. Informe uma instância de TipoDePlano.")
        self.__plano_associado = plano_associado
        print(f"Plano '{plano_associado.nome_do_plano}' atribuído à linha {self.numero}.")


    def calcular_fatura(self, minutos_consumidos=0, dados_consumidos=0):
        if self.__plano_associado is not None:
            self.__faturaFinal = self.__plano_associado.calcular_valor_fatura(minutos_consumidos, dados_consumidos)
            return self.__faturaFinal
        else:
            raise Exception("Nenhum plano associado à linha telefônica.")

    def exibir_informacoes_linha(self):
        status_plano = self.tipo_de_plano.nome_do_plano if self.tipo_de_plano else "Nenhum plano ativo"
        print(f"Linha: {self.numero}, Plano Ativo: {status_plano}")

    @property
    def numero(self):
        return self.__numero

    @property
    def tipo_de_plano(self):
        return self.__plano_associado

    @property
    def tecnologia(self):
        return self.__tecnologia

    @property
    def faturaFinal(self):
        return self.__faturaFinal

class OperadoraDeTelefonia:
    def __init__(self):
        self.__linhas_telefonicas = []
        self.__historico_faturas = []

    def adicionar_linha_telefonica(self, linha):
        if not isinstance(linha, LinhaTelefonica):
            raise Exception("Linha inválida. Informe uma linha que seja um instância de LinhaTelefonica.")
        self.__linhas_telefonicas.append(linha)
        print(f"Linha {linha.numero} adicionada à operadora.")

    def registrar_fatura(self, fatura):
        if not isinstance(fatura, FaturaMensal):
            raise Exception("Fatura inválida. Informe uma fatura que seja instância de FaturaMensal.")
        self.__historico_faturas.append(fatura)

    def faturamento_total(self):
        total = sum(fatura.calcular_valor_total() for fatura in self.__historico_faturas)
        return total

    @property
    def historico_faturas(self):
        return self.__historico_faturas

    @property
    def linhas_telefonicas(self):
        return self.__linhas_telefonicas


class FaturaMensal:
    def __init__(self, linha_telefonica, minutos_consumidos=0, dados_consumidos=0):
        if not isinstance(linha_telefonica, LinhaTelefonica):
            raise Exception("Linha telefônica inválida. Informe uma instância de LinhaTelefonica.")
        self.linha_telefonica = linha_telefonica
        self.minutos_consumidos = minutos_consumidos
        self.dados_consumidos = dados_consumidos
        self.__valor_total = 0

    def calcular_valor_total(self):
        if self.linha_telefonica.tipo_de_plano is None:
            raise ValueError("A linha telefônica não possui um plano associado.")
        self.__valor_total = self.linha_telefonica.calcular_fatura(
            minutos_consumidos=self.minutos_consumidos,
            dados_consumidos=self.dados_consumidos
        )
        return self.__valor_total

    def exibir_resumo(self):
        try:
            valor_total = self.calcular_valor_total()
            print(f"--- Detalhes da Fatura ---")
            print(f"Linha Telefônica: {self.linha_telefonica.numero}")
            print(f"Plano Ativo: {self.linha_telefonica.tipo_de_plano.nome_do_plano}")
            print(f"Minutos Consumidos: {self.minutos_consumidos}")
            print(f"Dados Consumidos: {self.dados_consumidos}")
            print(f"Valor Total da Fatura: R$ {valor_total:.2f}")
            print(f"--------------------------")
        except ValueError as e:
            print(f"Erro ao exibir detalhes da fatura: {e}")
