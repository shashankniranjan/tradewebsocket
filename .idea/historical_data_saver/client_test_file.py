import requests

class FlaskClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def get_last_price(self):
        response = requests.get(self.server_url + '/ltp')
        if response.status_code == 200:
            return response.json()['last_price']
        else:
            raise Exception('Failed to get last price: {}'.format(response.status_code))

    def get_last_msg(self):
        response = requests.get(self.server_url + '/ltm')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to get last msg: {}'.format(response.status_code))

# Example usage:

client = FlaskClient('http://localhost:5000')

def main():
    while True:
        try:
            last_price = client.get_last_price()
            last_msg = client.get_last_msg()

            print('Last price:', last_price)
            print('Last msg:', last_msg)
        except Exception as e:
            print('Error:', e)

if __name__ == '__main__':
    main()
