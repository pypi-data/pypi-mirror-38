"""
Run an Algo
"""

import os
import datetime
import json
import analysis_engine.build_algo_request as algo_utils
import analysis_engine.iex.extract_df_from_redis as iex_extract_utils
import analysis_engine.yahoo.extract_df_from_redis as yahoo_extract_utils
import analysis_engine.algo as default_algo
import analysis_engine.build_result as build_result
from analysis_engine.consts import SUCCESS
from analysis_engine.consts import ERR
from analysis_engine.consts import NOT_RUN
from analysis_engine.consts import FAILED
from analysis_engine.consts import EMPTY
from analysis_engine.consts import COMMON_TICK_DATE_FORMAT
from analysis_engine.consts import get_percent_done
from analysis_engine.utils import last_close
from analysis_engine.utils import get_last_close_str
from analysis_engine.utils import get_date_from_str
from analysis_engine.api_requests import get_ds_dict
from spylunking.log.setup_logging import build_colorized_logger


log = build_colorized_logger(
    name=__name__)


def run_algo(
        ticker=None,
        tickers=None,
        balance=None,     # float starting base capital
        commission=None,  # float for single trade commission for buy or sell
        start_date=None,  # string YYYY-MM-DD HH:MM:SS
        end_date=None,    # string YYYY-MM-DD HH:MM:SS
        datasets=None,    # string list of identifiers
        algo=None,  # derived ``analysis_engine.algo.Algo`` instance
        num_owned_dict=None,  # not supported
        cache_freq='daily',   # 'minute' not supported
        auto_fill=True,
        use_key=None,
        extract_mode='all',
        iex_datasets=None,
        redis_enabled=True,
        redis_address=None,
        redis_db=None,
        redis_password=None,
        redis_expire=None,
        s3_enabled=True,
        s3_address=None,
        s3_bucket=None,
        s3_access_key=None,
        s3_secret_key=None,
        s3_region_name=None,
        s3_secure=False,
        celery_disabled=True,
        broker_url=None,
        result_backend=None,
        label=None,
        verbose=False,
        publish_to_slack=True,
        publish_to_s3=True,
        publish_to_redis=True,
        raise_on_err=False):
    """run_algo

    Run an algorithm with steps:

        1) Extract redis keys between dates
        2) Compile a data pipeline dictionary (call it ``data``)
        3) Call algorithm's ``myalgo.handle_data(data=data)``
            a) If no ``algo`` is set, the
               ``analysis_engine.algo.BaseAlgo`` algorithm
               is used.

    .. note:: Please ensure Redis and Minio are running
              before trying to extract tickers

    **Stock tickers to extract**

    :param ticker: single stock ticker/symbol/ETF to extract
    :param tickers: optional - list of tickers to extract
    :param use_key: optional - extract historical key from Redis

    **Algo Configuration**

    :param balance: float balance
    :param commission: float for single trade commission for
        buy or sell
    :param start_date: string ``YYYY-MM-DD_HH:MM:SS`` cache value
    :param end_date: string ``YYYY-MM-DD_HH:MM:SS`` cache value
    :param dataset_types: list of strings that are ``iex`` or ``yahoo``
        datasets that are cached.
    :param cache_freq: optional - depending on if you are running data feeds
        on a ``daily`` cron (default) vs every ``minute`` (or faster)
    :param algo: derived instance of ``analysis_engine.algo.Algo`` object
    :param num_owned_dict: not supported yet
    :param auto_fill: optional - boolean for auto filling
        buy/sell orders for backtesting (default is
        ``True``)
    :param trading_calendar: ``trading_calendar.TradingCalendar``
        object, by default ``analysis_engine.calendars.
        always_open.AlwaysOpen`` trading calendar
        # TradingCalendar by ``TFSExchangeCalendar``

    **(Optional) Data sources, datafeeds and datasets to gather**

    :param iex_datasets: list of strings for gathering specific `IEX
        datasets <https://iextrading.com/developer/docs/#stocks>`__
        which are set as consts: ``analysis_engine.iex.consts.FETCH_*``.

    **(Optional) Redis connectivity arguments**

    :param redis_enabled: bool - toggle for auto-caching all
        datasets in Redis
        (default is ``True``)
    :param redis_address: Redis connection string format: ``host:port``
        (default is ``localhost:6379``)
    :param redis_db: Redis db to use
        (default is ``0``)
    :param redis_password: optional - Redis password
        (default is ``None``)
    :param redis_expire: optional - Redis expire value
        (default is ``None``)

    **(Optional) Minio (S3) connectivity arguments**

    :param s3_enabled: bool - toggle for auto-archiving on Minio (S3)
        (default is ``True``)
    :param s3_address: Minio S3 connection string format: ``host:port``
        (default is ``localhost:9000``)
    :param s3_bucket: S3 Bucket for storing the artifacts
        (default is ``dev``) which should be viewable on a browser:
        http://localhost:9000/minio/dev/
    :param s3_access_key: S3 Access key
        (default is ``trexaccesskey``)
    :param s3_secret_key: S3 Secret key
        (default is ``trex123321``)
    :param s3_region_name: S3 region name
        (default is ``us-east-1``)
    :param s3_secure: Transmit using tls encryption
        (default is ``False``)

    **(Optional) Celery worker broker connectivity arguments**

    :param celery_disabled: bool - toggle synchronous mode or publish
        to an engine connected to the `Celery broker and backend
        <https://github.com/celery/celery#transports-and-backends>`__
        (default is ``True`` - synchronous mode without an engine
        or need for a broker or backend for Celery)
    :param broker_url: Celery broker url
        (default is ``redis://0.0.0.0:6379/13``)
    :param result_backend: Celery backend url
        (default is ``redis://0.0.0.0:6379/14``)
    :param label: tracking log label
    :param publish_to_slack: optional - boolean for
        publishing to slack (coming soon)
    :param publish_to_s3: optional - boolean for
        publishing to s3 (coming soon)
    :param publish_to_redis: optional - boolean for
        publishing to redis (coming soon)

    **(Optional) Debugging**

    :param verbose: bool - show extract warnings
        and other debug logging (default is False)
    :param raise_on_err: optional - boolean for
        unittests and developing algorithms with the
        ``analysis_engine.run_algo.run_algo`` helper.
        When set to ``True`` exceptions will
        are raised to the calling functions

    **Supported environment variables**

    ::

        export REDIS_ADDRESS="localhost:6379"
        export REDIS_DB="0"
        export S3_ADDRESS="localhost:9000"
        export S3_BUCKET="dev"
        export AWS_ACCESS_KEY_ID="trexaccesskey"
        export AWS_SECRET_ACCESS_KEY="trex123321"
        export AWS_DEFAULT_REGION="us-east-1"
        export S3_SECURE="0"
        export WORKER_BROKER_URL="redis://0.0.0.0:6379/13"
        export WORKER_BACKEND_URL="redis://0.0.0.0:6379/14"
    """

    # dictionary structure with a list sorted on: ascending dates
    # algo_data_req[ticker][list][dataset] = pd.DataFrame
    algo_data_req = {}
    extract_requests = []
    rec = {}
    msg = None

    use_tickers = tickers
    if ticker:
        use_tickers = [ticker]
    else:
        if not use_tickers:
            use_tickers = []

    default_iex_datasets = [
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

    if not iex_datasets:
        iex_datasets = default_iex_datasets

    if redis_enabled:
        if not redis_address:
            redis_address = os.getenv(
                'REDIS_ADDRESS',
                'localhost:6379')
        if not redis_password:
            redis_password = os.getenv(
                'REDIS_PASSWORD',
                None)
        if not redis_db:
            redis_db = int(os.getenv(
                'REDIS_DB',
                '0'))
        if not redis_expire:
            redis_expire = os.getenv(
                'REDIS_EXPIRE',
                None)
    if s3_enabled:
        if not s3_address:
            s3_address = os.getenv(
                'S3_ADDRESS',
                'localhost:9000')
        if not s3_access_key:
            s3_access_key = os.getenv(
                'AWS_ACCESS_KEY_ID',
                'trexaccesskey')
        if not s3_secret_key:
            s3_secret_key = os.getenv(
                'AWS_SECRET_ACCESS_KEY',
                'trex123321')
        if not s3_region_name:
            s3_region_name = os.getenv(
                'AWS_DEFAULT_REGION',
                'us-east-1')
        if not s3_secure:
            s3_secure = os.getenv(
                'S3_SECURE',
                '0') == '1'
        if not s3_bucket:
            s3_bucket = os.getenv(
                'S3_BUCKET',
                'dev')
    if not broker_url:
        broker_url = os.getenv(
            'WORKER_BROKER_URL',
            'redis://0.0.0.0:6379/13')
    if not result_backend:
        result_backend = os.getenv(
            'WORKER_BACKEND_URL',
            'redis://0.0.0.0:6379/14')

    if not label:
        label = 'run-algo'

    num_tickers = len(use_tickers)
    last_close_str = get_last_close_str()

    if iex_datasets:
        log.info(
            '{} - tickers={} '
            'iex={}'.format(
                label,
                num_tickers,
                json.dumps(iex_datasets)))
    else:
        log.info(
            '{} - tickers={}'.format(
                label,
                num_tickers))

    ticker_key = use_key
    if not ticker_key:
        ticker_key = '{}_{}'.format(
            ticker,
            last_close_str)

    if not algo:
        algo = default_algo.BaseAlgo(
            tickers=use_tickers,
            balance=balance,
            commission=commission,
            name=label,
            auto_fill=auto_fill,
            publish_to_slack=publish_to_slack,
            publish_to_s3=publish_to_s3,
            publish_to_redis=publish_to_redis,
            raise_on_err=raise_on_err)

    if not algo:
        msg = (
            '{} - missing algo object'.format(
                label))
        log.error(msg)
        return build_result.build_result(
                status=EMPTY,
                err=msg,
                rec=rec)

    if raise_on_err:
        log.debug(
            '{} - enabling algo exception raises'.format(
                label))
        algo.raise_on_err = True

    common_vals = {}
    common_vals['base_key'] = ticker_key
    common_vals['celery_disabled'] = celery_disabled
    common_vals['ticker'] = ticker
    common_vals['label'] = label
    common_vals['iex_datasets'] = iex_datasets
    common_vals['s3_enabled'] = s3_enabled
    common_vals['s3_bucket'] = s3_bucket
    common_vals['s3_address'] = s3_address
    common_vals['s3_secure'] = s3_secure
    common_vals['s3_region_name'] = s3_region_name
    common_vals['s3_access_key'] = s3_access_key
    common_vals['s3_secret_key'] = s3_secret_key
    common_vals['s3_key'] = ticker_key
    common_vals['redis_enabled'] = redis_enabled
    common_vals['redis_address'] = redis_address
    common_vals['redis_password'] = redis_password
    common_vals['redis_db'] = redis_db
    common_vals['redis_key'] = ticker_key
    common_vals['redis_expire'] = redis_expire

    """
    Extract Datasets
    """

    iex_daily_status = FAILED
    iex_minute_status = FAILED
    iex_quote_status = FAILED
    iex_stats_status = FAILED
    iex_peers_status = FAILED
    iex_news_status = FAILED
    iex_financials_status = FAILED
    iex_earnings_status = FAILED
    iex_dividends_status = FAILED
    iex_company_status = FAILED
    yahoo_news_status = FAILED
    yahoo_options_status = FAILED
    yahoo_pricing_status = FAILED

    iex_daily_df = None
    iex_minute_df = None
    iex_quote_df = None
    iex_stats_df = None
    iex_peers_df = None
    iex_news_df = None
    iex_financials_df = None
    iex_earnings_df = None
    iex_dividends_df = None
    iex_company_df = None
    yahoo_option_calls_df = None
    yahoo_option_puts_df = None
    yahoo_pricing_df = None
    yahoo_news_df = None

    use_start_date_str = start_date
    use_end_date_str = end_date
    last_close_date = last_close()
    end_date_val = None

    cache_freq_fmt = COMMON_TICK_DATE_FORMAT

    if not use_end_date_str:
        use_end_date_str = last_close_date.strftime(
            cache_freq_fmt)

    end_date_val = get_date_from_str(
        date_str=use_end_date_str,
        fmt=cache_freq_fmt)

    if not use_start_date_str:
        start_date_val = end_date_val - datetime.timedelta(
            days=60)
        use_start_date_str = start_date_val.strftime(
            cache_freq_fmt)

    total_dates = (end_date_val - start_date_val).days

    if end_date_val < start_date_val:
        msg = (
            '{} - invalid dates - start_date={} is after '
            'end_date={}'.format(
                label,
                start_date_val,
                end_date_val))
        raise Exception(msg)

    log.debug(
        '{} - days={} start={} end={} datatset={}'.format(
            label,
            total_dates,
            use_start_date_str,
            use_end_date_str,
            datasets))

    for ticker in use_tickers:
        req = algo_utils.build_algo_request(
            ticker=ticker,
            use_key=use_key,
            start_date=use_start_date_str,
            end_date=use_end_date_str,
            datasets=datasets,
            balance=balance,
            cache_freq=cache_freq,
            label=label)
        ticker_key = '{}_{}'.format(
            ticker,
            last_close_str)
        common_vals['ticker'] = ticker
        common_vals['base_key'] = ticker_key
        common_vals['redis_key'] = ticker_key
        common_vals['s3_key'] = ticker_key

        for date_key in req['extract_datasets']:
            date_req = get_ds_dict(
                ticker=ticker,
                base_key=date_key,
                ds_id=label,
                service_dict=common_vals)
            extract_requests.append({
                'ticker': ticker,
                'date_key': date_key,
                'req': date_req})
    # end of for all ticker in use_tickers

    extract_iex = True
    if extract_mode not in ['all', 'iex']:
        extract_iex = False

    extract_yahoo = True
    if extract_mode not in ['all', 'yahoo']:
        extract_yahoo = False

    first_extract_date = None
    last_extract_date = None
    total_extract_requests = len(extract_requests)
    cur_idx = 1
    for idx, extract_node in enumerate(extract_requests):
        extract_ticker = extract_node['ticker']
        extract_date = extract_node['date_key']
        extract_req = extract_node['req']
        if not first_extract_date:
            first_extract_date = extract_date
        last_extract_date = extract_date
        dataset_id = '{}_{}'.format(
            ticker,
            extract_date)
        percent_label = (
            '{} ticker={} date={} {} {}/{}'.format(
                label,
                extract_ticker,
                extract_date,
                get_percent_done(
                    progress=cur_idx,
                    total=total_extract_requests),
                idx,
                total_extract_requests))
        log.debug(
            '{} - extract - start'.format(
                percent_label))
        if 'daily' in iex_datasets or extract_iex:
            iex_daily_status, iex_daily_df = \
                iex_extract_utils.extract_daily_dataset(
                    extract_req)
            if iex_daily_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_daily={}'.format(ticker))
        if 'minute' in iex_datasets or extract_iex:
            iex_minute_status, iex_minute_df = \
                iex_extract_utils.extract_minute_dataset(
                    extract_req)
            if iex_minute_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_minute={}'.format(ticker))
        if 'quote' in iex_datasets or extract_iex:
            iex_quote_status, iex_quote_df = \
                iex_extract_utils.extract_quote_dataset(
                    extract_req)
            if iex_quote_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_quote={}'.format(ticker))
        if 'stats' in iex_datasets or extract_iex:
            iex_stats_df, iex_stats_df = \
                iex_extract_utils.extract_stats_dataset(
                    extract_req)
            if iex_stats_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_stats={}'.format(ticker))
        if 'peers' in iex_datasets or extract_iex:
            iex_peers_df, iex_peers_df = \
                iex_extract_utils.extract_peers_dataset(
                    extract_req)
            if iex_peers_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_peers={}'.format(ticker))
        if 'news' in iex_datasets or extract_iex:
            iex_news_status, iex_news_df = \
                iex_extract_utils.extract_news_dataset(
                    extract_req)
            if iex_news_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_news={}'.format(ticker))
        if 'financials' in iex_datasets or extract_iex:
            iex_financials_status, iex_financials_df = \
                iex_extract_utils.extract_financials_dataset(
                    extract_req)
            if iex_financials_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_financials={}'.format(ticker))
        if 'earnings' in iex_datasets or extract_iex:
            iex_earnings_status, iex_earnings_df = \
                iex_extract_utils.extract_dividends_dataset(
                    extract_req)
            if iex_earnings_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_earnings={}'.format(ticker))
        if 'dividends' in iex_datasets or extract_iex:
            iex_dividends_status, iex_dividends_df = \
                iex_extract_utils.extract_dividends_dataset(
                    extract_req)
            if iex_dividends_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_dividends={}'.format(ticker))
        if 'company' in iex_datasets or extract_iex:
            iex_company_status, iex_company_df = \
                iex_extract_utils.extract_dividends_dataset(
                    extract_req)
            if iex_company_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract iex_company={}'.format(ticker))
        # end of iex extracts

        if extract_yahoo:
            yahoo_options_status, yahoo_option_calls_df = \
                yahoo_extract_utils.extract_option_calls_dataset(
                    extract_req)
            yahoo_options_status, yahoo_option_puts_df = \
                yahoo_extract_utils.extract_option_puts_dataset(
                    extract_req)
            if yahoo_options_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract yahoo_options={}'.format(ticker))
            yahoo_pricing_status, yahoo_pricing_df = \
                yahoo_extract_utils.extract_pricing_dataset(
                    extract_req)
            if yahoo_pricing_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract yahoo_pricing={}'.format(ticker))
            yahoo_news_status, yahoo_news_df = \
                yahoo_extract_utils.extract_yahoo_news_dataset(
                    extract_req)
            if yahoo_news_status != SUCCESS:
                if verbose:
                    log.warning(
                        'unable to extract yahoo_news={}'.format(ticker))
        # end of yahoo extracts

        ticker_data = {}
        ticker_data['daily'] = iex_daily_df
        ticker_data['minute'] = iex_minute_df
        ticker_data['quote'] = iex_quote_df
        ticker_data['stats'] = iex_stats_df
        ticker_data['peers'] = iex_peers_df
        ticker_data['news1'] = iex_news_df
        ticker_data['financials'] = iex_financials_df
        ticker_data['earnings'] = iex_earnings_df
        ticker_data['dividends'] = iex_dividends_df
        ticker_data['company'] = iex_company_df
        ticker_data['calls'] = yahoo_option_calls_df
        ticker_data['puts'] = yahoo_option_puts_df
        ticker_data['pricing'] = yahoo_pricing_df
        ticker_data['news'] = yahoo_news_df

        if ticker not in algo_data_req:
            algo_data_req[ticker] = []

        algo_data_req[ticker].append({
            'id': dataset_id,  # id is currently the cache key in redis
            'date': extract_date,  # used to confirm dates in asc order
            'data': ticker_data
        })

        log.info(
            'extract - {} dataset={}'.format(
                percent_label,
                len(algo_data_req[ticker])))
        cur_idx += 1
    # end of for service_dict in extract_requests

    # this could be a separate celery task
    status = NOT_RUN
    if len(algo_data_req) == 0:
        msg = (
            '{} - nothing to test - no data found for tickers={} '
            'between {} and {}'.format(
                label,
                use_tickers,
                first_extract_date,
                last_extract_date))
        log.info(msg)
        return build_result.build_result(
            status=EMPTY,
            err=msg,
            rec=rec)

    # this could be a separate celery task
    try:
        log.info(
            'handle_data START - {} from {} to {}'.format(
                percent_label,
                first_extract_date,
                last_extract_date))
        algo.handle_data(
            data=algo_data_req)
        log.info(
            'handle_data END - {} from {} to {}'.format(
                percent_label,
                first_extract_date,
                last_extract_date))
    except Exception as e:
        msg = (
            '{} - algo={} encountered exception in handle_data '
            'tickers={} from '
            '{} to {} ex={}'.format(
                percent_label,
                algo.get_name(),
                use_tickers,
                first_extract_date,
                last_extract_date,
                e))
        if raise_on_err:
            if algo:
                log.error(
                    'algo={} failed in handle_data with debug_msg'
                    '={}'.format(
                        algo.get_name(),
                        algo.get_debug_msg()))
            log.error(msg)
            raise e
        else:
            log.error(msg)
            return build_result.build_result(
                status=ERR,
                err=msg,
                rec=rec)
    # end of try/ex

    # this could be a separate celery task
    try:
        log.info(
            'get_result START - {} from {} to {}'.format(
                percent_label,
                first_extract_date,
                last_extract_date))
        rec = algo.get_result()
        status = SUCCESS
        log.info(
            'get_result END - {} from {} to {}'.format(
                percent_label,
                first_extract_date,
                last_extract_date))
    except Exception as e:
        msg = (
            '{} - algo={} encountered exception in get_result '
            'tickers={} from '
            '{} to {} ex={}'.format(
                percent_label,
                algo.get_name(),
                use_tickers,
                first_extract_date,
                last_extract_date,
                e))
        if raise_on_err:
            if algo:
                log.error(
                    'algo={} failed in get_result with debug_msg'
                    '={}'.format(
                        algo.get_name(),
                        algo.get_debug_msg()))
            log.error(msg)
            raise e
        else:
            log.error(msg)
            return build_result.build_result(
                status=ERR,
                err=msg,
                rec=rec)
    # end of try/ex

    return build_result.build_result(
        status=status,
        err=msg,
        rec=rec)
# end of run_algo
