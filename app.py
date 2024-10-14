import asyncio
from flask import Flask, request, render_template, jsonify
from metaapi_cloud_sdk import MetaApi
import nest_asyncio

nest_asyncio.apply()

app = Flask(__name__)

# Main function to run the trading server
async def main():
    metaapi_token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0YjY3MzQ0YzI5NDQ3NWRkZGQ0M2FjMTNkN2JkZmZmYyIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjRiNjczNDRjMjk0NDc1ZGRkZDQzYWMxM2Q3YmRmZmZjIiwiaWF0IjoxNzI4NjUxMTIzfQ.bdNUn7AIpuTGwso8HM26R-OnfT0PdSfa6p7MNplL9fW-FhgucwqmbSXdqJok06YRz7KIbJkhAYOIUm8XeVlYlBG5u7g2Dgkkxx00yazXmgdTATvPgneLmBkAs2gsV3iHt23FBjjE_6VrTlZbAZaSLkPqDIlQvhBLub1KoMuhtuFROGDTGlAdPvYaUacFvq42oPpc-M0zdziTp6rEd6Dv_cM5KSXLfL4usy69ggi8Kl6WnS9Mxc-mTPJYiR04xC21QhVNg9WzyTWmMdaTXEkfAwARjQhwzw9sjkIbvknSppoLGXH9cXO8rCuU9l28eY1_2BBMVY7sjj2W-Eol9E9FVfLBeFohCY_30HM9pFK_EYsF7LwS9i4zdx1OKRjNQ-17LGs7aq2w--TgP9g6royYBdWGisznvMsd2ilAj09r1WIcjPOjpiHg-6T2AseT9O-wT8CE347UcOr8PwmdF91en0tQ3WSCzZAYWFx2xecQqd5iuVPNGql42WUYWq5G3mk_FZpt2l1Rwm1vkc-OnYnn0xbA-CBz_EQRci6idOxebKGtGBEgxAjCv23uPy08smUH5BhqmmAyy4a18mb97vK1iVcKn6DbD52eVtL_6Hl3jPkXdzk09sitNlTMGsmCcg9DQoowQpVFymn2qWSPoKjGsMsRcrV-IFv9Mf107DeLK_A'  # Add your MetaApi token here
    api = MetaApi(metaapi_token)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html')

    @app.route('/connect', methods=['POST'])
    def connect():
        data = request.get_json()
        login = data['login']
        password = data['password']
        server_name = data['server_name']
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(connect_account(api, login, password, server_name))
        return jsonify({'status': 'Connected'})

    @app.route('/trade', methods=['POST'])
    def trade():
        data = request.get_json()
        login = data['login']
        password = data['password']
        server_name = data['server_name']
        symbol = data['symbol']
        lot_size = float(data['lot_size'])
        num_trades = int(data['num_trades'])
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(trading_logic(api, login, password, server_name, symbol, lot_size, num_trades))
        return jsonify({'status': 'Trades executed'})

    async def trading_logic(api, login, password, server_name, symbol, lot_size, num_trades):
        account = await get_account(api, login, password, server_name)
        if account:
            await account.deploy()
            await wait_for_connection(account)
            connection = account.get_rpc_connection()
            await connection.connect()
            print(f"Placing {num_trades} trades on symbol: {symbol}, lot size: {lot_size}")
            for _ in range(num_trades):
                detected_pattern = await detect_pattern(connection, symbol)
                if detected_pattern:
                    await place_trades(connection, detected_pattern, symbol, lot_size, "Joker1.0")
                else:
                    print("No valid pattern detected, skipping trade.")
            await account.undeploy()

    async def get_account(api, login, password, server_name):
        accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)
        if not account:
            print('Adding MT5 account to MetaApi')
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
        return account

    async def wait_for_connection(account):
        while True:
            state = account.state
            connection_status = account.connection_status
            print(f'Account state: {state}, connection status: {connection_status}')
            if state == 'DEPLOYED' and connection_status == 'CONNECTED':
                break
            await asyncio.sleep(5)
        print('Account connected')

    async def place_trades(connection, order_type, symbol, volume, comment):
        try:
            if order_type == "buy":
                order = await connection.create_market_buy_order(symbol, volume)
                print(f'Buy order successful: {order} - {comment}')
            elif order_type == "sell":
                order = await connection.create_market_sell_order(symbol, volume)
                print(f'Sell order successful: {order} - {comment}')
            else:
                print('Invalid order type')
        except Exception as e:
            print(f"Error placing order: {str(e)}")

    async def connect_account(api, login, password, server_name):
        account = await get_account(api, login, password, server_name)
        if account:
            print('Deploying account...')
            await account.deploy()
            await wait_for_connection(account)
            print('Account deployed and connected.')
        else:
            print('Account not found or failed to create.')

    async def detect_pattern(connection, symbol):
        # Example pattern detection based on 15-minute candles
        market_data = await connection.get_symbol_price(symbol)
        print(f"Market data for {symbol}: {market_data}")
        if not market_data:
            print("Failed to retrieve market data.")
            return None
        # Placeholder: Use real pattern detection logic here
        detected_pattern = 'buy'  # Placeholder for a real detection algorithm
        print(f"Detected pattern: {detected_pattern}")
        return detected_pattern

    app.run(debug=True)

asyncio.run(main())