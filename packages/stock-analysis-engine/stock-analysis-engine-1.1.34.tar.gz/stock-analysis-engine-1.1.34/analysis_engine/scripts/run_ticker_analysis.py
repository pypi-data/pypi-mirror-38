#!/usr/bin/env python

"""

Run buy and sell analysis on a stock to send alerts to subscribed
users

Steps:

1) Parse arguments
2) Get pricing data as a Celery task
3) Publish pricing data as a Celery tasks
4) Coming Soon - Start buy/sell analysis as Celery task(s)

"""

import os
import argparse
import analysis_engine.api_requests as api_requests
import analysis_engine.work_tasks.get_new_pricing_data as task_pricing
import analysis_engine.work_tasks.task_screener_analysis as screener_utils
from celery import signals
from spylunking.log.setup_logging import build_colorized_logger
from analysis_engine.work_tasks.get_celery_app import get_celery_app
from analysis_engine.consts import LOG_CONFIG_PATH
from analysis_engine.consts import TICKER
from analysis_engine.consts import TICKER_ID
from analysis_engine.consts import COMMON_DATE_FORMAT
from analysis_engine.consts import NEXT_EXP_STR
from analysis_engine.consts import WORKER_BROKER_URL
from analysis_engine.consts import WORKER_BACKEND_URL
from analysis_engine.consts import WORKER_CELERY_CONFIG_MODULE
from analysis_engine.consts import INCLUDE_TASKS
from analysis_engine.consts import SSL_OPTIONS
from analysis_engine.consts import TRANSPORT_OPTIONS
from analysis_engine.consts import S3_ACCESS_KEY
from analysis_engine.consts import S3_SECRET_KEY
from analysis_engine.consts import S3_REGION_NAME
from analysis_engine.consts import S3_ADDRESS
from analysis_engine.consts import S3_SECURE
from analysis_engine.consts import S3_BUCKET
from analysis_engine.consts import S3_KEY
from analysis_engine.consts import REDIS_ADDRESS
from analysis_engine.consts import REDIS_KEY
from analysis_engine.consts import REDIS_PASSWORD
from analysis_engine.consts import REDIS_DB
from analysis_engine.consts import REDIS_EXPIRE
from analysis_engine.consts import ppj
from analysis_engine.consts import is_celery_disabled
from analysis_engine.consts import get_status
from analysis_engine.utils import last_close


# Disable celery log hijacking
# https://github.com/celery/celery/issues/2509
@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


log = build_colorized_logger(
    name='run-analysis',
    log_config_path=LOG_CONFIG_PATH)


def start_screener_analysis(
        req):
    """start_screener_analysis

    Start screener-driven analysis with a simple workflow:

    1) Convert FinViz screeners into a list of tickers
       and a ``pandas.DataFrames`` from each ticker's html row
    2) Build unique list of tickers
    3) Pull datasets for each ticker
    4) Run sale-side processing - coming soon
    5) Run buy-side processing - coming soon
    6) Issue alerts to slack - coming soon

    :param req: dictionary to start the screener analysis
    """
    label = req.get(
        'label',
        'screener')
    log.info(
        '{} - start screener analysis'.format(
            label))
    req['celery_disabled'] = True
    analysis_res = screener_utils.run_screener_analysis(
        work_dict=req)
    log.info(
        '{} - done screener analysis result={}'.format(
            label,
            analysis_res))
# end of start_screener_analysis


