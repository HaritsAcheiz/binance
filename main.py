from selenium.webdriver import Keys
from seleniumbase import SB
import pandas as pd
from seleniumbase.common.exceptions import TextNotVisibleException


def check_account(data, i):
    url = 'https://accounts.binance.com/en/login'
    while 1:
        with SB(
                uc=True,
                incognito=True,
                proxy='udksqrvp-rotate:0irkbd10fjkn@p.webshare.io:80',
                maximize=True) as sb:
            sb.driver.uc_open_with_reconnect(url, reconnect_time=3)
            sb.type('input[name="username"]', text=data.iloc[i, 0])
            sb.driver.uc_click('button:contains(Next)')
            try:
                sb.assert_text('found', timeout=3)
                print(f'{data.iloc[i, 0]} is not exist!!!')
                data.iloc[i, -1] = False
                break
            except TextNotVisibleException:
                try:
                    sb.assert_text('password', timeout=3)
                    print(f'{data.iloc[i, 0]} is exist!!!')
                    data.iloc[i, -1] = True
                    break
                except TextNotVisibleException:
                    try:
                        sb.assert_text('passkey', timeout=3)
                        print(f'{data.iloc[i, 0]} is exist!!!')
                        data.iloc[i, -1] = True
                        break
                    except TextNotVisibleException:
                        print('error found...retry')

if __name__ == '__main__':
    data = pd.read_excel('binance test.xlsx', header=0, sheet_name='Sheet1')
    data['is_exist'] = None
    for i in range(len(data)):
        check_account(data, i)
    data.to_csv('checked_email.csv')
