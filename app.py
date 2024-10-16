import asyncio
from flask import Flask, render_template, request, jsonify
from metaapi_cloud_sdk import MetaApi
import nest_asyncio

nest_asyncio.apply()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    server_name = data.get('server_name')
    asyncio.run(connect_to_account(login, password, server_name))
    return jsonify({"status": "Connected"})

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    server_name = data.get('server_name')
    symbol = data.get('symbol')
    lot_size = data.get('lot_size')
    num_trades = data.get('num_trades')
    auto_trade = data.get('auto_trade')
    trading_logic = data.get('trading_logic', 'crossover')  # default logic
    asyncio.run(execute_trade(login, password, server_name, symbol, lot_size, num_trades, auto_trade, trading_logic))
    return jsonify({"status": "Trade Successful"})

async def connect_to_account(login, password, server_name):
    api = MetaApi('eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0YjY3MzQ0YzI5NDQ3NWRkZGQ0M2FjMTNkN2JkZmZmYyIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjRiNjczNDRjMjk0NDc1ZGRkZDQzYWMxM2Q3YmRmZmZjIiwiaWF0IjoxNzI4NjUxMTIzfQ.bdNUn7AIpuTGwso8HM26R-OnfT0PdSfa6p7MNplL9fW-FhgucwqmbSXdqJok06YRz7KIbJkhAYOIUm8XeVlYlBG5u7g2Dgkkxx00yazXmgdTATvPgneLmBkAs2gsV3iHt23FBjjE_6VrTlZbAZaSLkPqDIlQvhBLub1KoMuhtuFROGDTGlAdPvYaUacFvq42oPpc-M0zdziTp6rEd6Dv_cM5KSXLfL4usy69ggi8Kl6WnS9Mxc-mTPJYiR04xC21QhVNg9WzyTWmMdaTXEkfAwARjQhwzw9sjkIbvknSppoLGXH9cXO8rCuU9l28eY1_2BBMVY7sjj2W-Eol9E9FVfLBeFohCY_30HM9pFK_EYsF7LwS9i4zdx1OKRjNQ-17LGs7aq2w--TgP9g6royYBdWGisznvMsd2ilAj09r1WIcjPOjpiHg-6T2AseT9O-wT8CE347UcOr8PwmdF91en0tQ3WSCzZAYWFx2xecQqd5iuVPNGql42WUYWq5G3mk_FZpt2l1Rwm1vkc-OnYnn0xbA-CBz_EQRci6idOxebKGtGBEgxAjCv23uPy08smUH5BhqmmAyy4a18mb97vK1iVcKn6DbD52eVtL_6Hl3jPkXdzk09sitNlTMGsmCcg9DQoowQpVFymn2qWSPoKjGsMsRcrV-IFv9Mf107DeLK_A')  # Remove your API access token here
    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)
    if not account:
        account = await api.metatrader_account_api.create_account({
            'name': 'Test account',
            'type': 'cloud',
            'login': login,
            'password': password,
            'server': server_name,
            'platform': 'mt5',
            'application': 'MetaApi',
            'magic': 1000,
        })
    await account.deploy()
    while True:
        state = account.state
        connection_status = account.connection_status
        if state == 'DEPLOYED' and connection_status == 'CONNECTED':
            break
        await asyncio.sleep(5)
    print('Account connected')

async def execute_trade(login, password, server_name, symbol, lot_size, num_trades, auto_trade, trading_logic):
    api = MetaApi('eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0YjY3MzQ0YzI5NDQ3NWRkZGQ0M2FjMTNkN2JkZmZmYyIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjRiNjczNDRjMjk0NDc1ZGRkZDQzYWMxM2Q3YmRmZmZjIiwiaWF0IjoxNzI4NjUxMTIzfQ.bdNUn7AIpuTGwso8HM26R-OnfT0PdSfa6p7MNplL9fW-FhgucwqmbSXdqJok06YRz7KIbJkhAYOIUm8XeVlYlBG5u7g2Dgkkxx00yazXmgdTATvPgneLmBkAs2gsV3iHt23FBjjE_6VrTlZbAZaSLkPqDIlQvhBLub1KoMuhtuFROGDTGlAdPvYaUacFvq42oPpc-M0zdziTp6rEd6Dv_cM5KSXLfL4usy69ggi8Kl6WnS9Mxc-mTPJYiR04xC21QhVNg9WzyTWmMdaTXEkfAwARjQhwzw9sjkIbvknSppoLGXH9cXO8rCuU9l28eY1_2BBMVY7sjj2W-Eol9E9FVfLBeFohCY_30HM9pFK_EYsF7LwS9i4zdx1OKRjNQ-17LGs7aq2w--TgP9g6royYBdWGisznvMsd2ilAj09r1WIcjPOjpiHg-6T2AseT9O-wT8CE347UcOr8PwmdF91en0tQ3WSCzZAYWFx2xecQqd5iuVPNGql42WUYWq5G3mk_FZpt2l1Rwm1vkc-OnYnn0xbA-CBz_EQRci6idOxebKGtGBEgxAjCv23uPy08smUH5BhqmmAyy4a18mb97vK1iVcKn6DbD52eVtL_6Hl3jPkXdzk09sitNlTMGsmCcg9DQoowQpVFymn2qWSPoKjGsMsRcrV-IFv9Mf107DeLK_A')  # Remove your API access token here
    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)
    await account.deploy()
    connection = account.get_rpc_connection()
    await connection.connect()
    
    moving_average = None
    for _ in range(int(num_trades)):
        price_data = await connection.get_symbol_price(symbol)  # Fetch the current price data
        price = price_data['bid']  # Assuming we're using the bid price
        
        if moving_average is None:
            moving_average = price  # Initialize moving average
        
        moving_average = (moving_average + price) / 2  # Simple moving average calculation
        
        if price > moving_average:
            order = await connection.create_market_buy_order(symbol, float(lot_size))
        else:
            order = await connection.create_market_sell_order(symbol, float(lot_size))
        
        print(f'Trade successful: {order}')
        await asyncio.sleep(1)  # Sleep for 1 second between trades

    await account.undeploy()

if __name__ == "__main__":
    app.run(debug=True, port=5000)