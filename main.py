from selenium.webdriver import Keys
from seleniumbase import SB
import pandas as pd

def check_account(data, i):
    url = 'https://accounts.binance.com/en/login'
    with SB(uc=True, incognito=True) as sb:
        try:
            sb.maximize_window()
            sb.driver.uc_open_with_reconnect(url, reconnect_time=3)
            sb.type('input[name="username"]', text=data.iloc[i, 0])
            sb.driver.uc_click('button:contains(Next)')
            # sb.click('input#email', timeout=3)
            # sb.update_text('input#email', text)
            # sb.click('button:contains(Next)', timeout=3)
            if sb.assert_text('password'):
                print(f'{data.iloc[i, 0]} is exist!!!')
                data.iloc[i, -1] = True
        except Exception as e:
            print(f'{data.iloc[i, 0]} is not exist!!!')
            data.iloc[i, -1] = False
            input('press any key')

if __name__ == '__main__':
    data = pd.read_excel('binance test.xlsx', header=0, sheet_name='Sheet1')
    data['is_exist'] = None
    # for i in range(len(data)):
    for i in range(2):
        check_account(data, i)
    data.to_csv('checked_email.csv')
    #
    # text = 'Hello@gmail.com'