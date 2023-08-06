"""
Consts and helper functions

Algorithm Environment Variables
-------------------------------

::

    ALGO_MODULE_PATH = ev(
        'ALGO_MODULE_PATH',
        '/opt/sa/analysis_engine/mocks/example_algo_minute.py')
    ALGO_BASE_MODULE_PATH = ev(
        'ALGO_BASE_MODULE_PATH',
        '/opt/sa/analysis_engine/algo.py')
    ALGO_MODULE_NAME = ev(
        'ALGO_MODULE_NAME',
        'example_algo_minute')
    ALGO_VERSION = ev(
        'ALGO_VERSION',
        '1')
    ALGO_BUYS_S3_BUCKET_NAME = ev(
        'ALGO_BUYS_S3_BUCKET_NAME',
        'algobuys')
    ALGO_SELLS_S3_BUCKET_NAME = ev(
        'ALGO_SELLS_S3_BUCKET_NAME',
        'algosells')
    ALGO_RESULT_S3_BUCKET_NAME = ev(
        'ALGO_RESULT_S3_BUCKET_NAME',
        'algoresults')
    ALGO_READY_DATASET_S3_BUCKET_NAME = ev(
        'ALGO_READY_DATASET_S3_BUCKET_NAME',
        'algoready')
    ALGO_EXTRACT_DATASET_S3_BUCKET_NAME = ev(
        'ALGO_EXTRACT_DATASET_S3_BUCKET_NAME',
        'algoready')
    ALGO_HISTORY_DATASET_S3_BUCKET_NAME = ev(
        'ALGO_HISTORY_DATASET_S3_BUCKET_NAME',
        'algohistory')
    ALGO_REPORT_DATASET_S3_BUCKET_NAME = ev(
        'ALGO_REPORT_DATASET_S3_BUCKET_NAME',
        'algoreport')
    ALGO_BACKUP_DATASET_S3_BUCKET_NAME = ev(
        'ALGO_BACKUP_DATASET_S3_BUCKET_NAME',
        'algobackup')
    ALGO_READY_DIR = ev(
        'ALGO_READY_DIR',
        '/tmp')
    ALGO_EXTRACT_DIR = ev(
        'ALGO_EXTRACT_DIR',
        '/tmp')
    ALGO_HISTORY_DIR = ev(
        'ALGO_HISTORY_HISTORY_DIR',
        '/tmp')
    ALGO_REPORT_DIR = ev(
        'ALGO_REPORT_DIR',
        '/tmp')
    ALGO_LOAD_DIR = ev(
        'ALGO_LOAD_DIR',
        '/tmp')
    ALGO_BACKUP_DIR = ev(
        'ALGO_BACKUP_DIR',
        '/tmp')
    ALGO_READY_REDIS_ADDRESS = ev(
        'ALGO_READY_REDIS_ADDRESS',
        'localhost:6379')
    ALGO_EXTRACT_REDIS_ADDRESS = ev(
        'ALGO_EXTRACT_REDIS_ADDRESS',
        'localhost:6379')
    ALGO_HISTORY_REDIS_ADDRESS = ev(
        'ALGO_HISTORY_REDIS_ADDRESS',
        'localhost:6379')
    ALGO_REPORT_REDIS_ADDRESS = ev(
        'ALGO_REPORT_REDIS_ADDRESS',
        'localhost:6379')
    ALGO_BACKUP_REDIS_ADDRESS = ev(
        'ALGO_BACKUP_REDIS_ADDRESS',
        'localhost:6379')

Stock and Analysis Environment Variables
----------------------------------------

::

    TICKER = ev(
        'TICKER',
        'SPY')
    TICKER_ID = int(ev(
        'TICKER_ID',
        '1'))
    DEFAULT_TICKERS = ev(
        'DEFAULT_TICKERS',
        'SPY,AMZN,TSLA,NFLX').split(',')
    NEXT_EXP = analysis_engine.options_dates.option_expiration()
    NEXT_EXP_STR = NEXT_EXP.strftime('%Y-%m-%d')

Logging Environment Variables
-----------------------------

::

    APP_NAME = 'pr'
    LOG_CONFIG_PATH = ev(
        'LOG_CONFIG_PATH',
        './analysis_engine/log/logging.json')

Celery Environment Variables
----------------------------

::

    SLACK_WEBHOOK = ev(
        'SLACK_WEBHOOK',
        None)
    PROD_SLACK_ALERTS = ev(
        'PROD_SLACK_ALERTS',
        '0')
    SSL_OPTIONS = {}
    TRANSPORT_OPTIONS = {}
    WORKER_BROKER_URL = ev(
        'WORKER_BROKER_URL',
        'redis://localhost:6379/13')
    WORKER_BACKEND_URL = ev(
        'WORKER_BACKEND_URL',
        'redis://localhost:6379/14')
    WORKER_CELERY_CONFIG_MODULE = ev(
        'WORKER_CELERY_CONFIG_MODULE',
        'analysis_engine.work_tasks.celery_config')
    WORKER_TASKS = ev(
        'WORKER_TASKS',
        ('analysis_engine.work_tasks.get_new_pricing_data,'
         'analysis_engine.work_tasks.handle_pricing_update_task,'
         'analysis_engine.work_tasks.prepare_pricing_dataset,'
         'analysis_engine.work_tasks.publish_from_s3_to_redis,'
         'analysis_engine.work_tasks.publish_pricing_update,'
         'analysis_engine.work_tasks.task_screener_analysis,'
         'analysis_engine.work_tasks.publish_ticker_aggregate_from_s3'))
    INCLUDE_TASKS = WORKER_TASKS.split(',')

Supported S3 Environment Variables
----------------------------------

::

    ENABLED_S3_UPLOAD = ev(
        'ENABLED_S3_UPLOAD',
        '0') == '1'
    S3_ACCESS_KEY = ev(
        'AWS_ACCESS_KEY_ID',
        'trexaccesskey')
    S3_SECRET_KEY = ev(
        'AWS_SECRET_ACCESS_KEY',
        'trex123321')
    S3_REGION_NAME = ev(
        'AWS_DEFAULT_REGION',
        'us-east-1')
    S3_ADDRESS = ev(
        'S3_ADDRESS',
        'localhost:9000')
    S3_SECURE = ev(
        'S3_SECURE',
        '0') == '1'
    S3_BUCKET = ev(
        'S3_BUCKET',
        'pricing')
    S3_COMPILED_BUCKET = ev(
        'S3_COMPILED_BUCKET',
        'compileddatasets')
    S3_KEY = ev(
        'S3_KEY',
        'test_key')
    DAILY_S3_BUCKET_NAME = ev(
        'DAILY_S3_BUCKET_NAME',
        'daily')
    MINUTE_S3_BUCKET_NAME = ev(
        'MINUTE_S3_BUCKET_NAME',
        'minute')
    QUOTE_S3_BUCKET_NAME = ev(
        'QUOTE_S3_BUCKET_NAME',
        'quote')
    STATS_S3_BUCKET_NAME = ev(
        'STATS_S3_BUCKET_NAME',
        'stats')
    PEERS_S3_BUCKET_NAME = ev(
        'PEERS_S3_BUCKET_NAME',
        'peers')
    NEWS_S3_BUCKET_NAME = ev(
        'NEWS_S3_BUCKET_NAME',
        'news')
    FINANCIALS_S3_BUCKET_NAME = ev(
        'FINANCIALS_S3_BUCKET_NAME',
        'financials')
    EARNINGS_S3_BUCKET_NAME = ev(
        'EARNINGS_S3_BUCKET_NAME',
        'earnings')
    DIVIDENDS_S3_BUCKET_NAME = ev(
        'DIVIDENDS_S3_BUCKET_NAME',
        'dividends')
    COMPANY_S3_BUCKET_NAME = ev(
        'COMPANY_S3_BUCKET_NAME',
        'company')
    PREPARE_S3_BUCKET_NAME = ev(
        'PREPARE_S3_BUCKET_NAME',
        'prepared')
    ANALYZE_S3_BUCKET_NAME = ev(
        'ANALYZE_S3_BUCKET_NAME',
        'analyzed')
    SCREENER_S3_BUCKET_NAME = ev(
        'SCREENER_S3_BUCKET_NAME',
        'screener-data')
    PRICING_S3_BUCKET_NAME = ev(
        'PRICING_S3_BUCKET_NAME',
        'pricing')
    OPTIONS_S3_BUCKET_NAME = ev(
        'OPTIONS_S3_BUCKET_NAME',
        'options')

Supported Redis Environment Variables
-------------------------------------

::

    ENABLED_REDIS_PUBLISH = ev(
        'ENABLED_REDIS_PUBLISH',
        '0') == '1'
    REDIS_ADDRESS = ev(
        'REDIS_ADDRESS',
        'localhost:6379')
    REDIS_KEY = ev(
        'REDIS_KEY',
        'test_redis_key')
    REDIS_PASSWORD = ev(
        'REDIS_PASSWORD',
        None)
    REDIS_DB = int(ev(
        'REDIS_DB',
        '0'))
    REDIS_EXPIRE = ev(
        'REDIS_EXPIRE',
        None)

"""

