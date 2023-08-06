from debauto.utils import formata_data


class Configuracao:
    """
        Configuração do débito automático
    """

    def __init__(self, banco, codigo, agencia, conta, convenio, empresa, sequencial, vencimento):
        self.banco = banco
        self.codigo = codigo
        self.agencia = agencia
        self.conta = conta
        self.convenio = convenio
        self.empresa = empresa
        self.sequencial = sequencial
        self.__vencimento = vencimento

    @property
    def vencimento(self):
        return formata_data(self.__vencimento)

    @vencimento.setter
    def vencimento(self, value):
        self.__vencimento = value


class Debito:
    """
        Débito
    """
    def __init__(self, identificacao, agencia, conta, vencimento, valor, moeda, livre, tipo):
        self.identificacao = identificacao
        self.agencia = agencia
        self.conta = conta
        self.__vencimento = vencimento
        self.__valor = valor
        self.moeda = moeda
        self.livre = livre
        self.tipo = tipo

    @property
    def vencimento(self):
        return formata_data(self.__vencimento)

    @vencimento.setter
    def vencimento(self, value):
        self.__vencimento = value

    @property
    def valor(self):
        return str("%.2f" % self.__valor).replace(".", "")

    @valor.setter
    def valor(self, value):
        self.__valor = value


class Remessa:
    """
        Remessa Debito Automatico
    """

    def __init__(self, cfg):
        # assert
        assert isinstance(cfg, Configuracao), TypeError("cfg deve ser uma instância de Configuração.")

        # configuração
        self.configuracao = cfg

        # debitos
        self.__debitos = []

    @property
    def debitos(self):
        return self.__debitos

    @debitos.setter
    def debitos(self, value):
        # assert
        assert isinstance(value, Debito), TypeError("Você deve passar uma instância de débito.")
        self.__debitos.append(value)

    def quantidade(self):
        """ quantidade de débitos """
        return len(self.__debitos)

    def valor_total(self):
        """ valor total dos débitos """
        return sum(_.valor for _ in self.debitos)

    def gerar_txt(self):
        with open('test.txt', 'w+') as f:
            f.write(self.get_header())

            for _ in self.get_debitos():
                f.write(_)

            f.write(self.get_trailler())

    def __repr__(self):
        """ representação do objeto """
        return "<Remessa: %s>" % self.configuracao.banco
