
import datetime
import pandas as pd


class dates:

    def __init__(self, path_FOMC: str = None):
        if path_FOMC is not None:
            FOMC = pd.read_csv(path_FOMC)['FOMC'].tolist()
            self.FOMC = pd.to_datetime(FOMC, yearfirst=True)
        self.last_day = '2018-08-08'
        self.recession_end = pd.to_datetime('2009-06-01', yearfirst=True)
        self.TaperTantrum = pd.to_datetime('2015-05-23', yearfirst=True)
        self.Feb2018 = pd.to_datetime('2018-02-01', yearfirst=True)

    # find the subsample before and after the FOMC meetings

    def FOMC_sample(self, df, window: list = [0, 1]):
        '''
        Input:
            df: a pandas.Dataframe object contains the full sample
            FOMC_dates: a pandas.DatetimeIndex object that contains the
            historical dates of FOMC meetings

        Output:
            df_FOMC: a pandas.Dataframe object that contains the subsample
            for the window period specified
        '''

        w = datetime.timedelta(weeks=1)
        after = pd.to_datetime(
            [d + window[1] * w for d in self.FOMC], yearfirst=True)
        before = pd.to_datetime([d - window[0] * w
                                 for d in self.FOMC], yearfirst=True)

        indexlist = []
        for before, after in zip(before, after):
            indexlist += [before + datetime.timedelta(days=x)
                          for x in range(0, (after - before).days)]
        return df.loc[df.index.intersection(indexlist), :]