import os
import sys
import json
import analysis_engine.options_dates


def ev(
        k,
        v):
    '''ev

    :param k: environment variable key
    :param v: environment variable value
    '''
    val = os.getenv(k, v)
    if val:
        return val.strip()
    return val
# end of ev


SUCCESS = 0
FAILED = 1
ERR = 2
EX = 3
NOT_RUN = 4
INVALID = 5
NOT_DONE = 6
NOT_SET = 7
EMPTY = 8
TRADE_OPEN = 9
TRADE_NOT_ENOUGH_FUNDS = 10
TRADE_FILLED = 11
TRADE_NO_SHARES_TO_SELL = 12
TRADE_EXPIRED = 13
TRADE_SHARES = 14
TRADE_VERTICAL_BULL_SPREAD = 15
TRADE_VERTICAL_BEAR_SPREAD = 16
TRADE_PROFITABLE = 17
TRADE_NOT_PROFITABLE = 18
TRADE_HIT_STOP_LOSS = 19
TRADE_HIT_STOP_LOSS_PERCENT = 20
TRADE_HIT_TAILING_STOP_LOSS = 21
TRADE_HIT_TAILING_STOP_LOSS_PERCENT = 22
TRADE_INVALID = 23
TRADE_ERROR = 24
TRADE_ENTRY = 25
TRADE_EXIT = 26
BACKTEST_FOUND_TRADE_PROFITABLE = 27
BACKTEST_FOUND_TRADE_NOT_PROFITABLE = 28
BACKTEST_FOUND_TRADE_NEVER_FILLED = 29  # limit order price never hit
BACKTEST_FOUND_TRADE_EXPIRED = 30  # trades assumed are expired after a day
SPREAD_VERTICAL_BULL = 31
SPREAD_VERTICAL_BEAR = 32
OPTION_CALL = 33
OPTION_PUT = 34
ALGO_PROFITABLE = 35
ALGO_NOT_PROFITABLE = 36
ALGO_ERROR = 37
ALGO_NOT_ACTIVE = 38
S3_FAILED = 39
REDIS_FAILED = 40
FILE_FAILED = 41
SLACK_FAILED = 42
ALGO_HORIZON_UNITS_DAY = 43  # evaluate trade performance on daily-units
ALGO_HORIZON_UNITS_MINUTE = 44  # evaluate trade performance on minutely-units