def run_ticker_analysis():
    """run_ticker_analysis

    Collect all datasets for the ticker **SPY**:

    ::

        run_ticker_analysis.py -t SPY

    .. note:: This requires the following services are listening on:

        - redis ``localhost:6379``
        - minio ``localhost:9000``

    **Coming Soon**

    Run buy and sell analysis on a stock to send alerts to subscribed
    users

    """

    log.info(
        'start - run_ticker_analysis')

    parser = argparse.ArgumentParser(
        description=(
            'Download and store the latest stock pricing, '
            'news, and options chain data '
            'and store it in S3 and Redis. '
            'Once stored, this will also '
            'start the buy and sell trading analysis.'))
    parser.add_argument(
        '-t',
        help=(
            'ticker'),
        required=False,
        dest='ticker')
    parser.add_argument(
        '-g',
        help=(
            'optional - fetch mode: '
            'all = fetch from all data sources (default), '
            'yahoo = fetch from just Yahoo sources, '
            'iex = fetch from just IEX sources'),
        required=False,
        dest='fetch_mode')
    parser.add_argument(
        '-i',
        help=(
            'optional - ticker id '
            'not used without a database'),
        required=False,
        dest='ticker_id')
    parser.add_argument(
        '-e',
        help=(
            'optional - options expiration date'),
        required=False,
        dest='exp_date_str')
    parser.add_argument(
        '-l',
        help=(
            'optional - path to the log config file'),
        required=False,
        dest='log_config_path')
    parser.add_argument(
        '-b',
        help=(
            'optional - broker url for Celery'),
        required=False,
        dest='broker_url')
    parser.add_argument(
        '-B',
        help=(
            'optional - backend url for Celery'),
        required=False,
        dest='backend_url')
    parser.add_argument(
        '-k',
        help=(
            'optional - s3 access key'),
        required=False,
        dest='s3_access_key')
    parser.add_argument(
        '-s',
        help=(
            'optional - s3 secret key'),
        required=False,
        dest='s3_secret_key')
    parser.add_argument(
        '-a',
        help=(
            'optional - s3 address format: <host:port>'),
        required=False,
        dest='s3_address')
    parser.add_argument(
        '-S',
        help=(
            'optional - s3 ssl or not'),
        required=False,
        dest='s3_secure')
    parser.add_argument(
        '-u',
        help=(
            'optional - s3 bucket name'),
        required=False,
        dest='s3_bucket_name')
    parser.add_argument(
        '-G',
        help=(
            'optional - s3 region name'),
        required=False,
        dest='s3_region_name')
    parser.add_argument(
        '-p',
        help=(
            'optional - redis_password'),
        required=False,
        dest='redis_password')
    parser.add_argument(
        '-r',
        help=(
            'optional - redis_address format: <host:port>'),
        required=False,
        dest='redis_address')
    parser.add_argument(
        '-n',
        help=(
            'optional - redis and s3 key name'),
        required=False,
        dest='keyname')
    parser.add_argument(
        '-m',
        help=(
            'optional - redis database number (0 by default)'),
        required=False,
        dest='redis_db')
    parser.add_argument(
        '-x',
        help=(
            'optional - redis expiration in seconds'),
        required=False,
        dest='redis_expire')
    parser.add_argument(
        '-z',
        help=(
            'optional - strike price'),
        required=False,
        dest='strike')
    parser.add_argument(
        '-c',
        help=(
            'optional - contract type "C" for calls "P" for puts'),
        required=False,
        dest='contract_type')
    parser.add_argument(
        '-P',
        help=(
            'optional - get pricing data if "1" or "0" disabled'),
        required=False,
        dest='get_pricing')
    parser.add_argument(
        '-N',
        help=(
            'optional - get news data if "1" or "0" disabled'),
        required=False,
        dest='get_news')
    parser.add_argument(
        '-O',
        help=(
            'optional - get options data if "1" or "0" disabled'),
        required=False,
        dest='get_options')
    parser.add_argument(
        '-U',
        help=(
            'optional - s3 enabled for publishing if "1" or '
            '"0" is disabled'),
        required=False,
        dest='s3_enabled')
    parser.add_argument(
        '-R',
        help=(
            'optional - redis enabled for publishing if "1" or '
            '"0" is disabled'),
        required=False,
        dest='redis_enabled')
    parser.add_argument(
        '-A',
        help=(
            'optional - run an analysis '
            'supported modes: scn'),
        required=False,
        dest='analysis_type')
    parser.add_argument(
        '-L',
        help=(
            'optional - screener urls to pull '
            'tickers for analysis'),
        required=False,
        dest='urls')
    parser.add_argument(
        '-d',
        help=(
            'debug'),
        required=False,
        dest='debug',
        action='store_true')
    args = parser.parse_args()

    ticker = TICKER
    ticker_id = TICKER_ID
    fetch_mode = 'all'
    exp_date_str = NEXT_EXP_STR
    ssl_options = SSL_OPTIONS
    transport_options = TRANSPORT_OPTIONS
    broker_url = WORKER_BROKER_URL
    backend_url = WORKER_BACKEND_URL
    celery_config_module = WORKER_CELERY_CONFIG_MODULE
    include_tasks = INCLUDE_TASKS
    s3_access_key = S3_ACCESS_KEY
    s3_secret_key = S3_SECRET_KEY
    s3_region_name = S3_REGION_NAME
    s3_address = S3_ADDRESS
    s3_secure = S3_SECURE
    s3_bucket_name = S3_BUCKET
    s3_key = S3_KEY
    redis_address = REDIS_ADDRESS
    redis_key = REDIS_KEY
    redis_password = REDIS_PASSWORD
    redis_db = REDIS_DB
    redis_expire = REDIS_EXPIRE
    strike = None
    contract_type = None
    get_pricing = True
    get_news = True
    get_options = True
    s3_enabled = True
    redis_enabled = True
    analysis_type = None
    debug = False

    if args.ticker:
        ticker = args.ticker.upper()
    if args.ticker_id:
        ticker_id = args.ticker_id
    if args.exp_date_str:
        exp_date_str = NEXT_EXP_STR
    if args.broker_url:
        broker_url = args.broker_url
    if args.backend_url:
        backend_url = args.backend_url
    if args.s3_access_key:
        s3_access_key = args.s3_access_key
    if args.s3_secret_key:
        s3_secret_key = args.s3_secret_key
    if args.s3_region_name:
        s3_region_name = args.s3_region_name
    if args.s3_address:
        s3_address = args.s3_address
    if args.s3_secure:
        s3_secure = args.s3_secure
    if args.s3_bucket_name:
        s3_bucket_name = args.s3_bucket_name
    if args.keyname:
        s3_key = args.keyname
        redis_key = args.keyname
    if args.redis_address:
        redis_address = args.redis_address
    if args.redis_password:
        redis_password = args.redis_password
    if args.redis_db:
        redis_db = args.redis_db
    if args.redis_expire:
        redis_expire = args.redis_expire
    if args.strike:
        strike = args.strike
    if args.contract_type:
        contract_type = args.contract_type
    if args.get_pricing:
        get_pricing = args.get_pricing == '1'
    if args.get_news:
        get_news = args.get_news == '1'
    if args.get_options:
        get_options = args.get_options == '1'
    if args.s3_enabled:
        s3_enabled = args.s3_enabled == '1'
    if args.redis_enabled:
        redis_enabled = args.redis_enabled == '1'
    if args.fetch_mode:
        fetch_mode = str(args.fetch_mode).lower()
    if args.analysis_type:
        analysis_type = str(args.analysis_type).lower()
    if args.debug:
        debug = True

    work = api_requests.build_get_new_pricing_request()

    work['ticker'] = ticker
    work['ticker_id'] = ticker_id
    work['s3_bucket'] = s3_bucket_name
    work['s3_key'] = s3_key
    work['redis_key'] = redis_key
    work['strike'] = strike
    work['contract'] = contract_type
    work['exp_date'] = exp_date_str
    work['s3_access_key'] = s3_access_key
    work['s3_secret_key'] = s3_secret_key
    work['s3_region_name'] = s3_region_name
    work['s3_address'] = s3_address
    work['s3_secure'] = s3_secure
    work['redis_address'] = redis_address
    work['redis_password'] = redis_password
    work['redis_db'] = redis_db
    work['redis_expire'] = redis_expire
    work['get_pricing'] = get_pricing
    work['get_news'] = get_news
    work['get_options'] = get_options
    work['s3_enabled'] = s3_enabled
    work['redis_enabled'] = redis_enabled
    work['fetch_mode'] = fetch_mode
    work['analysis_type'] = analysis_type
    work['debug'] = debug
    work['label'] = 'ticker={}'.format(
        ticker)

    if analysis_type == 'scn':
        label = 'screener={}'.format(
            work['ticker'])
        fv_urls = []
        if args.urls:
            fv_urls = str(args.urls).split('|')
        if len(fv_urls) == 0:
            fv_urls = os.getenv('SCREENER_URLS', []).split('|')
        screener_req = api_requests.build_screener_analysis_request(
            ticker=ticker,
            fv_urls=fv_urls,
            label=label)
        work.update(screener_req)
        start_screener_analysis(
            req=work)
    # end of analysis_type
    else:
        if not args.keyname:
            last_close_date = last_close()
            work['s3_key'] = '{}_{}'.format(
                work['ticker'],
                last_close_date.strftime(COMMON_DATE_FORMAT))
            work['redis_key'] = '{}_{}'.format(
                work['ticker'],
                last_close_date.strftime(COMMON_DATE_FORMAT))

        path_to_tasks = 'analysis_engine.work_tasks'
        task_name = (
            '{}.get_new_pricing_data.get_new_pricing_data'.format(
                path_to_tasks))
        task_res = None
        if is_celery_disabled():
            work['celery_disabled'] = True
            log.debug(
                'starting without celery work={}'.format(
                    ppj(work)))
            task_res = task_pricing.get_new_pricing_data(
                work)

            if debug:
                log.info(
                    'done - result={} '
                    'task={} status={} '
                    'err={} label={}'.format(
                        ppj(task_res),
                        task_name,
                        get_status(status=task_res['status']),
                        task_res['err'],
                        work['label']))
            else:
                log.info(
                    'done - result '
                    'task={} status={} '
                    'err={} label={}'.format(
                        task_name,
                        get_status(status=task_res['status']),
                        task_res['err'],
                        work['label']))
            # if/else debug
        else:
            log.info(
                'connecting to broker={} backend={}'.format(
                    broker_url,
                    backend_url))

            # Get the Celery app
            app = get_celery_app(
                name=__name__,
                auth_url=broker_url,
                backend_url=backend_url,
                path_to_config_module=celery_config_module,
                ssl_options=ssl_options,
                transport_options=transport_options,
                include_tasks=include_tasks)

            log.info(
                'calling task={} - work={}'.format(
                    task_name,
                    ppj(work)))
            job_id = app.send_task(
                task_name,
                (work,))
            log.info(
                'calling task={} - success job_id={}'.format(
                    task_name,
                    job_id))
        # end of if/else
    # end of supported modes
# end of run_ticker_analysis


if __name__ == '__main__':
    run_ticker_analysis()
