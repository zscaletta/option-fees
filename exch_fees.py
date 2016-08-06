import pandas as pd


# list of exch keys for dicts and get_feesched
list_exch = ['ase', 'bat', 'bse', 'cc2',
             'cbo', 'edg', 'gem', 'ise',
             'ihg', 'mia', 'ndq', 'nbo',
             'nys', 'phs']


# dictionary struct containing exch values (can be updated via 'get_feesched()' and saved
# rebates are negative values, assumes contra customer
dict_maketake = {'ase_add': 0.0, 'ase_rem': 0.0,
                    'bat_add': -0.85, 'bat_rem': 0.85,
                    'bse_add': 0.0, 'bse_rem': 0.0,
                    'cc2_add': -0.8, 'cc2_rem': 0.83,
                    'cbo_add': 0.0, 'cbo_rem': 0.0,
                    'edg_add': -0.05, 'edg_rem': -0.05,
                    'gem_add': -0.75, 'gem_rem': 0.82,
                    'ise_add': 0.0, 'ise_rem': 0.0,
                    'ihg_add': -0.05, 'ihg_rem': -0.05,
                    'mia_add': 0.0, 'mia_rem': 0.0,
                 'ndq_add': -0.8, 'ndq_rem': 0.85,
                 'nbo_add': 0.85, 'nbo_rem': -0.8,
                 'nys_add': -0.75, 'nys_rem': 0.85,
                 'phs_add': 0.0, 'phs_rem': 0.0
                 }

# dictionary struct containing
# urls are for tables available at IB website
dict_feesched_urls = {'ase': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1197&nhf=T',
                 'bat': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1328&nhf=T',
                 'bse': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1198&nhf=T',
                 'cc2': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1514&nhf=T',
                 'cbo': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1199&nhf=T',
                 'edg': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=15926&nhf=T',
                      'gem': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=5598&nhf=T',
                      'ise': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1200&nhf=T',
                      'ihg': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=17654&nhf=T',
                      'mia': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=4806&nhf=T',
                      'ndq': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1201&nhf=T',
                      'nbo': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=4099&nhf=T',
                      'nys': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1203&nhf=T',
                      'phs': 'https://gdcdyn.interactivebrokers.com/en/index.php?f=1202&nhf=T'
                      }

# *** fn get_feesched() can be used to retrieve add/remove fees from tables on interactive brokers site
# returns tuple of fees in cents, (remove, add)
# rebates are negative numbers
# assumes public customer, and executions are contra customer

def get_feesched(exch, penny=False, full_table=False):

    exch = exch.lower()
    if exch not in list_exch:
        return "Invalid exch argument provided.  Acceptable exchanges: {0}".format(list_exch)

    if exch == 'ase':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={'  ': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})
            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]

            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Other']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                else:

                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot Symbols']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'bat':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={' ': 'Type',
                                  ' Public Customer': 'PubCust_add',
                                  ' Broker-Dealer/JBO': 'PubCust_rem'})
            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]

            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Non-Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                else:

                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'bse':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]

            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})
            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]

            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Contra Customer4']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot Symbols - Contra Customer']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'cc2':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={' ': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})
            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]

            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Equity - Non-Penny Symbols']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Equity - Penny Symbols']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'cbo':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={' ': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})
            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All - Non-Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All - Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0]) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0]) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'edg':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={' ': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer/JBO': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Non-Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'gem':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Other']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot Options (including SPY)']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'ise':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All other']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All other']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'ihg':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={' ': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Other']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot Options']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'mia':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Other']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot Options']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'ndq':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Non-Penny Pilot (includes NDX)']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot Issues']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'nbo':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            # return a.columns
            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Non-Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'nys':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            # return a.columns
            a = a.rename(columns={'Unnamed: 0': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table.iloc[5]
                    add_int = int(float(add_rem[1]) * 100)
                    rem_int = int(float(add_rem[2]) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table.iloc[2]
                    add_int = int(float(add_rem[1]) * 100)
                    rem_int = int(float(add_rem[2]) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    elif exch == 'phs':
        tables = []
        try:
            tables = pd.read_html(dict_feesched_urls[exch])
        except:
            pass
        if tables:
            a = tables[0]
            a = a.rename(columns={' ': 'Type',
                                  'Public Customer': 'PubCust_add',
                                  'Broker-Dealer': 'PubCust_rem'})

            a['PubCust_add'] = a['PubCust_add'].str.split(' ').str[1]
            a['PubCust_rem'] = a['PubCust_rem'].str.split(' ').str[1]
            pubcust_table = a[['Type', 'PubCust_add', 'PubCust_rem']]

            if full_table:
                return pubcust_table
            else:
                if not penny:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'All Other']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                else:
                    add_rem = pubcust_table[pubcust_table['Type'] == 'Penny Pilot']
                    add_int = int(float(add_rem['PubCust_add'].values[0].replace('—', '-')) * 100)
                    rem_int = int(float(add_rem['PubCust_rem'].values[0].replace('—', '-')) * 100)
                    ad = (add_int, rem_int)
                return ad
        else:
            pass
            return 'Failed to retrieve fee schedule from html: {0}'.format(dict_feesched_urls[exch])

    else:
        return "Unable to complete request"

