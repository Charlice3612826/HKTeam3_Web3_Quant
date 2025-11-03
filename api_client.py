import requests
import config
from datetime import datetime

class RoostooClient:
    def __init__(self):
        self.base_url = config.ROOSTOO_BASE_URL
        self.api_key = config.ROOSTOO_API_KEY
        self.secret = config.ROOSTOO_SECRET
    
    def get_market_data(self, symbol='BTCUSDT'):
        """获取市场数据"""
        # 根据实际API文档修改端点
        url = f"{self.base_url}/api/v1/ticker?symbol={symbol}"
        response = requests.get(url)
        return response.json()
    
    def place_order(self, symbol, side, quantity):
        """下单"""
        # 根据实际API文档修改
        url = f"{self.base_url}/api/v1/order"
        data = {
            'symbol': symbol,
            'side': side,  # 'BUY' or 'SELL'
            'quantity': quantity,
            'timestamp': int(datetime.now().timestamp() * 1000)
        }
        # 这里需要添加签名逻辑（根据API文档要求）
        response = requests.post(url, json=data)
        return response.json()
    
    def get_account_info(self):
        """获取账户信息"""
        url = f"{self.base_url}/api/v1/account"
        response = requests.get(url)
        return response.json()
