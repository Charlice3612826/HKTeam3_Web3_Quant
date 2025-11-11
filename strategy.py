import time

class OpeningRangeBreakoutStrategy(BacktestStrategy):
    """15-minute Opening Range Breakout Strategy (optimized version)."""
    def __init__(self, lookback_minutes=90, atr_period=10, atr_multiplier=0.03, cooldown_hours=2):
        super().__init__("Opening Range Breakout Strategy (15m optimized)")
        self.lookback_minutes = lookback_minutes
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.cooldown_hours = cooldown_hours

    def generate_signals(self, data):
        df = data.copy()
        df['date'] = df.index.date
        df['hour'] = df.index.hour

        # Initialize columns
        df['upper'] = np.nan
        df['lower'] = np.nan

        # 1. Calculate opening range (first lookback_minutes of each day)
        bars_in_lookback = int(self.lookback_minutes / 15)  # assuming 15m bars by default
        for date in df['date'].unique():
            day_data = df[df['date'] == date]
            open_period = day_data[day_data['hour'] == 0].head(bars_in_lookback)
            if not open_period.empty:
                upper_val = open_period['high'].max()
                lower_val = open_period['low'].min()
                # Assign the same upper/lower for all rows of that date
                df.loc[df['date'] == date, 'upper'] = upper_val
                df.loc[df['date'] == date, 'lower'] = lower_val

        # 2. Calculate ATR (Average True Range) over atr_period bars
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift(1)).abs()
        low_close  = (df['low'] - df['close'].shift(1)).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = true_range.rolling(self.atr_period).mean()

        # 3. Generate raw signals based on breakout with ATR buffer
        df['signal'] = 0  # default no-trade signal
        df.loc[df['close'] > df['upper'] + self.atr_multiplier * df['ATR'], 'signal'] = 1   # breakout upward
        df.loc[df['close'] < df['lower'] - self.atr_multiplier * df['ATR'], 'signal'] = -1  # breakout downward

        # 4. Implement cooldown: after a signal occurs, suppress further signals for `cooldown_hours`
        df = df.reset_index(drop=False)  # make index a column to use numeric indexing
        last_signal_index = None
        cooldown_bars = int((self.cooldown_hours * 60) / 15)  # number of 15m bars in cooldown period (e.g., 2 hours = 8 bars)
        for i, sig in enumerate(df['signal']):
            if last_signal_index is not None and i <= last_signal_index + cooldown_bars:
                # If within cooldown window after last signal, override to 0 (no trade)
                df.at[i, 'signal'] = 0
            if sig == 1 or sig == -1:
                last_signal_index = i  # update last signal occurrence

        df = df.set_index('index')  # restore original index (datetime index)
        df = df.fillna(0)  # replace any NaN values with 0 (especially in ATR before enough data)
        return df


class QuickTestStrategy:
    def __init__(self):
        self.name = "快速测试策略"
        self.trade_count = 0
        self.last_trade_time = 0
        
    def generate_signal(self, market_data):
        """
        快速测试策略：每分钟交替买卖
        """
        current_time = time.time()
        
        # 每分钟执行一次交易（避免频率限制）
        if current_time - self.last_trade_time < 60:  # 60秒间隔
            return 'HOLD'
        
        self.trade_count += 1
        self.last_trade_time = current_time
        
        print(f"🎯 测试交易 #{self.trade_count}")
        
        # 交替执行买卖：奇数次数买，偶数次数卖
        if self.trade_count % 2 == 1:
            print("➡️ 生成买入信号")
            return 'BUY'
        else:
            print("⬅️ 生成卖出信号")
            return 'SELL'

# 保留原来的SimpleStrategy类作为备用
class SimpleStrategy:
    def __init__(self):
        self.name = "简单移动平均策略"
        self.last_price = None
    
    def generate_signal(self, market_data):
        """
        生成交易信号
        返回: 'BUY', 'SELL', 或 'HOLD'
        """
        if not market_data.get('Success'):
            return 'HOLD'
            
        # 提取行情数据
        ticker = market_data['Data']['BTC/USD']
        current_price = ticker['LastPrice']
        price_change = ticker['Change']  # 24小时价格变化百分比
        
        print(f"价格: ${current_price}, 24小时变化: {price_change*100:.2f}%")
        
        # 简单的策略逻辑
        if price_change < -0.02:  # 如果24小时下跌超过2%
            return 'BUY'
        elif price_change > 0.03:  # 如果24小时上涨超过3%
            return 'SELL'
        else:
            return 'HOLD'
