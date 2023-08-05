# -*- coding: utf-8 -*-

import pandas as pd
from ..utils.argchecker import verify_that, apply_rule


class Account:
    """
        账户信息快照，提供调用时刻的实时账户信息
        公有属性:
        ::
            name: str: 账户名称
            account_idx: int 账户索引
            type: int 账户类型
        ..
        公有方法:
        ::
            position:获取指定标的和方向的仓位信息
            positions: 获得所有仓位的双向仓位信息
            cash: 获得账户的资金信息
        ..
    """

    def __init__(self, account_idx, acc_type, name, env):
        self.name = name
        self.account_idx = account_idx
        self.account_type = acc_type
        self._snap = None
        self._env = env

    @property
    def positions(self) -> 'pd.DataFrame':
        """ 账户的双向仓位信息

        :return: pandas.df or OrderDict 双向持仓信息
        """
        return self._snap.positions(self.account_idx, True)

    @property
    def cash(self) -> 'pd.DataFrame':
        """ 账户的资金信息

        :return: pandas.df or OrderDict 账户资金信息
        """
        return self._snap.cash(self.account_idx, True)

    @apply_rule(verify_that('target_idx').is_instance_of(int, list, tuple))
    def position(self, target_idx=(), side=0, df=True) -> 'pd.DataFrame':
        """
        从positions中构建position
        :param target_idx: 标的索引
        :param side: 持仓方向
        :param df: 是否生成dataframe对象
        :return: df or OrderDict position对象
        """
        if isinstance(target_idx, int):
            target_idx = [target_idx]
        if len(target_idx) < 1:
            target_idx = list(range(self._env.target_idx_count()))
        else:
            _, target_idx = self._env.check_idx('position', None, target_idx, False)
        return self._snap.position(self.account_idx, target_idx, side, df)


class Order:
    def __init__(self):
        self.account_name = None
        self.account_idx = None
        self.order_id = None
        self.order_id_broker = None
        self.code = None
        self.target_idx = None
        self.side = None
        self.position_effect = None
        self.order_type = None
        self.source = None
        self.status = None
        self.rej_reason = float('nan')
        self.price = None
        self.volume = None
        self.value = None
        self.filled_volume = None
        self.filled_average = None
        self.filled_amount = None
        self.created = None
        self.updated = None


class Execution:
    def __init__(self):
        self.account_name = None
        self.account_idx = None
        self.order_id = None
        self.order_id_broker = None
        self.trade_id = None
        self.code = None
        self.target_idx = None
        self.position_effect = None
        self.side = None
        self.price = None
        self.source = None
        self.volume = None
        self.amount = None
        self.created = None


class Context:
    """
    用途：存储用户定义的各类全局变量
          可以在策略中获取的系统信息

    公有属性:
        ::
            account_list：dict 账户列表
            target_list: dict 标的列表
            backtest_setting: dict 回测参数列表
            reg_kdata: list 注册Kdata的索引
            reg_factor: list 注册因子的索引
            reg_userindi: list 注册用户因子的索引
            reg_userdata: list 用户添加函数的索引
            account: df 账户信息，调用方法
                context.account(idx=0): idx int 账户索引
            now: datetime 回测过程返回的是刷新时间点，实盘模式返回的是本地时间点
        ..
    实现说明：
        1、account_list target_list backtest_setting reg_kdata reg_factor reg_userindi reg_userdata 在回测接口中填充并保存
        2、account做成一个函数引用，用于获取调用时刻的账户快照
        3、允许用户向context中添加新的属性(包括函数引用和变量)
        4、避免覆盖系统定义的变量名
    """

    def __init__(self):
        self.day_begin = False
        self.account_list = []
        self.target_list = []
        self.backtest_setting = {}
        self.reg_kdata = []
        self.reg_factor = []
        self.reg_userindi = []
        self.reg_userdata = []
        self.now = None
        self._snap = None
        # 生成 account 列表
        self._acc_snapshot_list = None

    def _init_acc_snapshot(self, env, snap_):
        """ 生成Account对象列表

        """
        self._snap = snap_
        self._acc_snapshot_list = snap_.init_acc_snapshot(env)
        [setattr(o, '_snap', snap_) for o in self._acc_snapshot_list]

    def account(self, account_idx=0) -> 'Account':
        """根据账户索引获取账户信息

        :param account_idx: 账户索引，默认为0 也就是第一个账户的信息
        :return: Account对象
        """

        return self._acc_snapshot_list[account_idx]
