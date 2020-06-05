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

    def indicadores(self, benchmark):
        # CDI
        cdi = pd.read_excel("C:\\Nícolas\\FEA.dev\\fundo_quanti\\CDI.xlsx", index_col=0, header=None)
        # INDEX TO DATETIME
        self.RESULT.index = pd.to_datetime(self.RESULT.index)
        cdi.index = pd.to_datetime(cdi.index)
        cdi = cdi[cdi.index >= self.RESULT.index[0]]
        tx_livre_risco = (cdi[1][-1]/cdi[1][0] - 1) * 100

        # RENTABILIDADE ESTRATEGIA
        rentabilidade = (((self.RESULT['pl'].iloc[-1] / self.RESULT['pl'].iloc[0]) - 1) * 100)
        print("\nrentabilidade estrategia: {:.2f}%".format(rentabilidade))

        # RENTABILIDADE ACAO
        print("rentabilidade share: {:.2f}%".format(((self.RESULT['Adj Close'].iloc[-1] / self.RESULT['Adj Close'].iloc[0]) - 1) * 100))

        # ALPHA
        print("alpha: {:.2f}%".format(
            ((rentabilidade / 100) / (self.RESULT['Adj Close'].iloc[-1] / self.RESULT['Adj Close'].iloc[0]) - 1) * 100))
        # SHARPE RATIO (retorno do fundo - retorno tx livre de risco)/risco fundo
        risco = self.RESULT['pl'].pct_change().std()
        sharpe = (rentabilidade - tx_livre_risco)/risco
        print("Sharpe Ratio: ", sharpe)
        # SHARPE MODIFICADO
        sharper_m = (rentabilidade - (((benchmark['Adj Close'][-1]/benchmark['Adj Close'][-1])-1)*100))/risco
        print("Sharpe Modificado: ", sharper_m)
        # INDICE TREYNOR
        # DRAW DOWN
        # BENCHMARK


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
    dt_ini = '2018-12-31'
    dt_fim = '2019-12-31'
    # SET STRATEGY
    stg = pt(1.45, 14.17, -49.34, 53.24, -20.04)

    # SHARES
    sh_azul = sh(dt_ini, dt_fim, "AZUL4.SA")
    SHARES = sh_azul.data()

    # BENCH MARK
    sh_ibov = sh(dt_ini, dt_fim, "^BVSP")
    BENCH = sh_ibov.data()

    # RUN BACK TEST
    bt = back_test(SHARES, stg, frequency=2)
    bt.run_bt()
    bt.indicadores(BENCH)

if __name__ == '__main__':
    main()