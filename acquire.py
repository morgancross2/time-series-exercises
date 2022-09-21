import pandas as pd
import requests
import os

def get_items():
    filename = 'items.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename).iloc[:,1:]
    else:
        base_url = 'https://python.zgulde.net/api/v1/items'
        data = requests.get(base_url).json()

        curr_page = data['payload']['page']
        max_page = data['payload']['max_page']
        next_page = data['payload']['next_page']

        items_list = requests.get(base_url).json()['payload']['items']
        while curr_page <= max_page:
            new_data = requests.get(base_url+'?page='+next_page[-1]).json()['payload']
            for store in new_data['items']:
                items_list.append(store)
            if curr_page < max_page:
                next_page = new_data['next_page']
                curr_page = requests.get(base_url+'?page='+next_page[-1]).json()['payload']['page']
                continue
            else:
                break

        df = pd.DataFrame(items_list)
        df.to_csv(filename)
        return df


def get_stores():
    filename = 'stores.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename).iloc[:,1:]
    else:
        base_url = 'https://python.zgulde.net/api/v1/stores'
        store_list = requests.get(base_url).json()['payload']['stores']
        df = pd.DataFrame(store_list)
        df.to_csv(filename)
        return df
    
    
def get_sales():
    filename = 'sales.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename).iloc[:,1:]
    else:
        base_url = 'https://python.zgulde.net/api/v1/sales'
        data = requests.get(base_url).json()

        curr_page = data['payload']['page']
        max_page = data['payload']['max_page']
        next_page = data['payload']['next_page']

        sales_list = requests.get(base_url).json()['payload']['sales']
        while curr_page < max_page:
            next_page_url = base_url+'?page='+str((curr_page+1))
            new_data = requests.get(next_page_url).json()['payload']
            curr_page = requests.get(next_page_url).json()['payload']['page']
        for store in new_data['sales']:
            sales_list.append(store)

        new_data = requests.get(base_url + '?page='+str(max_page)).json()['payload']
        for store in new_data['sales']:
            sales_list.append(store)

        df = pd.DataFrame(sales_list)
        df.to_csv(filename)

        return df

def get_combined_csv():
    items = get_items()
    sales = get_sales()
    stores = get_stores()

    sales.columns = ['item_id', 'sale_amount', 'sale_date', 'sale_id', 'store_id']
    df = pd.merge(sales, stores, on='store_id', how='left')
    df = pd.merge(df, items, on='item_id', how='left')
    
    return df
    
    
def get_power_data():
    filename = 'power_systems.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename).iloc[:,1:]
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url)
        df = pd.DataFrame(df)
        df.to_csv(filename)
        
    return df
