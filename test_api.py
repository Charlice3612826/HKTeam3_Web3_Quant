#!/usr/bin/env python3
"""
Roostoo API 测试脚本
用于测试API连接和基本功能
"""

import os
import sys
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import RoostooAPIClient

def test_api_connection():
    """测试API连接"""
    print("🔌 开始测试Roostoo API连接...")
    print("=" * 60)
    
    try:
        # 创建客户端实例
        client = RoostooAPIClient()
        print("✅ API客户端创建成功")
        
        # 1. 测试服务器时间
        print("\n1. 测试服务器时间...")
        result = client.get_server_time()
        if 'ServerTime' in result:
            print(f"✅ 服务器时间: {result['ServerTime']}")
        else:
            print(f"❌ 服务器时间获取失败: {result}")
            return False
        
        # 2. 测试交易所信息
        print("\n2. 测试交易所信息...")
        result = client.get_exchange_info()
        if 'IsRunning' in result:
            print(f"✅ 交易所状态: {'运行中' if result['IsRunning'] else '停止'}")
            if 'TradePairs' in result:
                pairs = list(result['TradePairs'].keys())
                print(f"✅ 可交易对: {', '.join(pairs)}")
        else:
            print(f"❌ 交易所信息获取失败: {result}")
            return False
        
        # 3. 测试行情数据（单个交易对）
        print("\n3. 测试BTC/USD行情...")
        result = client.get_ticker('BTC/USD')
        if result.get('Success') and 'Data' in result:
            btc_data = result['Data']['BTC/USD']
            print(f"✅ BTC/USD行情:")
            print(f"   - 最新价: ${btc_data['LastPrice']}")
            print(f"   - 买一价: ${btc_data['MaxBid']}")
            print(f"   - 卖一价: ${btc_data['MinAsk']}")
            print(f"   - 24小时涨跌幅: {btc_data['Change']*100:.2f}%")
        else:
            print(f"❌ BTC行情获取失败: {result}")
            return False
        
        # 4. 测试所有行情数据
        print("\n4. 测试所有交易对行情...")
        result = client.get_ticker()  # 不传参数获取所有
        if result.get('Success') and 'Data' in result:
            total_pairs = len(result['Data'])
            print(f"✅ 共获取 {total_pairs} 个交易对行情")
            for pair, data in result['Data'].items():
                print(f"   📊 {pair}: ${data['LastPrice']} ({data['Change']*100:+.2f}%)")
        else:
            print(f"❌ 所有行情获取失败: {result}")
            return False
        
        # 5. 测试账户余额（需要签名）
        print("\n5. 测试账户余额查询...")
        result = client.get_balance()
        if result.get('Success') and 'Wallet' in result:
            print("✅ 账户余额查询成功:")
            for currency, balance in result['Wallet'].items():
                free = balance['Free']
                locked = balance['Lock']
                if free > 0 or locked > 0:  # 只显示有余额的币种
                    print(f"   💰 {currency}: 可用={free}, 冻结={locked}")
        else:
            print(f"❌ 余额查询失败: {result}")
            # 这里不返回False，因为可能是权限问题而不是连接问题
        
        # 6. 测试挂单查询
        print("\n6. 测试挂单数量查询...")
        result = client.get_pending_count()
        if result.get('Success'):
            total_pending = result['TotalPending']
            print(f"✅ 当前挂单数量: {total_pending}")
            if total_pending > 0:
                print(f"   挂单分布: {result['OrderPairs']}")
        else:
            print(f"ℹ️ 挂单查询: {result.get('ErrMsg', '无挂单')}")
        
        print("\n" + "=" * 60)
        print("🎉 所有API测试完成！")
        print("📋 下一步建议:")
        print("   1. 如果所有测试都通过，可以开始实盘交易")
        print("   2. 如果余额查询失败，请检查API密钥权限")
        print("   3. 可以先小额测试下单功能")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        return False

def test_order_functions():
    """测试订单相关功能（谨慎使用）"""
    print("\n🔐 订单功能测试（需要谨慎）...")
    
    try:
        client = RoostooAPIClient()
        
        # 先查询当前挂单
        print("查询当前挂单...")
        orders = client.query_order(pending_only=True)
        if orders.get('Success') and 'OrderMatched' in orders:
            pending_orders = orders['OrderMatched']
            print(f"当前有 {len(pending_orders)} 个挂单")
            
            # 如果有挂单，测试取消功能
            if pending_orders:
                order_id = pending_orders[0]['OrderID']
                print(f"测试取消订单 {order_id}...")
                result = client.cancel_order(order_id=order_id)
                print(f"取消结果: {result}")
        
        # 测试查询历史订单
        print("\n查询最近3个历史订单...")
        orders = client.query_order(limit=3)
        if orders.get('Success') and 'OrderMatched' in orders:
            history_orders = orders['OrderMatched']
            print(f"最近 {len(history_orders)} 个订单:")
            for order in history_orders:
                status = order['Status']
                side = order['Side']
                pair = order['Pair']
                print(f"  {order['OrderID']}: {pair} {side} {status}")
        
    except Exception as e:
        print(f"订单测试异常: {e}")

if __name__ == "__main__":
    print("Roostoo API 测试脚本")
    print("注意: 这是真实API测试，会访问实际交易账户")
    print()
    
    # 检查环境变量
    load_dotenv()
    api_key = os.getenv('ROOSTOO_API_KEY')
    secret = os.getenv('ROOSTOO_SECRET')
    
    if not api_key or not secret:
        print("❌ 错误: 请在.env文件中配置ROOSTOO_API_KEY和ROOSTOO_SECRET")
        sys.exit(1)
    
    print(f"API Key: {api_key[:10]}...")
    print(f"Secret: {secret[:10]}...")
    print()
    
    # 运行基础连接测试
    if test_api_connection():
        # 询问是否测试订单功能
        response = input("\n是否测试订单功能？(y/N): ").lower()
        if response == 'y':
            test_order_functions()
    
    print("\n测试脚本执行完毕！")
