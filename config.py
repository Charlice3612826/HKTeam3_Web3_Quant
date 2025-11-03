import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件中的环境变量

# Roostoo API配置
ROOSTOO_API_KEY = os.getenv('ROOSTOO_API_KEY')
ROOSTOO_SECRET = os.getenv('ROOSTOO_SECRET')
ROOSTOO_BASE_URL = "https://mock-api.roostoo.com"

# 交易配置
INITIAL_BALANCE = 50000  # 初始资金
COMMISSION_RATE = 0.001  # 手续费率

# API端点
ENDPOINTS = {
    'server_time': '/v3/serverTime',
    'exchange_info': '/v3/exchangeInfo',
    'ticker': '/v3/ticker',
    'balance': '/v3/balance',
    'pending_count': '/v3/pending_count',
    'place_order': '/v3/place_order',
    'query_order': '/v3/query_order',
    'cancel_order': '/v3/cancel_order'
}
