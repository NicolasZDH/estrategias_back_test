"""
https://www.wrprates.com/teoria-do-prospecto-ou-teoria-da-perspectiva/
"""


class prospect_theory():

    def __init__(self, alpha, beta, gama, realiza_ganho, realiza_perda):
        self.reference_point = None
        self.alpha = alpha
        self.beta = beta
        self.gama = gama
        self.realiza_ganho = realiza_ganho
        self.realiza_perda = realiza_perda
        self.is_first = True
        self.i_have = True

    def new_reference_point(self, rf):
        self.reference_point = rf

    def decision(self, price):
        """

        :param price: actual price of the share
        :return: the decision of buy (1), sell(-1) or hold(0)
        """
        # CHECK IF IS THE FIRST PRICE
        if self.is_first is True:
            self.is_first = False
            self.reference_point = price
            return 1
        # FUNCAO PROSPECTO

        # VENDO NA ALTA QUANDO A AVERSAO A PERDA SE CONCRETIZA (IGUAL OU ACIMA DO LIMITE REALIZA_GANHO)
        if price >= self.reference_point and self.i_have is True:
            prospect_value = (price - self.reference_point) ** self.alpha

            if prospect_value >= self.realiza_ganho:
                # SELL
                self.i_have = False
                return -1

        # LIMITE DA PROPENSAO AO RISCO (IGUAL OU ABAIXO DO  REALIZA_PERDA)
        elif price < self.reference_point and self.i_have is False:
            prospect_value = self.gama * ((-(price - self.reference_point)) ** self.beta)

            if prospect_value <= self.realiza_perda:
                # BUY
                self.i_have = True
                return 1
        # HOLD
        return 0