SA_MODE_PREPARE = 100
SA_MODE_ANALYZE = 101
SA_MODE_PREDICT = 102
SA_MODE_EXTRACT = 103
SA_MODE_SHOW_DATASET = 104
SA_MODE_RESTORE_REDIS_DATASET = 105
SA_MODE_RUN_ALGO = 106

SA_DATASET_TYPE_ALGO_READY = 200

PLOT_ACTION_SHOW = 900
PLOT_ACTION_SAVE_TO_S3 = 901
PLOT_ACTION_SAVE_AS_FILE = 902

FETCH_MODE_ALL = 1000
FETCH_MODE_YHO = 1001
FETCH_MODE_IEX = 1002

# version of python
IS_PY2 = sys.version[0] == '2'
NUM_BYTES_IN_AN_MB = 1048576

APP_NAME = ev(
    'APP_NAME',
    'pr')
LOG_CONFIG_PATH = ev(
    'LOG_CONFIG_PATH',
    './analysis_engine/log/logging.json')
SSL_OPTIONS = {}
TRANSPORT_OPTIONS = {}
WORKER_BROKER_URL = ev(
    'WORKER_BROKER_URL',
    'redis://localhost:6379/13')
WORKER_BACKEND_URL = ev(
    'WORKER_BACKEND_URL',
    'redis://localhost:6379/14')
