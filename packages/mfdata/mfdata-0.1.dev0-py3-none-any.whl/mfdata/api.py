import numpy as np
import pandas as pd
from fredapi import Fred
from mfdata.utils import *
from mfdata.dates import *
import functools


class ts(object):

    def __init__(self,
                 unit: str,
                 multiplier: int,
                 currency: str,
                 UI: str,
                 surface: int,
                 family: list,
                 value):
        self.unit = unit
        self.multiplier = multiplier
        self.currency = currency
        self.UI = UI
        self.surface = surface
        self.family = family
        self.value = value
        self.name = family[surface]


class page(object):

    def __init__(self,
                 category: str,
                 sa: str,
                 value):

        self.category = category
        self.sa = sa  # seasonally-adjusted?
        self.value = value


class frb_h8(dates, plot):
    '''
    Class designed for preparing data from Federal Reserve Board H8 table.
    The class has layers of data that is specified in the H8 table and can
    store data of different categories.

    '''

    def __init__(self,
                 filepath: list):
        '''
        At initialization, data is parsed into time series objects
        categorized by the type of institutions, and aggregated as
        a book of pages. Each time serie records the metadata such
        as the unit of measure, currency, and the unique identifier
        of the serie.

        Raw data will further be transformed into easy-to-use format
        such as Dataframe using functions defined as methods.
        '''

        super(frb_h8, self).__init__()

        self.filepath = filepath
        self.pages = []

        for path in filepath:

            df = pd.read_csv(path)
            col_names = df.columns.values
            category, sa = col_names[1].split(',')[-2:]
            category = category.strip().title()

            if sa.split(' ')[1] == 'not':
                sa = 'NSA'
            else:
                sa = 'SA'

            ts_list = []
            
            # securities
            col_names[2] = 'Bank credit: Securities in bank credit'
            col_names[3] = 'Bank credit: Securities in bank credit: ' + col_names[3]
            col_names[4] = 'Bank credit: Securities in bank credit: Treasury and agency securities: Agency MBS'
            col_names[5] = 'Bank credit: Securities in bank credit: Treasury and agency securities: Treasuries'
            col_names[6] = 'Bank credit: Securities in bank credit: ' + col_names[6]
            col_names[7] = 'Bank credit: Securities in bank credit: Other securities: Non-Agency MBS'
            col_names[8] = 'Bank credit: Securities in bank credit: Other securities: Securities other than MBS or Treasuries' 
            
            # loans
            col_names[9] = 'Bank credit: ' + col_names[9]
            col_names[25] = 'All other loans and leases'
            col_names[26] = 'All other loans and leases: Loans to nondepository financial institutions'
            col_names[27] = 'All other loans and leases: Other loans not elsewhere classified'
            
            for iname in range(10, 28):
                col_names[iname] = 'Bank credit: Loans and leases in bank credit: ' \
                    + col_names[iname]
                
            
            col_names[28] = 'Bank credit: (Less) Allowance for loan and lease losses'
            col_names[30] = 'Total fed funds sold and reverse repo'
            col_names[35] = 'Deposits: ' + col_names[35]
            col_names[36] = 'Deposits: ' + col_names[36]

            df.columns = col_names

            for col in col_names[1:]:
                family = col.split(',')[0].split(':')
                family = list(map(lambda x: x.strip(), family))

                surface = len(family) - 1

                unit = df.loc[df[col_names[0]] == 'Unit:', col].values[0]

                multiplier = df.loc[df[col_names[0]] == 'Multiplier:',
                                    col].values[0]

                currency = df.loc[df[col_names[0]] == 'Currency:',
                                  col].values[0]

                UI = df.loc[df[col_names[0]] ==
                            'Unique Identifier: ', col].values[0]
                UI = UI.split('/')[-1]

                value = df.loc[5:, [col_names[0], col]]
                value.columns = ['Date', family[surface]]
                value['Date'] = pd.to_datetime(value['Date'], yearfirst=True)
                value[family[surface]] = value[family[surface]].astype(float)
                value.set_index('Date', inplace=True)

                ts_list.append(ts(unit=unit, multiplier=multiplier,
                                  currency=currency, UI=UI,
                                  surface=surface, family=family,
                                  value=value))
            pg = page(category=category, sa=sa, value=ts_list)
            self.pages.append(pg)

    def _list(self):
        for page in self.pages:
            page_header = page.category + ', ' + page.sa
            tsname_list = ['{}: {}{}'.format(ts.UI, ts.surface * '\t', ts.name)
                           for ts in page.value]
            page_body = '\n'.join(tsname_list)

            print(color.BOLD + color.RED + page_header + color.END)
            print(page_body)
            print('\n')

    def search(self, page, tsname: str):
        i_ts = 0
        for i, ts in enumerate(page.value):
            if ts.name == tsname:
                i_ts = i
        return i_ts

    def merge(self, tsname: str, multi_index=False):
        df_list = []
        for page in self.pages:
            ts = page.value[self.search(page, tsname)].value
            firstletter = ''.join([word[0].upper()
                                   for word in tsname.split(' ')])
            ts.columns = [firstletter + '_' + page.category[:3]]
            df_list.append(ts)
        df = pd.concat(df_list, axis=1)
        return df

    def combine(self, pages, terms):
        n = 0
        levels = [(a.category.split(' ')[0], b) for a in pages for b in terms]
        columns = pd.MultiIndex.from_tuples(levels, names=['group', 'series'])

        for page in pages:
            tslist = [page.value[self.search(
                page, name)].value for name in terms]
            tempdf = functools.reduce(
                (lambda x, y: pd.merge(x, y, left_index=True, right_index=True,
                                       how='inner')), tslist)
            if n == 1:
                df = df.merge(tempdf, left_index=True,
                              right_index=True, how='inner')
            else:
                df = tempdf
            n = 1
        df.columns = columns
        return df


class dtcc_repo(dates, plot):

    def __init__(self, filepath: str):

        super(dtcc_repo, self).__init__()

        self.filepath = filepath
        GCF = pd.read_excel(filepath, skiprows=6)
        GCF.Date = pd.to_datetime(GCF.Date, yearfirst=True)
        GCF.set_index('Date', inplace=True)
        GCF = GCF[list(GCF)[:3]]
        GCF.columns = ['Repo: MBS', 'Repo: Treasury', 'Repo: Agency']
        self.value = GCF


class database(object):

    def __init__(self,
                 database: str = None,
                 key: str = None,
                 var_list: list = None):
        self.database = database
        self.var_list = var_list  # for simple request in FRED
        self.key = key  # the form depends on the database we use
        self.fred = Fred(api_key=self.key)

    def fetch(self):
        '''
        Fetch data from FRED by names given in a list called var_list

        Return
        '''

        fred = self.fred

        if self.key is None:
            import textwrap
            raise ValueError(textwrap.dedent("""\
                    You need to set a valid API key."""))

        if self.database is not 'fred':
            import textwrap
            raise ValueError(textwrap.dedent("""\
                    This function is intended for FRED, please try other
                    functions."""))
            
        dflist = [fred.get_series(var).to_frame(name = var).resample('D').mean() for var in self.var_list]
        
        df = dflist[0]
        
        for ts in dflist[1:]:
            df = df.merge(ts, left_index = True, right_index = True, how = 'inner')
        
        return df
