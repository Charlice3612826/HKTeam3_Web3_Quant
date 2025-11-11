import time
import schedule
from api_client import client  # 导入我们创建的客户端
from strategy import SimpleStrategy, QuickTestStrategy，OpeningRangeBreakoutStrategy
import config

class TradingBot:
    def __init__(self):
        self.client = client
        self.strategy = OpeningRangeBreakoutStrategy()
        self.running = True
        
    def test_connection(self):
        """测试API连接"""
        print("测试API连接...")
        
        # 测试服务器时间
        result = self.client.get_server_time()
        print(f"服务器时间: {result}")
        
        # 测试交易所信息
        result = self.client.get_exchange_info()
        print(f"交易所信息: {result}")
        
        # 测试余额查询
        result = self.client.get_balance()
        print(f"账户余额: {result}")
        
        # 测试行情数据
        result = self.client.get_ticker('BTC/USD')
        print(f"BTC行情: {result}")
    
    import logging

    def run_once(self):
        """执行一次完整的交易循环"""
        try:
            print("\n" + "="*50)
            print("开始交易循环...")
    
            # 初始化日志路径
            today = datetime.now().strftime('%Y-%m-%d')
            os.makedirs("logs", exist_ok=True)
            log_file = f'logs/{today}.log'
            logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    
            # 1. 获取历史K线数据
            ohlcv = self.client.get_ohlcv('BTC/USD', '15m', 100)
            if not ohlcv:
                print("❌ 获取K线数据失败，跳过本轮")
                return
    
            df = self.client.convert_to_dataframe(ohlcv)
            if df.empty:
                print("⚠️ K线数据为空")
                return
    
            # 2. 生成交易信号
            signal_df = self.strategy.generate_signals(df)
            latest_signal = signal_df['signal'].iloc[-1]
            current_price = df['close'].iloc[-1]
            print(f"📈 当前价格: {current_price}, 信号: {latest_signal}")
    
            # 3. 执行交易
            if latest_signal == 1:
                print("🟢 执行买入...")
                result = self.client.place_order('BTC/USD', 'BUY', 'MARKET', 0.0001)
                print(f"✅ 买入结果: {result}")
                logging.info(f"BUY at {current_price}, result: {result}")
            elif latest_signal == -1:
                print("🔴 执行卖出...")
                result = self.client.place_order('BTC/USD', 'SELL', 'MARKET', 0.0001)
                print(f"✅ 卖出结果: {result}")
                logging.info(f"SELL at {current_price}, result: {result}")
            else:
                print("⏸ 无交易信号")
    
            # 4. 打印余额
            account = self.client.get_balance()
            if account.get("Success"):
                usd_balance = account['SpotWallet']['USD']['Free']
                print(f"💰 当前USD余额: {usd_balance}")
                logging.info(f"USD balance: {usd_balance}")
    
        except Exception as e:
            print(f"⚠️ 交易循环错误: {e}")
            logging.exception(f"交易循环异常: {e}")

    def run_continuous(self):
        """持续运行"""
        print("🚀 启动快速测试模式...")
        
        # 先测试连接
        self.test_connection()
        
        # 修改这行：改为每2分钟运行一次（原先是5分钟）
        schedule.every(2).minutes.do(self.run_once)
        
        # 立即运行一次
        self.run_once()
        
        print("⏰ 机器人开始运行（每2分钟检查一次）...")
        while self.running:
            schedule.run_pending()
            time.sleep(1)