WORKER_CELERY_CONFIG_MODULE = ev(
    'WORKER_CELERY_CONFIG_MODULE',
    'analysis_engine.work_tasks.celery_config')
WORKER_TASKS = ev(
    'WORKER_TASKS',
    ('analysis_engine.work_tasks.get_new_pricing_data,'
     'analysis_engine.work_tasks.handle_pricing_update_task,'
     'analysis_engine.work_tasks.prepare_pricing_dataset,'
     'analysis_engine.work_tasks.publish_from_s3_to_redis,'
     'analysis_engine.work_tasks.publish_pricing_update,'
     'analysis_engine.work_tasks.task_screener_analysis,'
     'analysis_engine.work_tasks.run_distributed_algorithm,'
     'analysis_engine.work_tasks.publish_ticker_aggregate_from_s3'
     ''))
INCLUDE_TASKS = WORKER_TASKS.split(',')
CELERY_DISABLED = ev('CELERY_DISABLED', '0') == '1'

########################################
#
# Custom Variables
#
########################################
TICKER = ev(
    'TICKER',
    'SPY')
TICKER_ID = int(ev(
    'TICKER_ID',
    '1'))
DEFAULT_TICKERS = ev(
    'DEFAULT_TICKERS',
    'SPY,AMZN,TSLA,NFLX').split(',')
NEXT_EXP = analysis_engine.options_dates.option_expiration()
NEXT_EXP_STR = NEXT_EXP.strftime('%Y-%m-%d')
DAILY_S3_BUCKET_NAME = ev(
    'DAILY_S3_BUCKET_NAME',
    'daily')
MINUTE_S3_BUCKET_NAME = ev(
    'MINUTE_S3_BUCKET_NAME',
    'minute')
QUOTE_S3_BUCKET_NAME = ev(
    'QUOTE_S3_BUCKET_NAME',
    'quote')
STATS_S3_BUCKET_NAME = ev(
    'STATS_S3_BUCKET_NAME',
    'stats')
PEERS_S3_BUCKET_NAME = ev(
    'PEERS_S3_BUCKET_NAME',
    'peers')
NEWS_S3_BUCKET_NAME = ev(
    'NEWS_S3_BUCKET_NAME',
    'news')
FINANCIALS_S3_BUCKET_NAME = ev(
    'FINANCIALS_S3_BUCKET_NAME',
    'financials')
EARNINGS_S3_BUCKET_NAME = ev(
    'EARNINGS_S3_BUCKET_NAME',
    'earnings')
DIVIDENDS_S3_BUCKET_NAME = ev(
    'DIVIDENDS_S3_BUCKET_NAME',
    'dividends')
COMPANY_S3_BUCKET_NAME = ev(
    'COMPANY_S3_BUCKET_NAME',
    'company')
FETCH_MODE = ev(
    'FETCH_MODE',
    'full')
PREPARE_S3_BUCKET_NAME = ev(
    'PREPARE_S3_BUCKET_NAME',
    'prepared')
ANALYZE_S3_BUCKET_NAME = ev(
    'ANALYZE_S3_BUCKET_NAME',
    'analyzed')
SCREENER_S3_BUCKET_NAME = ev(
    'SCREENER_S3_BUCKET_NAME',
    'screener-data')
