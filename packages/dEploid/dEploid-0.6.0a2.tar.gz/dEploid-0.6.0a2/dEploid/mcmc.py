import _dEploid
from pandas import DataFrame


class chain(object):
    def __init__(self, args):
        self.mcmcSamples = _dEploid.mcmcChain(args)

    def get_proportions(self):
        """
        """
        df = DataFrame(self.mcmcSamples.get_proportions())
        df.columns = ["p" + str(i+1) for i in range(len(df.columns))]
        return df

    def get_llk(self):
        """
        """
        return self.mcmcSamples.get_llk()

    def get_hap(self):
        """
        """
        df = DataFrame(self.mcmcSamples.get_hap())
        df.columns = ["h" + str(i+1) for i in range(len(df.columns))]
        return df
