import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

def prepare_sales(df):
    df.sale_date = df.sale_date.str.replace(' 00:00:00 GMT', '')
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    df = df.set_index('sale_date').sort_index()
    df['month'] = df.index.month_name()
    df['dayofweek'] = df.index.day_name()
    df['sales_total'] = df.sale_amount*df.item_price
    
    return df


def prepare_power_data(df):
    df.columns = df.columns.str.lower()
    df.date = pd.to_datetime(df.date, format='%Y-%m-%d')
    df = df.set_index('date').sort_index()
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    df = df.fillna(0)
    
    return df