PRICING_S3_BUCKET_NAME = ev(
    'PRICING_S3_BUCKET_NAME',
    'pricing')
OPTIONS_S3_BUCKET_NAME = ev(
    'OPTIONS_S3_BUCKET_NAME',
    'options')
PREPARE_DATA_MIN_SIZE = 11
PLOT_COLORS = {
    'red': '#E74C3C',
    'feldspar': '#D19275',
    'copper': '#EDC393',
    'brown': '#6B4226',
    'orange': '#FF7D40',
    'maroon': '#800000',
    'gray': '#8B8989',
    'black': '#111111',
    'pink': '#FFCCCC',
    'green': '#2ECC71',
    'blue': '#3498db',
    'darkblue': '#000080',
    'lightgreen': '#C0FF3E',
    'darkgreen': '#385E0F',
    'gold': '#FFCC11',
    'yellow': '#FFE600',
    'volumetop': '#385E0F',
    'volume': '#ADFF2F',
    'high': '#CC1100',
    'low': '#164E71',
    'open': '#608DC0',
    'close': '#99CC32',
    'white': '#FFFFFF'
}

IEX_DAILY_DATE_FORMAT = '%Y-%b-%d'
IEX_MINUTE_DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'
IEX_TICK_DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'
IEX_QUOTE_DATE_FORMAT = '%B %d, %Y'
IEX_DATASETS_DEFAULT = [
    'daily',
    'minute',
    'quote',
    'stats',
    'peers',
    'news',
    'financials',
    'earnings',
    'dividends',
    'company'
]

COMMON_DATE_FORMAT = '%Y-%m-%d'
COMMON_TICK_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CACHE_DICT_VERSION = 1

SLACK_WEBHOOK = ev(
    'SLACK_WEBHOOK',
    None)
PROD_SLACK_ALERTS = ev(
    'PROD_SLACK_ALERTS',
    '0')
DATASET_COLLECTION_VERSION = 1
DATASET_COLLECTION_SLACK_ALERTS = ev(
    'DATASET_COLLECTION_SLACK_ALERTS',
    '0')
SLACK_FINVIZ_ALL_COLUMNS = [
    'ticker',
    'price',
    'volume',
    'change',
    'pe',
    'market_cap',
    'company',
    'industry',
    'sector',
    'country'
]
SLACK_FINVIZ_COLUMNS = [
    'ticker',
    'price',
    'volume',
    'change',
    'pe',
    'market_cap'
]
ALGO_INPUT_COMPRESS = (ev(
    'ALGO_INPUT_COMPRESS',
    '0') == '1')
ALGO_LOAD_COMPRESS = (ev(
    'ALGO_LOAD_COMPRESS',
    '0') == '1')
ALGO_HISTORY_COMPRESS = (ev(
    'ALGO_HISTORY_COMPRESS',
    '0') == '1')
ALGO_REPORT_COMPRESS = (ev(
    'ALGO_REPORT_COMPRESS',
    '0') == '1')
DEFAULT_SERIALIZED_DATASETS = [
    'daily',
    'minute',
    'quote',
    'stats',
    'peers',
    'news1',
    'financials',
    'earnings',
    'dividends',
    'company',
    'news',
    'calls',
    'puts',
    'pricing'
]
EMPTY_DF_STR = '[{}]'

########################################
#
# Algorithm Variables
#
########################################
ALGO_MODULE_PATH = ev(
    'ALGO_MODULE_PATH',
    '/opt/sa/analysis_engine/mocks/example_algo_minute.py')
ALGO_BASE_MODULE_PATH = ev(
    'ALGO_BASE_MODULE_PATH',
    '/opt/sa/analysis_engine/algo.py')
ALGO_MODULE_NAME = ev(
    'ALGO_MODULE_NAME',
    'example_algo_minute')
ALGO_VERSION = ev(
    'ALGO_VERSION',
    '1')
ALGO_BUYS_S3_BUCKET_NAME = ev(
    'ALGO_BUYS_S3_BUCKET_NAME',
    'algobuys')
