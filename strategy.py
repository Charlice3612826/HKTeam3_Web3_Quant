class SimpleStrategy:
    def __init__(self):
        self.name = "简单移动平均策略"
    
    def generate_signal(self, market_data):
        """
        生成交易信号
        返回: 'BUY', 'SELL', 或 'HOLD'
        """
        # 这里实现你的策略逻辑
        # 示例：简单的价格判断
        current_price = market_data.get('lastPrice', 0)
        
        if current_price < 50000:  # 示例条件
            return 'BUY'
        elif current_price > 60000:
            return 'SELL'
        else:
            return 'HOLD'
        
        # 实际竞赛中，这里可以替换为：
        # - 机器学习模型预测
        # - 技术指标计算（RSI, MACD等）
        # - 基于规则的逻辑
