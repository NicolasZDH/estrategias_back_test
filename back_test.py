from fundo_quanti.dados_yahoo_finance import shares as sh
from fundo_quanti.prospect_strategy import prospect_theory as pt
import pandas as pd
import numpy as np

class back_test():
    def __init__(self, shares, estrategia, frequency=1, patrimonio_inicial=1000, price_type="Adj Close"):
        self.frequency = frequency
        self.patrimonio = patrimonio_inicial
        self.stg = estrategia           # estrategia.decision(day_price): return the order to buy(1) hold(0) or sell(-1)
        self.p_type = price_type        # Adj Close, Close, Open
        self.shares = shares

    def indicadores(self):
        rentabilidade = (((self.RESULT['pl'].iloc[-1] / self.RESULT['pl'].iloc[0]) - 1)* 100)
        print("\nrentabilidade estrategia: {:.2f}%".format(rentabilidade))
        print("rentabilidade share: {:.2f}%".format(((self.RESULT['Adj Close'].iloc[-1] / self.RESULT['Adj Close'].iloc[0]) - 1) * 100))
        print("alpha: {:.2f}%".format(
            ((rentabilidade / 100) / (self.RESULT['Adj Close'].iloc[-1] / self.RESULT['Adj Close'].iloc[0]) - 1) * 100))

    def run_bt(self):
        # SHARE HISTORICAL SERIES
        # shares = sh(self.start_date, self.end_date, self.ticket)
        # df_share = shares.data()[self.p_type].copy().to_frame()
        df_share = self.shares[self.p_type].copy().to_frame()

        #SELECIONA AS DATAS DE ACORDO COM A FREQUENCIA
        periodos = [df_share.index[x] for x in range(len(df_share.index)) if x % self.frequency == 0]

        # BACK TEST
        # CHOOSE THE DECISIONS: BUY(1), HOLD(0) OR SELL(-1)
        df_decision = df_share[self.p_type][periodos].apply(lambda x: self.stg.decision(x)).copy().to_frame('decision')
        result = pd.concat([df_share, df_decision], axis=1, sort=False)

        # ADD COLUMN QUANTIDADE, CAIXA E PATRIMONIO (SERIA INTERESSANTE UTILIZAR UM LAMBDA, MAS N DESCOBRI COMO)
        qtde = []
        caixa = []
        pl = []
        i_have = False
        pl_anterior = self.patrimonio

        for x in range(len(result)):
            if (result['decision'][x] == 0 or result['decision'][x] == -1) and i_have is True:
                # ADD QTDE
                qtde.append(qtde[x-1])
                # ADD CAIXA
                caixa.append(caixa[x-1])
                # ADD PL
                pl_anterior = result['Adj Close'][x] * qtde[x] + caixa[x]
                pl.append(pl_anterior)

                i_have = False if result['decision'][x] == -1 else True
                # SELL
                if result['decision'][x] == -1:
                    qtde[-1] = 0

            elif result['decision'][x] == 1 and i_have is False:
                # ADD QTDE
                qtde.append(pl_anterior // result['Adj Close'][x])
                # ADD CAIXA
                caixa.append(pl_anterior % result['Adj Close'][x])
                # ADD PL
                pl_anterior = result['Adj Close'][x] * qtde[x] + caixa[x]
                pl.append(pl_anterior)

                i_have = True

            else:
                # ADD QTDE
                qtde.append(qtde[x-1])
                # ADD CAIXA
                caixa.append(caixa[x-1])
                # ADD PL
                pl.append(pl[x-1])


        result['qtde'] = qtde
        result['caixa'] = caixa
        result['pl'] = pl

        self.RESULT = result

        # RENTABILIDADE ESTRATEGIA
        rentabilidade = (((result['pl'].iloc[-1]/result['pl'].iloc[0]) - 1)*100)
        return rentabilidade

def main():
    # SET STRATEGY
    stg = pt(0.88, 0.88, 2.1, 2.4, -2)

    # SHARES
    sh_azul = sh('2016-01-01', '2019-12-31', "AZUL4.SA")
    SHARES = sh_azul.data()

    # RUN BACKTEST
    bt = back_test(SHARES, stg, frequency=1)
    bt.run_bt()
    bt.indicadores()

if __name__ == '__main__':
    main()