ALGO_SELLS_S3_BUCKET_NAME = ev(
    'ALGO_SELLS_S3_BUCKET_NAME',
    'algosells')
ALGO_RESULT_S3_BUCKET_NAME = ev(
    'ALGO_RESULT_S3_BUCKET_NAME',
    'algoresult')
ALGO_EXTRACT_DATASET_S3_BUCKET_NAME = ev(
    'ALGO_EXTRACT_DATASET_S3_BUCKET_NAME',
    'algoready')
ALGO_READY_DATASET_S3_BUCKET_NAME = ev(
    'ALGO_READY_DATASET_S3_BUCKET_NAME',
    'algoready')
ALGO_HISTORY_DATASET_S3_BUCKET_NAME = ev(
    'ALGO_HISTORY_DATASET_S3_BUCKET_NAME',
    'algohistory')
ALGO_REPORT_DATASET_S3_BUCKET_NAME = ev(
    'ALGO_REPORT_DATASET_S3_BUCKET_NAME',
    'algoreport')
ALGO_BACKUP_DATASET_S3_BUCKET_NAME = ev(
    'ALGO_BACKUP_DATASET_S3_BUCKET_NAME',
    'algobackup')
ALGO_READY_DIR = ev(
    'ALGO_READY_DIR',
    '/tmp')
ALGO_EXTRACT_DIR = ev(
    'ALGO_EXTRACT_DIR',
    '/tmp')
ALGO_HISTORY_DIR = ev(
    'ALGO_HISTORY_HISTORY_DIR',
    '/tmp')
ALGO_REPORT_DIR = ev(
    'ALGO_REPORT_DIR',
    '/tmp')
ALGO_LOAD_DIR = ev(
    'ALGO_LOAD_DIR',
    '/tmp')
ALGO_BACKUP_DIR = ev(
    'ALGO_BACKUP_DIR',
    '/tmp')
ALGO_READY_REDIS_ADDRESS = ev(
    'ALGO_READY_REDIS_ADDRESS',
    'localhost:6379')
ALGO_EXTRACT_REDIS_ADDRESS = ev(
    'ALGO_EXTRACT_REDIS_ADDRESS',
    'localhost:6379')
ALGO_HISTORY_REDIS_ADDRESS = ev(
    'ALGO_HISTORY_REDIS_ADDRESS',
    'localhost:6379')
ALGO_REPORT_REDIS_ADDRESS = ev(
    'ALGO_REPORT_REDIS_ADDRESS',
    'localhost:6379')
ALGO_BACKUP_REDIS_ADDRESS = ev(
    'ALGO_BACKUP_REDIS_ADDRESS',
    'localhost:6379')

########################################
#
# S3 Variables
#
########################################
ENABLED_S3_UPLOAD = ev(
    'ENABLED_S3_UPLOAD',
    '0') == '1'
S3_ACCESS_KEY = ev(
    'AWS_ACCESS_KEY_ID',
    'trexaccesskey')
S3_SECRET_KEY = ev(
    'AWS_SECRET_ACCESS_KEY',
    'trex123321')
S3_REGION_NAME = ev(
    'AWS_DEFAULT_REGION',
    'us-east-1')
S3_ADDRESS = ev(
    'S3_ADDRESS',
    'localhost:9000')
S3_SECURE = ev(
    'S3_SECURE',
    '0') == '1'
S3_BUCKET = ev(
    'S3_BUCKET',
    'pricing')
S3_COMPILED_BUCKET = ev(
    'S3_COMPILED_BUCKET',
    'compileddatasets')
S3_KEY = ev(
    'S3_KEY',
    'test_key')

########################################
#
# Redis Variables
#
########################################
ENABLED_REDIS_PUBLISH = ev(
    'ENABLED_REDIS_PUBLISH',
    '0') == '1'
REDIS_ADDRESS = ev(
    'REDIS_ADDRESS',
    'localhost:6379')
REDIS_KEY = ev(
    'REDIS_KEY',
    'test_redis_key')
REDIS_PASSWORD = ev(
    'REDIS_PASSWORD',
    None)
