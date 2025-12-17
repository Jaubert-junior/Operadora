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
        raise NotImplementedError("Método deve ser implementado pelas subclasses de TipoDePlano.")
        
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
            return self.__plano_associado.calcular_valor_fatura(minutos_consumidos, dados_consumidos)
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

class FaturaMensal:
    def __init__(self, id_fatura, linha_telefonica, mes, ano, minutos_consumidos=0, dados_consumidos=0):
        self.id_fatura = id_fatura
        self.linha_telefonica = linha_telefonica
        self.mes = mes
        self.ano = ano
        self.minutos_consumidos = minutos_consumidos
        self.dados_consumidos = dados_consumidos

    def registrar_consumo(self, minutos, dados):
        self.minutos_consumidos += minutos
        self.dados_consumidos += dados

    def calcular_valor_total(self):
        plano = self.linha_telefonica.tipo_de_plano
        if not plano:
            raise ValueError(f"A linha {self.linha_telefonica.numero} não possui um plano ativo para calcular a fatura.")

        valor_total = plano.calcular_valor_fatura(
            self.minutos_consumidos,
            self.dados_consumidos
        )
        return valor_total

    def exibir_detalhes_fatura(self):
        try:
            valor_total = self.calcular_valor_total()
            print(f"--- Detalhes da Fatura ---")
            print(f"ID da Fatura: {self.id_fatura}")
            print(f"Linha Telefônica: {self.linha_telefonica.numero}")
            print(f"Mês/Ano de Referência: {self.mes}/{self.ano}")
            print(f"Minutos Consumidos: {self.minutos_consumidos}")
            print(f"Dados Consumidos: {self.dados_consumidos} MB")
            plano = self.linha_telefonica.tipo_de_plano
            print(f"Plano Ativo: {plano.nome_do_plano if plano else 'Nenhum'}")
            print(f"Valor Total da Fatura: R$ {valor_total:.2f}")
            print(f"--------------------------")
        except ValueError as e:
            print(f"Erro ao exibir detalhes da fatura: {e}")
    
    