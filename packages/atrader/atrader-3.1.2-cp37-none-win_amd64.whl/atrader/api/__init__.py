# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:54:05 2018

@author: kunlin.l
"""

from collections import Iterable
from datetime import datetime
from atrader import pd, np, enums
from ..basic import env, gv, vr
from . import apiset
from .. import convertor as cvt
from ..utils.language import text
from ..utils.datetimefunc import to_datetime, datetime_to_mft, to_int_now_date, is_format_dt, str_date_to_mft
from ..utils.argchecker import apply_rule, verify_that

NONETYPE = type(None)
CALLABLETYPE = type(lambda x: x)


################################
# 运行模式

@env.force_mode(gv.RUNMODE_CONSOLE)
@env.force_phase(gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('strategy_name').is_instance_of(str),
            verify_that('file_path').is_exist_path(),
            verify_that('target_list').is_instance_of(Iterable),
            verify_that('frequency').is_valid_frequency(),
            verify_that('fre_num').is_instance_of(int).is_greater_than(0),
            verify_that('begin_date').is_instance_of((str, datetime)).is_valid_date(),
            verify_that('end_date').is_instance_of((str, datetime)).is_valid_date(),
            verify_that('fq').is_instance_of(int).is_valid_fq())
def run_backtest(strategy_name='',
                 file_path='',
                 target_list=(),
                 frequency='day',
                 fre_num=1,
                 begin_date='',
                 end_date=0,
                 fq=0):
    config = {
        'entry': {
            'strategy_name': strategy_name,
            'strategy_path': file_path,
            'targets': target_list,
            'frequency': frequency,
            'freq_num': fre_num,
            'begin_date': begin_date,
            'end_date': end_date,
            'fq': fq
        }
    }

    from ._mode_back import run_backtest
    return run_backtest(config)


################################
# ATCore 交互


@env.force_phase(gv.RUMMODE_PHASE_DEFAULT)
def clear_cache():
    import os, shutil
    print(text.LOG_CLEAN_CACHE)
    root_dir = env.root_sub_dir()
    for d in os.listdir(root_dir):
        try:
            if d.startswith('record_'):
                shutil.rmtree(os.path.join(root_dir, d))
        except OSError:
            pass
    env.cls_root_sub_dir('mat')
    print(text.LOG_CLEAN_CACHE_END)


#################################

# 数据注册


@env.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('frequency').is_valid_frequency(),
            verify_that('fre_num').is_instance_of(int),
            verify_that('adjust').is_in((True, False)))
def reg_kdata(frequency: 'str',
              fre_num: 'int',
              adjust=False):
    print(text.LOG_REG_REG_KDATA)
    if frequency in ('day', 'tick', 'week', 'month', 'year') and fre_num != 1:
        raise ValueError(text.ERROR_SUPPORT_MULTI_FREQUENCY.format(FREQUENCY=frequency))
    idx = apiset.reg_k_data(frequency, fre_num, adjust)
    print(text.LOG_REG_REG_KDATA_END)
    env.user_context.reg_kdata.append(idx)


@env.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('factor').is_instance_of(str, list, tuple))
def reg_factor(factor: 'list'):
    if isinstance(factor, str):
        factor = [factor]
    if len(factor) < 1:
        raise ValueError(text.ERROR_INPUT_FACTOR_TOTAL)

    print(text.LOG_REG_REG_FACTOR)
    strategy_input = env.get_strategy_input()
    reg_idx = apiset.reg_factor(factor,
                                strategy_input['TargetList'],
                                strategy_input['BeginDate'],
                                strategy_input['EndDate'])
    print(text.LOG_REG_REG_FACTOR_END)
    env.user_context.reg_factor.append({'reg_idx': reg_idx, 'factor': list(factor)})


@env.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('timeline').is_instance_of(list, tuple),
            verify_that('data').is_instance_of(list, tuple))
def reg_userdata(timeline, data):
    if len(timeline) != len(data):
        raise ValueError(text.ERROT_INPUT_USER_DATA_TIMELINE_DATALEN)

    if len(timeline) < 1:
        raise ValueError(text.ERROR_EMPTY_TIME_LINE)

    if isinstance(timeline[0], str):
        in_fmt = '%Y-%m-%d' if is_format_dt(timeline[0], '%Y-%m-%d') else '%Y-%m-%d %H:%M:%S'
        new_time_line = str_date_to_mft(timeline, format=in_fmt)
    else:
        new_time_line = datetime_to_mft(timeline)

    print(text.LOG_REG_REG_USERDATA)
    reg_idx = apiset.reg_user_data(np.array(new_time_line), np.array(data))
    print(text.LOG_REG_REG_USERDATA_END)
    env.user_context.reg_userdata.append(reg_idx)


@env.force_phase(gv.RUMMODE_PHASE_USERINIT)
@apply_rule(verify_that('indi_func').is_instance_of(CALLABLETYPE))
def reg_userindi(indi_func):
    print(text.LOG_REG_REG_USERINDI)
    reg_idx = apiset.reg_userindi(indi_func)
    print(text.LOG_REG_REG_USERINDI_END)
    env.user_context.reg_userindi.append(reg_idx)


#################################

# 非策略结构使用函数

@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('block').is_instance_of(str),
            verify_that('date').is_valid_date(allow_empty_str=True))
def get_code_list(block: 'str', date=''):
    blocks = str.lower(block).strip().split(',')
    if isinstance(date, str) and date.strip() == '':
        new_date = to_int_now_date('%Y%m%d')
    else:
        new_date = cvt.convert_str_or_datetime_to_int_date(date)
    ls = apiset.get_code_list(blocks, new_date)

    return cvt.convert_code_list_to_df(ls)


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('factor').is_instance_of(str),
            verify_that('target_list').is_instance_of(str, tuple, list),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date())
def get_factor_by_factor(factor: 'str',
                         target_list: 'list',
                         begin_date,
                         end_date):
    if isinstance(target_list, str):
        target_list = [target_list]

    targets = env.check_target(cvt.todictmc(target_list))
    new_begin_date = cvt.convert_str_or_datetime_to_int_date(begin_date)
    new_end_date = cvt.convert_str_or_datetime_to_int_date(end_date)
    if begin_date != 0 and new_begin_date > new_end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    factor_dict = apiset.get_factor_by_factor(factor, targets, new_begin_date, new_end_date)
    result_df = cvt.convert_factor_by_factor_to_df(factor_dict, cvt.todotmc(targets))
    return result_df


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('factor_list').is_instance_of(str, tuple, list),
            verify_that('target_list').is_instance_of(str, tuple, list),
            verify_that('date').is_valid_date(allow_empty_str=True))
def get_factor_by_day(factor_list: 'list',
                      target_list: 'list',
                      date=''):
    if isinstance(factor_list, str):
        factor_list = [factor_list]

    if isinstance(target_list, str):
        target_list = [target_list]

    targets = env.check_target(cvt.todictmc(target_list))
    if date == '':
        new_date = to_int_now_date()
    else:
        new_date = cvt.convert_str_or_datetime_to_int_date(date)
    factor_dict = apiset.get_factor_by_day(factor_list, targets, new_date)
    factor_df = cvt.convert_factor_by_day_to_df(factor_dict) if factor_dict is not None else None

    return factor_df


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('factor_list').is_instance_of(str, tuple, list),
            verify_that('target').is_instance_of(str),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date())
def get_factor_by_code(factor_list: 'list',
                       target: 'str',
                       begin_date,
                       end_date):
    if isinstance(factor_list, str):
        factor_list = [factor_list]

    targets = env.check_target(cvt.todictmc([target]))
    new_begin_date = cvt.convert_str_or_datetime_to_int_date(begin_date)
    new_end_date = cvt.convert_str_or_datetime_to_int_date(end_date)
    if begin_date != 0 and new_begin_date > new_end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    factor_dict = apiset.get_factor_by_code(factor_list, targets, new_begin_date, new_end_date)
    factor_df = cvt.convert_factor_by_code_to_df(factor_dict) if factor_dict is not None else None
    return factor_df


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(list, tuple, str),
            verify_that('frequency').is_in(('day', 'week', 'month', 'min')),
            verify_that('fre_num').is_instance_of(int),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date(),
            verify_that('fq').is_in((enums.FQ_NA,
                                     enums.FQ_FORWARD,
                                     enums.FQ_BACKWARD)),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by_date').is_in((True, False)))
def get_kdata(target_list: 'list',
              frequency: 'str',
              fre_num: 'int',
              begin_date,
              end_date,
              fq=enums.FQ_NA,
              fill_up=False,
              df=False,
              sort_by_date=False):
    if isinstance(target_list, str):
        target_list = [target_list]

    if len(target_list) < 1:
        raise ValueError(text.ERROR_INPUT_EMPTY_PARAM.format(PARAMNAME='target_list'))

    begin_date = cvt.convert_str_or_datetime_to_int_date(begin_date)
    end_date = cvt.convert_str_or_datetime_to_int_date(end_date)
    new_targets = cvt.todictmc(target_list)
    fq = cvt.convert_internal_fq_to_atcore(fq)

    if frequency in ('day', 'week', 'month') and fre_num != 1:
        raise ValueError(text.ERROR_INPUT_FREQUENCY_FREQNUM)

    if 0 < end_date < begin_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    results = [None] * len(new_targets)
    data_list = apiset.get_k_data(new_targets, frequency, fre_num, begin_date, end_date, fill_up, fq)
    for idx, data in enumerate(data_list):
        results[idx] = cvt.convert_k_data_to_df(data, target_list[idx],
                                                env.get_target_type(cvt.todotmc(new_targets[idx])))

    if df:
        data_df = pd.concat(results, ignore_index=True)  # type: pd.DataFrame
        if sort_by_date:
            data_df = data_df.sort_values('time', ascending=True, na_position='first')  # type: pd.DataFrame
            data_df.index = range(data_df.shape[0])
        return data_df
    else:
        return {target: results[idx] for idx, target in enumerate(target_list)}


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(str, list, tuple),
            verify_that('frequency').is_in(('day', 'week', 'month', 'min')),
            verify_that('fre_num').is_instance_of(int),
            verify_that('end_date').is_valid_date(allow_empty_str=True),
            verify_that('n').is_instance_of(int).is_greater_than(0).is_less_than(1000),
            verify_that('fq').is_in((enums.FQ_NA, enums.FQ_BACKWARD, enums.FQ_FORWARD)),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by_time').is_in((True, False)))
def get_kdata_n(target_list: 'list',
                frequency: 'str',
                fre_num: 'int',
                n: 'int',
                end_date: 'str',
                fq=0,
                fill_up=False,
                df=False,
                sort_by_time=False):
    if isinstance(target_list, str):
        target_list = [target_list]

    if len(target_list) < 1:
        raise ValueError(text.ERROR_INPUT_EMPTY_PARAM.format(PARAMNAME='target_list'))

    if isinstance(end_date, str) and end_date.strip() == '':
        end_date = to_int_now_date('%Y%m%d')
    else:
        end_date = cvt.convert_str_or_datetime_to_int_date(end_date)

    new_targets = cvt.todictmc(target_list)
    fq = cvt.convert_internal_fq_to_atcore(fq)

    if frequency in ('day', 'week', 'month') and fre_num != 1:
        raise ValueError(text.ERROR_INPUT_FREQUENCY_FREQNUM)

    results = [None] * len(new_targets)
    for idx, target in enumerate(new_targets):
        kdata = apiset.get_k_data_n([target], frequency, fre_num, n, end_date, fill_up, fq)
        results[idx] = cvt.convert_k_data_to_df(kdata[0], target_list[idx], env.get_target_type(cvt.todotmc(target)))

    if df:
        data_df = pd.concat(results, ignore_index=True)  # type: pd.DataFrame
        if sort_by_time:
            data_df = data_df.sort_values('time', ascending=True, na_position='first')  # type: pd.DataFrame
            data_df.index = range(data_df.shape[0])
        return data_df
    else:
        return {target: results[idx] for idx, target in enumerate(target_list)}


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('main_code').is_instance_of(str),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_main_contract(main_code: 'str',
                      begin_date,
                      end_date):
    begin_date = cvt.convert_str_or_datetime_to_int_date(begin_date)
    if isinstance(end_date, str) and end_date.strip() == '':
        end_date = to_int_now_date('%Y%m%d')
    else:
        end_date = cvt.convert_str_or_datetime_to_int_date(end_date)
    new_targets = cvt.todictmc(main_code)

    if begin_date > end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    ls = apiset.get_main_contract(new_targets['Market'], new_targets['Code'], begin_date, end_date)

    return cvt.convert_main_contract_to_df(ls, new_targets['Market'])


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('market').is_instance_of(str),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_trading_days(market: 'str',
                     begin_date,
                     end_date=''):
    # TODO market: 支持数字货币
    new_begin_date = cvt.convert_str_or_datetime_to_int_date(begin_date)
    if isinstance(end_date, str) and end_date.strip() == '':
        new_end_date = to_int_now_date('%Y%m%d')
    else:
        new_end_date = cvt.convert_str_or_datetime_to_int_date(end_date)
    if new_begin_date > new_end_date:
        return None

    result = apiset.get_trading_days_condition(market, new_begin_date, new_end_date)
    if result.size < 1:
        return None

    return cvt.convert_trading_days_to_np_datetime(result)


@env.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(str, tuple, list),
            verify_that('frequency').is_in(('day', 'week', 'month', 'min')),
            verify_that('fre_num').is_instance_of(int),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_trading_time(target_list: 'list',
                     frequency: 'str',
                     fre_num: 'int',
                     begin_date,
                     end_date=''):
    if isinstance(target_list, str):
        target_list = [target_list]

    new_targets = cvt.todictmc(target_list)
    new_begin_date = cvt.convert_str_or_datetime_to_int_date(begin_date)
    if isinstance(end_date, str) and end_date.strip() == '':
        new_end_date = to_int_now_date('%Y%m%d')
    else:
        new_end_date = cvt.convert_str_or_datetime_to_int_date(end_date)

    if frequency in ('day', 'week', 'month') and fre_num != 1:
        raise ValueError(text.ERROR_INPUT_FREQUENCY_FREQNUM)

    if 0 < new_end_date < new_begin_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    t, d = apiset.get_trading_time(new_targets, frequency, new_begin_date, new_end_date, fre_num)

    if gv.freuency_to_int(frequency) >= gv.KFreq_Day:
        d = np.arange(0, t.size, 1, dtype=np.int)
    else:
        d -= 1

    return cvt.convert_trading_time_to_df(t, d)


#################################

# 策略结构使用函数


@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('target_indices').is_instance_of(int, list, tuple))
def get_current_bar(target_indices=()):
    if not isinstance(target_indices, np.ndarray):
        target_indices = np.array([target_indices]).ravel()
    if len(target_indices) < 1:
        target_indices = vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = env.check_idx('get_current_bar', None, target_indices, toarray=True)
    result = apiset.get_bar(target_indices)

    return cvt.convert_current_bar_to_df(result)


@env.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('target_indices').is_instance_of(list, int, tuple),
            verify_that('length').is_greater_than(0),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)))
def get_reg_kdata(reg_idx,
                  target_indices=(),
                  length=1,
                  fill_up=False,
                  df=False):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) == 0:
        target_indices = vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = env.check_idx('get_reg_kdata', None, target_indices, toarray=True)
    new_reg_idx = np.full((target_indices.size, 6), np.nan)
    for i, idx in enumerate(target_indices):
        new_reg_idx[i, :] = reg_idx[idx, :]

    if len(new_reg_idx) < 1 or new_reg_idx.size < 1:
        raise ValueError(text.ERROR_REG_IDX_PARAM)

    bar_pos = env.get_internal_fresh_bar_num(np.nan)
    result = apiset.get_reg_kdata(new_reg_idx.reshape((-1, 6)), bar_pos, length, fill_up).T

    columns = ['target_idx', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'open_interest']
    if df:
        data_df = pd.DataFrame(result, columns=columns)
        return data_df
    else:
        d = {}
        for idx, target_idx in enumerate(target_indices):
            s, e = idx * length, (idx + 1) * length
            d[idx] = pd.DataFrame(result[s:e], columns=columns)
        return d


@env.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('target_indices').is_instance_of(list, int, tuple),
            verify_that('length').is_greater_than(0),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)))
def get_reg_kdata_adj(reg_idx,
                      target_indices=(),
                      length=1,
                      fill_up=False,
                      df=False):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) == 0:
        target_indices = vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = env.check_idx('get_reg_kdata', None, target_indices, toarray=True)
    new_reg_idx = np.full((target_indices.size, 6), np.nan)
    for i, idx in enumerate(target_indices):
        new_reg_idx[i, :] = reg_idx[idx, :]

    if len(new_reg_idx) < 1 or new_reg_idx.size < 1:
        raise ValueError(text.ERROR_REG_IDX_PARAM)

    bar_pos = env.get_internal_fresh_bar_num(np.nan)
    result = apiset.get_reg_kdata_adj(new_reg_idx.reshape((-1, 6)), bar_pos, length, fill_up).T
    columns = ['target_idx', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount', 'open_interest']
    if df:
        data_df = pd.DataFrame(result, columns=columns)
        return data_df
    else:
        d = {}
        for idx, target_idx in enumerate(target_indices):
            s, e = idx * length, (idx + 1) * length
            d[idx] = pd.DataFrame(result[s:e], columns=columns)
        return d


@env.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('reg_idx').is_instance_of(dict),
            verify_that('length').is_greater_than(0),
            verify_that('target_indices').is_instance_of(list, int, tuple),
            verify_that('length').is_instance_of(int).is_greater_than(0),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by').is_in(('factor', 'target_idx', 'date')))
def get_reg_factor(reg_idx,
                   target_indices=(),
                   length=1,
                   df=False,
                   sort_by='target_idx'):
    if isinstance(target_indices, int):
        target_indices = [target_indices]
    if len(target_indices) < 1:
        target_indices = vr.g_ATraderCache['input_targets_idx_range']
    else:
        _, target_indices = env.check_idx('get_reg_factor', None, target_indices, toarray=True)

    factor = reg_idx.get('factor', [])
    reg_idx_ = reg_idx.get('reg_idx')[:, target_indices].ravel()
    bar_pos = env.get_internal_fresh_bar_num(np.nan)
    dt, value = apiset.get_reg_factor(reg_idx_, bar_pos, length)

    if df:
        data_df = cvt.convert_reg_factor_to_df(dt, value, target_indices, factor).sort_values(
            sort_by, ascending=True, na_position='first')  # type: pd.DataFrame
        data_df.index = range(data_df.shape[0])
        return data_df
    else:
        data_dict = cvt.convert_reg_factor_to_dict(dt, value, target_indices, factor)
        return data_dict


@env.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('reg_idx').is_instance_of(np.ndarray),
            verify_that('length').is_instance_of(int).is_greater_than(0))
def get_reg_userdata(reg_idx,
                     length=1):
    bar_pos = env.get_internal_fresh_bar_num(np.nan)
    datetime_tl, value = apiset.get_reg_userdata(reg_idx, bar_pos, length)

    return cvt.convert_reg_userdata_to_df(datetime_tl, value)


@env.force_phase(gv.RUMMODE_PHASE_USERINDI,
                 gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('length').is_instance_of(int))
def get_reg_userindi(reg_idx,
                     length=1) -> 'pd.DataFrame':
    bar_pos = env.get_internal_fresh_bar_num(np.nan)
    t, v = apiset.get_reg_user_indicator(reg_idx, bar_pos, length)

    return cvt.convert_user_indi_to_df(t, v)


#################################

# 回测细节设置

@env.force_phase(gv.RUMMODE_PHASE_USERINIT)
@env.force_mode(gv.RUNMODE_BACKTEST)
@apply_rule(verify_that('initial_cash').is_greater_than(0.0),
            verify_that('future_cost_fee').is_greater_than(0.0),
            verify_that('stock_cost_fee').is_greater_than(0.0),
            verify_that('rate').is_greater_than(0.0),
            verify_that('margin_rate').is_greater_than(0.0),
            verify_that('slide_price').is_greater_or_equal_than(0.0),
            verify_that('price_loc').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('deal_type').is_in((enums.MARKETORDER_DIRECT,
                                            enums.MARKETORDER_NONME_BEST_PRICE,
                                            enums.MARKETORDER_ME_BEST_PRICE)),
            verify_that('limit_type').is_in((enums.LIMITORDER_DIRECT,
                                             enums.LIMITORDER_NOPRICE_CANCEL)))
def set_backtest(initial_cash=1e7,
                 future_cost_fee=1.0,
                 stock_cost_fee=2.5,
                 rate=0.02,
                 margin_rate=1.0,
                 slide_price=0.0,
                 price_loc=1,
                 deal_type=0,
                 limit_type=0):
    return apiset.set_back_test(initial_cash, future_cost_fee, stock_cost_fee, rate,
                                margin_rate, slide_price, price_loc, deal_type, limit_type)


#################################

# 交易函数: 普通下单指令

@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('volume').is_instance_of(int),
            verify_that('side').is_in((enums.ORDERSIDE_BUY, enums.ORDERSIDE_SELL)),
            verify_that('position_effect').is_in((enums.ORDERPOSITIONEFFECT_OPEN,
                                                  enums.ORDERPOSITIONEFFECT_CLOSE,
                                                  enums.ORDERPOSITIONEFFECT_CLOSETODAY)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET)),
            verify_that('price').is_greater_or_equal_than(0))
def order_volume(account_idx: 'int',
                 target_idx: 'int',
                 volume: 'int',
                 side: 'int',
                 position_effect: 'int',
                 order_type: 'int',
                 price=0.0):
    account_idx, target_idx = env.check_idx('order_volume', account_idx, target_idx, toarray=False)
    return apiset.order_volume(account_idx, target_idx, volume, side, position_effect, order_type, price)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('value').is_greater_than(0),
            verify_that('side').is_in((enums.ORDERSIDE_BUY, enums.ORDERSIDE_SELL)),
            verify_that('position_effect').is_in((enums.ORDERPOSITIONEFFECT_OPEN,
                                                  enums.ORDERPOSITIONEFFECT_CLOSE,
                                                  enums.ORDERPOSITIONEFFECT_CLOSETODAY)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET,
                                             enums.ORDERTYPE_FAK,
                                             enums.ORDERTYPE_FOK,
                                             enums.ORDERTYPE_BOC,
                                             enums.ORDERTYPE_BOP,
                                             enums.ORDERTYPE_B5TC,
                                             enums.ORDERTYPE_B5TL)),
            verify_that('price').is_greater_or_equal_than(0))
def order_value(account_idx: 'int',
                target_idx: 'int',
                value: 'float',
                side: 'int',
                position_effect: 'int',
                order_type: 'int',
                price=0.0):
    account_idx, target_idx = env.check_idx('order_value', account_idx, target_idx, toarray=False)
    return apiset.order_value(account_idx, target_idx, value, side, position_effect, order_type, price)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('percent').is_greater_than(0).is_less_or_equal_than(1),
            verify_that('side').is_in((enums.ORDERSIDE_BUY,
                                       enums.ORDERSIDE_SELL)),
            verify_that('position_effect').is_in((enums.ORDERPOSITIONEFFECT_OPEN,
                                                  enums.ORDERPOSITIONEFFECT_CLOSE,
                                                  enums.ORDERPOSITIONEFFECT_CLOSETODAY)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET,
                                             enums.ORDERTYPE_FAK,
                                             enums.ORDERTYPE_FOK,
                                             enums.ORDERTYPE_BOC,
                                             enums.ORDERTYPE_BOP,
                                             enums.ORDERTYPE_B5TC,
                                             enums.ORDERTYPE_B5TL)),
            verify_that('price').is_greater_or_equal_than(0))
def order_percent(account_idx: 'int',
                  target_idx: 'int',
                  percent: 'float',
                  side: 'int',
                  position_effect: 'int',
                  order_type: 'int',
                  price=0.0):
    account_idx, target_idx = env.check_idx('order_percent', account_idx, target_idx, toarray=False)
    return apiset.order_percent(account_idx, target_idx, percent, side, position_effect, order_type, price)


#################################

# 交易函数: 目标下单指令

@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('target_volume').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('side').is_in((enums.POSITIONSIDE_LONG, enums.POSITIONSIDE_SHORT)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET,
                                             enums.ORDERTYPE_FAK,
                                             enums.ORDERTYPE_FOK,
                                             enums.ORDERTYPE_BOC,
                                             enums.ORDERTYPE_BOP,
                                             enums.ORDERTYPE_B5TC,
                                             enums.ORDERTYPE_B5TL)),
            verify_that('price').is_greater_or_equal_than(0))
def order_target_volume(account_idx: 'int',
                        target_idx: 'int',
                        target_volume: 'int',
                        side: 'int',
                        order_type: 'int',
                        price=0.0):
    handle_idx, target_idx = env.check_idx('order_target_value', account_idx, target_idx, toarray=False)
    return apiset.order_target_volume(account_idx, target_idx, target_volume, side, order_type, price)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('target_value').is_greater_or_equal_than(0),
            verify_that('side').is_in((enums.POSITIONSIDE_SHORT, enums.POSITIONSIDE_LONG)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET,
                                             enums.ORDERTYPE_FAK,
                                             enums.ORDERTYPE_FOK,
                                             enums.ORDERTYPE_BOC,
                                             enums.ORDERTYPE_BOP,
                                             enums.ORDERTYPE_B5TC,
                                             enums.ORDERTYPE_B5TL)),
            verify_that('price').is_greater_or_equal_than(0))
def order_target_value(account_idx: 'int',
                       target_idx: 'int',
                       target_value: 'float',
                       side: 'int',
                       order_type: 'int',
                       price=0.0):
    handle_idx, target_idx = env.check_idx('order_target_value', account_idx, target_idx, toarray=False)
    return apiset.order_target_value(account_idx, target_idx, target_value, side, order_type, price)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('target_percent').is_greater_than(0).is_less_or_equal_than(1),
            verify_that('side').is_in((enums.ORDERSIDE_BUY, enums.ORDERSIDE_SELL)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET,
                                             enums.ORDERTYPE_FAK,
                                             enums.ORDERTYPE_FOK,
                                             enums.ORDERTYPE_BOC,
                                             enums.ORDERTYPE_BOP,
                                             enums.ORDERTYPE_B5TC,
                                             enums.ORDERTYPE_B5TL)),
            verify_that('price').is_greater_or_equal_than(0))
def order_target_percent(account_idx: 'int',
                         target_idx: 'int',
                         target_percent: 'float',
                         side: 'int',
                         order_type: 'int',
                         price=0.0):
    handle_idx, target_idx = env.check_idx('order_target_percent', account_idx, target_idx, toarray=False)
    return apiset.order_target_percent(account_idx, target_idx, target_percent, side, order_type, price)


#################################

# 交易函数: 撤销委托指令

@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('orders').is_instance_of(list))
def order_cancel(orders: 'list'):
    return apiset.order_cancel(orders)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
def order_cancel_all():
    return apiset.order_cancel_all()


#################################

# 交易函数: 一键平仓指令
@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
def order_close_all():
    return apiset.order_close_all()


#################################

# 交易函数: 委托单查询函数
@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('order_list').is_instance_of(int, list, tuple))
def get_order_info(order_list=()):
    if isinstance(order_list, int):
        order_list = [order_list]
    strategy_input = env.get_strategy_input()
    ls = apiset.order_info(order_list)
    return cvt.convert_order_to_df(ls,
                                   strategy_input['AccountNameList'],
                                   strategy_input['TargetList'])


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
def get_unfinished_orders():
    bar_date_s = {int(env.fresh_bar_time)}
    ls = apiset.unfinished_orders(bar_date_s)
    strategy_input = env.get_strategy_input()
    return cvt.convert_unfinished_orders_to_df(ls,
                                               strategy_input['AccountNameList'],
                                               strategy_input['TargetList'])


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
def get_daily_orders():
    bar_date_s = {int(env.fresh_bar_time)}
    ls = apiset.get_orders_by_date(bar_date_s)
    strategy_input = env.get_strategy_input()
    return cvt.convert_daily_orders_to_df(ls,
                                          strategy_input['AccountNameList'],
                                          strategy_input['TargetList'])


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('side').is_in((enums.ORDERSIDE_UNKNOWN,
                                       enums.ORDERSIDE_BUY,
                                       enums.ORDERSIDE_SELL)),
            verify_that('position_effect').is_in((enums.ORDERPOSITIONEFFECT_UNKNOWN,
                                                  enums.ORDERPOSITIONEFFECT_OPEN,
                                                  enums.ORDERPOSITIONEFFECT_CLOSE,
                                                  enums.ORDERPOSITIONEFFECT_CLOSETODAY)))
def get_last_order(account_idx=0,
                   target_idx=0,
                   side=enums.ORDERSIDE_UNKNOWN,
                   position_effect=enums.ORDERPOSITIONEFFECT_UNKNOWN):
    handle_idx, target_idx = env.check_idx('get_last_order', account_idx, target_idx, toarray=False)
    side_set = {side}
    position_effect_set = {position_effect}

    if side == enums.ORDERSIDE_UNKNOWN:
        side_set = {enums.ORDERSIDE_BUY,
                    enums.ORDERSIDE_SELL}

    if position_effect == enums.ORDERPOSITIONEFFECT_UNKNOWN:
        position_effect_set = {enums.ORDERPOSITIONEFFECT_OPEN,
                               enums.ORDERPOSITIONEFFECT_CLOSE,
                               enums.ORDERPOSITIONEFFECT_CLOSETODAY}

    ls = apiset.last_order(handle_idx, target_idx, side_set, position_effect_set)
    if len(ls) < 1:
        return None
    strategy_input = env.get_strategy_input()
    return cvt.convert_last_order_to_df(ls,
                                        strategy_input['AccountNameList'],
                                        strategy_input['TargetList'])


#################################

# 成交查询

@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
def get_daily_executions():
    bar_date_s = {int(env.fresh_bar_time)}
    ls = apiset.get_execution(bar_date_s)
    if len(ls) < 1:
        return None
    strategy_input = env.get_strategy_input()
    return cvt.convert_daily_executions_to_df(ls,
                                              strategy_input['AccountNameList'],
                                              strategy_input['TargetList'])


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('account_idx').is_instance_of(int),
            verify_that('target_idx').is_instance_of(int),
            verify_that('side').is_in((enums.ORDERSIDE_UNKNOWN,
                                       enums.ORDERSIDE_BUY,
                                       enums.ORDERSIDE_SELL)),
            verify_that('position_effect').is_in((enums.ORDERPOSITIONEFFECT_UNKNOWN,
                                                  enums.ORDERPOSITIONEFFECT_OPEN,
                                                  enums.ORDERPOSITIONEFFECT_CLOSE,
                                                  enums.ORDERPOSITIONEFFECT_CLOSETODAY)))
def get_last_execution(account_idx=0,
                       target_idx=0,
                       side=enums.ORDERSIDE_UNKNOWN,
                       position_effect=enums.ORDERPOSITIONEFFECT_UNKNOWN):
    handle_idx, target_idx = env.check_idx('get_last_execution', account_idx, target_idx, toarray=False)
    side_set = {side}
    position_effect_set = {position_effect}

    if side == enums.ORDERSIDE_UNKNOWN:
        side_set = {enums.ORDERSIDE_BUY,
                    enums.ORDERSIDE_SELL}

    if position_effect == enums.ORDERPOSITIONEFFECT_UNKNOWN:
        position_effect_set = {enums.ORDERPOSITIONEFFECT_OPEN,
                               enums.ORDERPOSITIONEFFECT_CLOSE,
                               enums.ORDERPOSITIONEFFECT_CLOSETODAY}

    ls = apiset.last_execution(handle_idx, target_idx, side_set, position_effect_set)
    if len(ls) < 1:
        return None
    strategy_input = env.get_strategy_input()
    return cvt.convert_last_execution_to_df(ls,
                                            strategy_input['AccountNameList'],
                                            strategy_input['TargetList'])


#################################

# 止盈止损函数: byorder 的止盈止损

@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('target_order_id').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('stop_type').is_in((enums.ORDERSTOP_STOP_TYPE_PERCENT,
                                            enums.ORDERSTOP_STOP_TYPE_POINT)),
            verify_that('stop_gap').is_instance_of(int).is_greater_than(0),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET)))
def stop_loss_by_order(target_order_id: 'int',
                       stop_type: 'int',
                       stop_gap: 'int',
                       order_type: 'int'):
    return apiset.stop_loss_by_order(target_order_id,
                                     stop_type,
                                     stop_gap,
                                     order_type)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('target_order_id').is_instance_of(int, NONETYPE),
            verify_that('stop_type').is_in((enums.ORDERSTOP_STOP_TYPE_PERCENT,
                                            enums.ORDERSTOP_STOP_TYPE_POINT)),
            verify_that('stop_gap').is_greater_than(0).is_instance_of(int),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET)))
def stop_profit_by_order(target_order_id: 'int',
                         stop_type: 'int',
                         stop_gap: 'int',
                         order_type: 'int'):
    if target_order_id is None:
        return None

    return apiset.stop_profit_by_order(target_order_id,
                                       stop_type,
                                       stop_gap,
                                       order_type)


@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('target_order_id').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('stop_type').is_in((enums.ORDERSTOP_STOP_TYPE_POINT,
                                            enums.ORDERSTOP_STOP_TYPE_PERCENT)),
            verify_that('stop_gap').is_greater_than(0).is_instance_of(int),
            verify_that('trailing_gap').is_greater_than(0).is_instance_of(int),
            verify_that('trailing_type').is_in((enums.ORDERSTOP_TRAILING_POINT,
                                                enums.ORDERSTOP_TRAILING_PERCENT)),
            verify_that('order_type').is_in((enums.ORDERTYPE_LIMIT,
                                             enums.ORDERTYPE_MARKET)))
def stop_trailing_by_order(target_order_id: 'int',
                           stop_type: 'int',
                           stop_gap: 'int',
                           trailing_gap: 'int',
                           trailing_type: 'int',
                           order_type: 'int'):
    return apiset.stop_trailing_by_order(target_order_id,
                                         stop_type,
                                         stop_gap,
                                         trailing_gap,
                                         trailing_type,
                                         order_type)


#################################

# 止盈止损单查询函数

@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('stop_list').is_instance_of(list, tuple, int))
def get_stop_info(stop_list: 'list') -> 'pd.DataFrame':
    if isinstance(stop_list, int):
        stop_list = [stop_list]

    ls = apiset.stop_info(stop_list)
    if len(ls) < 1:
        return None

    return cvt.convert_stop_info_to_df(ls)


#################################

# 止盈止损单查询
@env.force_mode(gv.RUNMODE_BACKTEST, gv.RUNMODE_REALTRADE)
@env.force_phase(gv.RUMMODE_PHASE_ONDATA)
@apply_rule(verify_that('stop_list').is_instance_of(list, tuple, int))
def stop_cancel(stop_list: 'list'):
    if isinstance(stop_list, int):
        stop_list = [stop_list]

    return apiset.stop_cancel(stop_list)