REDIS_DB = int(ev(
    'REDIS_DB',
    '0'))
REDIS_EXPIRE = ev(
    'REDIS_EXPIRE',
    None)

# copy these values over
# when calling child tasks from a
# parent where the engine is
# running inside a fully-dockerized
# environment like kubernetes
# or docker-compose
SERVICE_VALS = [
    'ticker',
    's3_address',
    's3_access_key',
    's3_secret_key',
    's3_bucket',
    's3_secure',
    's3_region_name',
    'redis_address',
    'redis_db',
    'redis_password',
    'redis_expire'
]


def get_status(
        status):
    """get_status

    Return the string label for an integer status code
    which should be one of the ones above.

    :param status: integer status code
    """
    if status == SUCCESS:
        return 'SUCCESS'
    elif status == FAILED:
        return 'FAILED'
    elif status == ERR:
        return 'ERR'
    elif status == EX:
        return 'EX'
    elif status == NOT_RUN:
        return 'NOT_RUN'
    elif status == INVALID:
        return 'INVALID'
    elif status == NOT_DONE:
        return 'NOT_DONE'
    elif status == NOT_SET:
        return 'NOT_SET'
    elif status == EMPTY:
        return 'EMPTY'
    elif status == SA_MODE_PREPARE:
        return 'SA_MODE_PREPARE'
    elif status == SA_MODE_ANALYZE:
        return 'SA_MODE_ANALYZE'
    elif status == SA_MODE_PREDICT:
        return 'SA_MODE_PREDICT'
    elif status == SA_MODE_EXTRACT:
        return 'SA_MODE_EXTRACT'
    elif status == SA_MODE_SHOW_DATASET:
        return 'SA_MODE_SHOW_DATASET'
    elif status == SA_MODE_RESTORE_REDIS_DATASET:
        return 'SA_MODE_RESTORE_REDIS_DATASET'
    elif status == SA_MODE_RUN_ALGO:
        return 'SA_MODE_RUN_ALGO'
    elif status == PLOT_ACTION_SHOW:
        return 'PLOT_ACTION_SHOW'
    elif status == PLOT_ACTION_SAVE_TO_S3:
        return 'PLOT_ACTION_SAVE_TO_S3'
    elif status == PLOT_ACTION_SAVE_AS_FILE:
        return 'PLOT_ACTION_SAVE_AS_FILE'
    elif status == TRADE_OPEN:
        return 'TRADE_OPEN'
    elif status == TRADE_NOT_ENOUGH_FUNDS:
        return 'TRADE_NOT_ENOUGH_FUNDS'
    elif status == TRADE_FILLED:
        return 'TRADE_FILLED'
    elif status == TRADE_NO_SHARES_TO_SELL:
        return 'TRADE_NO_SHARES_TO_SELL'
    elif status == TRADE_EXPIRED:
        return 'TRADE_EXPIRED'
    elif status == TRADE_SHARES:
        return 'TRADE_SHARES'
    elif status == TRADE_VERTICAL_BULL_SPREAD:
        return 'TRADE_VERTICAL_BULL_SPREAD'
    elif status == TRADE_VERTICAL_BEAR_SPREAD:
        return 'TRADE_VERTICAL_BEAR_SPREAD'
    elif status == TRADE_PROFITABLE:
        return 'TRADE_PROFITABLE'
    elif status == TRADE_NOT_PROFITABLE:
        return 'TRADE_NOT_PROFITABLE'
    elif status == TRADE_HIT_STOP_LOSS:
        return 'TRADE_HIT_STOP_LOSS'
    elif status == TRADE_HIT_STOP_LOSS_PERCENT:
        return 'TRADE_HIT_STOP_LOSS_PERCENT'
    elif status == TRADE_HIT_TAILING_STOP_LOSS:
        return 'TRADE_HIT_TAILING_STOP_LOSS'
    elif status == TRADE_HIT_TAILING_STOP_LOSS_PERCENT:
        return 'TRADE_HIT_TAILING_STOP_LOSS_PERCENT'
    elif status == TRADE_INVALID:
        return 'TRADE_INVALID'
    elif status == TRADE_ERROR:
        return 'TRADE_ERROR'
    elif status == TRADE_ENTRY:
        return 'TRADE_ENTRY'
    elif status == TRADE_EXIT:
        return 'TRADE_EXIT'
    elif status == BACKTEST_FOUND_TRADE_PROFITABLE:
        return 'BACKTEST_FOUND_TRADE_PROFITABLE'
    elif status == BACKTEST_FOUND_TRADE_NOT_PROFITABLE:
        return 'BACKTEST_FOUND_TRADE_NOT_PROFITABLE'
    elif status == BACKTEST_FOUND_TRADE_NEVER_FILLED:
        return 'BACKTEST_FOUND_TRADE_NEVER_FILLED'
    elif status == BACKTEST_FOUND_TRADE_EXPIRED:
        return 'BACKTEST_FOUND_TRADE_EXPIRED'
    elif status == SPREAD_VERTICAL_BULL:
        return 'SPREAD_VERTICAL_BULL'
    elif status == SPREAD_VERTICAL_BEAR:
        return 'SPREAD_VERTICAL_BEAR'
    elif status == OPTION_CALL:
        return 'OPTION_CALL'
    elif status == OPTION_PUT:
        return 'OPTION_PUT'
    elif status == ALGO_PROFITABLE:
        return 'ALGO_PROFITABLE'
    elif status == ALGO_NOT_PROFITABLE:
        return 'ALGO_NOT_PROFITABLE'
    elif status == ALGO_ERROR:
        return 'ALGO_ERROR'
    elif status == ALGO_NOT_ACTIVE:
        return 'ALGO_NOT_ACTIVE'
    elif status == S3_FAILED:
        return 'S3_FAILED'
    elif status == REDIS_FAILED:
        return 'REDIS_FAILED'
    elif status == FILE_FAILED:
        return 'FILE_FAILED'
    elif status == SLACK_FAILED:
        return 'SLACK_FAILED'
    elif status == ALGO_HORIZON_UNITS_DAY:
        return 'ALGO_HORIZON_UNITS_DAY'
    elif status == ALGO_HORIZON_UNITS_MINUTE:
        return 'ALGO_HORIZON_UNITS_MINUTE'
    elif SA_DATASET_TYPE_ALGO_READY == SA_DATASET_TYPE_ALGO_READY:
        return 'SA_DATASET_TYPE_ALGO_READY'
    else:
        return 'unsupported status={}'.format(
            status)
