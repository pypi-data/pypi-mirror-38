# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import sys

# noinspection PyUnresolvedReferences
import pandas as pd
# noinspection PyUnresolvedReferences
import numpy as np

# noinspection PyUnresolvedReferences
from .utils.logger import write_syslog, write_userlog, write_log, sys_warning
# noinspection PyUnresolvedReferences
from .utils.utilfunc import load_mat, save_mat, trace_time
# noinspection PyUnresolvedReferences
from .account.snap_mod import *
# noinspection PyUnresolvedReferences
from .api import *
# noinspection PyUnresolvedReferences
from .account import Account, Context
# noinspection PyUnresolvedReferences
from . import setting as atrader_setting

# 不允许换行
pd.set_option('display.expand_frame_repr', False)
# 最大行数 500
pd.set_option('display.max_rows', 500)
# 最大允许列数 35
pd.set_option('display.max_columns', 35)
# 小数显示精度
pd.set_option('precision', 5)
# 绝对值小于0,001统一显示为0.0
pd.set_option('chop_threshold', 0.001)
# 对齐方式
pd.set_option('colheader_justify', 'right')

np.set_printoptions(threshold=np.nan)
np.seterr(all='ignore')


def set_setting(option, value):
    """ 设置 setting 模块的参数
        具体参数见 setting.py 文件
    """

    if hasattr(atrader_setting, option):
        setattr(atrader_setting, option, value)
    else:
        sys_warning('setting module without the attribute `%s`' % option)


def get_setting(option, default=None):
    """ 获取 setting 模块的参数
        具体参数见 setting.py 文件
    """

    return getattr(atrader_setting, option, default)


def get_version():
    """ 获取版本信息"""

    try:
        from .atdef import version
    except ImportError:
        return None
    return version


def get_support():
    """ 获取支持AT客户端版本"""

    try:
        from .atdef import support_at_version
    except ImportError:
        return (None, )
    return support_at_version


__version__ = get_version()
__author__ = 'www.bitpower.com.cn'
__mail__ = 'Contact@bitpower.com.con'
__telephone__ = '0755-86503293'
__address__ = '深圳市南山区粤海街道深圳湾科技生态园6栋413室'
