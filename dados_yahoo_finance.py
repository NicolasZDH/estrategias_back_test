from pandas_datareader import data
import yfinance as yf
import warnings

warnings.filterwarnings("ignore")

class shares():
    def __init__(self, start_date, end_date, tickets=None):
        yf.pdr_override()

        self.start_date = start_date    # '2016-01-01'
        self.end_date = end_date        # '2019-12-31'

        ibov_acoes = [
            'ABEV3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBDC4.SA', 'BBSE3.SA', 'BEEF3.SA', 'BPAC11.SA',
            'BRAP4.SA', 'BRDT3.SA', 'BRFS3.SA',
            'BRKM5.SA', 'BRML3.SA', 'BTOW3.SA', 'CCRO3.SA', 'CIEL3.SA', 'CMIG4.SA', 'COGN3.SA', 'CPFE3.SA', 'CRFB3.SA',
            'CSAN3.SA', 'CSNA3.SA', 'CVCB3.SA',
            'CYRE3.SA', 'ECOR3.SA', 'EGIE3.SA', 'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENBR3.SA', 'ENGI11.SA', 'EQTL3.SA',
            'FLRY3.SA', 'GGBR4.SA', 'GNDI3.SA',
            'GOAU4.SA', 'GOLL4.SA', 'HAPV3.SA', 'HGTX3.SA', 'HYPE3.SA', 'IGTA3.SA', 'IRBR3.SA', 'ITSA4.SA', 'ITUB4.SA',
            'JBSS3.SA', 'KLBN11.SA', 'LAME4.SA',
            'LREN3.SA', 'MGLU3.SA', 'MRFG3.SA', 'MRVE3.SA', 'MULT3.SA', 'NTCO3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA',
            'QUAL3.SA', 'RADL3.SA', 'RAIL3.SA',
            'RENT3.SA', 'SANB11.SA', 'SBSP3.SA', 'SULA11.SA', 'SUZB3.SA', 'TAEE11.SA', 'TIMP3.SA', 'TOTS3.SA',
            'UGPA3.SA', 'USIM5.SA', 'VALE3.SA', 'VIVT4.SA',
            'VVAR3.SA', 'WEGE3.SA', 'YDUQ3.SA'
            ]

        self.tickets = tickets if tickets is not None else ibov_acoes


    def data(self):
        """

        :return: multi index df of close, open, low, high, volume
        """
        return data.get_data_yahoo(self.tickets, self.start_date, self.end_date)