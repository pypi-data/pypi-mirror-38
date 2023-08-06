

inquant future quant api

# -*- coding: utf-8 -*-
from StrategyTemplate import *

class MyStrategy(StrategyTemplate):
    """�ҵĲ���"""

    def __init__(self):
        """���캯��"""
        super(MyStrategy,self).__init__()

    def OnTick(self, data):
        """Tick���ݴ��� עdata����һ��ֻ��һ��tick����"""
        print("tickqqqqq",data.Symbol,data.LocalTime,data.Exchange)

        pass

    def OnBar(self, data):
        """Bar���ݴ��� עdata����һ��ֻ��һ��bar����"""
        print("bar",data.Symbol,data.LocalTime,data.Exchange)

        resp10 = strategy.GetLastBar('rb1901',Exchange.SHFE,60,5)

        print(resp10[0].Symbol,resp10[0].LocalTime)
        pass

    def OnOrderChanged(self,order):
        """�ɽ��ر�����"""
        pass

    def TaskCallback(self):
        print(datetime.now().time())

if __name__ == '__main__':

    #�½�����
    strategy = MyStrategy()

    #������ʱ����
    strategy.CreateScheduler(strategy.TaskCallback,[90000,161005])

    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,-1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,0)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,2)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,3)

    strategy.WriteInfo(u"��ʼ��ʼ������...")
    #��ʼ��
    ret = strategy.Init("demo.json","d:\\strategylog\\")
    if not ret:
        strategy.WriteError("u��ʼ������ʧ�ܣ�����")
        input(u"��������˳�")
        sys.exit()
    strategy.WriteInfo(u"��ʼ�����Գɹ�")

    strategy.WriteInfo(u"��ʼ��������...")
    resp = strategy.Start()
    if not resp:
        strategy.WriteError(u"��������ʧ�ܣ���")
        input(u"��������˳�")
        sys.exit()
    strategy.WriteInfo(u"���������ɹ�")

    resp4 = strategy.SendOrder('rb1901',Exchange.SHFE,OrderSide.Buy,4166,1,OrderType.LMT,Offset.Open)
    resp5 = strategy.CancelOrder('7ba0ab1c8319442299c835269f600f3f')

    resp1 = strategy.GetAssetInfo()
    resp2 = strategy.GetOrders()
    resp3 = strategy.GetPositions()
        
    resp6 = strategy.GetOrder('7ba0ab1c8319442299c835269f600f3f')
    resp7 = strategy.GetOpenOrders()
    resp8 = strategy.GetContract('rb1901',Exchange.SHFE)
    resp9 = strategy.GetLastTick('rb1901',Exchange.SHFE,2)
    resp10 = strategy.GetLastBar('rb1901',Exchange.SHFE,300,5)

    input(u"����ִ���У���������˳�...")