# end of get_status


def ppj(
        json_data):
    """ppj

    :param json_data: dictionary to convert to
                      a pretty-printed, multi-line string
    """
    return str(
        json.dumps(
            json_data,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')))
# end of ppj


def to_float_str(
        val):
    """to_float_str

    convert the float to a string with 2 decimal points of
    precision

    :param val: float to change to a 2-decimal string
    """
    return str("%0.2f" % float(val))
# end of to_float_str


def to_f(
        val):
    """to_f

    truncate the float to 2 decimal points of
    precision

    :param val: float to change
    """
    return float(to_float_str(val))
# end of to_f


def get_mb(
        num):
    """get_mb

    convert a the number of bytes (as an ``integer``)
    to megabytes with 2 decimal points of precision

    :param num: integer - number of bytes
    """
    return to_f(num / NUM_BYTES_IN_AN_MB)
# end get_mb


def get_percent_done(
        progress,
        total):
    """get_percent_done

    calculate percentage done to 2 decimal points of
    precision

    :param progress: progress counter
    :param total: total number of counts
    """
    return to_f(float(float(progress)/float(total)*100.00))
# end of get_percent_done


def is_celery_disabled(
        work_dict=None):
    """is_celery_disabled

    :param work_dict: request to check
    """
    env_disabled = ev('CELERY_DISABLED', '0') == '1'
    request_disabled = False
    if work_dict:
        request_disabled = work_dict.get('celery_disabled', False)
    return (env_disabled or request_disabled)
# end of is_celery_disabled
