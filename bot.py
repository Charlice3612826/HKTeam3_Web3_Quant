import time
import schedule
from api_client import RoostooClient
from strategy import SimpleStrategy
import config

class TradingBot:
    def __init__(self):
        self.client = RoostooClient()
        self.strategy = SimpleStrategy()
        self.running = True
        
    def run_once(self):
        """执行一次完整的交易循环"""
        try:
            # 1. 获取市场数据
            market_data = self.client.get_market_data('BTCUSDT')
            print(f"当前价格: {market_data.get('lastPrice', 'N/A')}")
            
            # 2. 生成交易信号
            signal = self.strategy.generate_signal(market_data)
            print(f"信号: {signal}")
            
            # 3. 执行交易
            if signal == 'BUY':
                # 示例：买0.001个BTC
                result = self.client.place_order('BTCUSDT', 'BUY', 0.001)
                print(f"买入订单: {result}")
            elif signal == 'SELL':
                result = self.client.place_order('BTCUSDT', 'SELL', 0.001)
                print(f"卖出订单: {result}")
                
            # 4. 检查账户状态
            account = self.client.get_account_info()
            print(f"账户余额: {account.get('balance', 'N/A')}")
            
        except Exception as e:
            print(f"错误: {e}")
    
    def run_continuous(self):
        """持续运行"""
        print("交易机器人启动...")
        
        # 每5分钟运行一次（避免API频率限制）
        schedule.every(5).minutes.do(self.run_once)
        
        # 立即运行一次
        self.run_once()
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
