import os.path

from selenium.webdriver import Keys
from seleniumbase import SB
import pandas as pd
from seleniumbase.common.exceptions import TextNotVisibleException
import numpy as np


def check_account(data, i):
    url = 'https://accounts.binance.com/en/login'
    while 1:
        with SB(
                uc=True,
                incognito=True,
                proxy='udksqrvp-rotate:0irkbd10fjkn@p.webshare.io:80',
                maximize=True) as sb:
            sb.driver.uc_open_with_reconnect(url, reconnect_time=8)
            sb.type('input[name="username"]', text=data.iloc[i, 0])
            sb.driver.uc_click('button:contains(Next)', reconnect_time=8)
            try:
                sb.assert_text('found', timeout=3)
                print(f'{data.iloc[i, 0]} is not exist!!!')
                data.iloc[i, -1] = 'No'
                break
            except TextNotVisibleException:
                try:
                    sb.assert_text('password', timeout=3)
                    print(f'{data.iloc[i, 0]} is exist!!!')
                    data.iloc[i, -1] = 'Yes'
                    break
                except TextNotVisibleException:
                    try:
                        sb.assert_text('passkey', timeout=3)
                        print(f'{data.iloc[i, 0]} is exist!!!')
                        data.iloc[i, -1] = 'Yes'
                        break
                    except TextNotVisibleException:
                        try:
                            sb.assert_text('valid', timeout=3)
                            print(f'{data.iloc[i, 0]} is not exist!!!')
                            data.iloc[i, -1] = 'No'
                            break
                        # except TextNotVisibleException as e:
                        except Exception as e:
                            print('error found...retry')
                            print(e)
                            # input('press any key to continue')

if __name__ == '__main__':
    if os.path.exists('checked_email.csv'):
        data = pd.read_csv('checked_email.csv')
    else:
        data = pd.read_excel('binance test.xlsx', header=0, sheet_name='Sheet1')
        data['is_exist'] = None
    print(data)
    for i in range(len(data)):
        if pd.isna(data.iloc[i, -1]):
            check_account(data, i)
            print(data)
            data.to_csv('checked_email.csv', index=False)
        else:
            continue
