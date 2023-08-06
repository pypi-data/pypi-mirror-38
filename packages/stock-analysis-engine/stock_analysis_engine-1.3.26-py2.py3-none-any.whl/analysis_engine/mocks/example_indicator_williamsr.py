"""
Example Custom Williams Percent R Indicator that
uses Open instead of Close

**Supported environment variables**

::

    # to show debug, trace logging please export ``SHARED_LOG_CFG``
    # to a debug logger json file. To turn on debugging for this
    # library, you can export this variable to the repo's
    # included file with the command:
    export SHARED_LOG_CFG=/opt/sa/analysis_engine/log/debug-logging.json
"""

import analysis_engine.talib as talib
import analysis_engine.indicators.base_indicator as base_indicator
import spylunking.log.setup_logging as log_utils

log = log_utils.build_colorized_logger(name=__name__)


class ExampleIndicatorWilliamsR(base_indicator.BaseIndicator):
    """ExampleIndicatorWilliamsR"""

    def __init__(
            self,
            **kwargs):
        """__init__

        Custom indicator example for showing a Williams Percent R
        within an algo for analyzing intraday minute datasets

        Please refer to the `analysis_engine.indicators.base_indicator.Ba
        seIndicator source code for the latest supported parameters <ht
        tps://github.com/AlgoTraders/stock
        -analysis-engine/blob/master/
        analysis_engine/indicators/base_indicator.py>`__

        :param kwargs: keyword arguments
        """
        super().__init__(**kwargs)
    # end of __init__

    def process(
            self,
            algo_id,
            ticker,
            dataset):
        """process

        Derive custom indicator processing to determine buy and sell
        conditions before placing orders. Just implement your own
        ``process`` method.

        Please refer to the TA Lib guides for details on building indicators:

        - Overlap Studies
          https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        - Momentum Indicators
          https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
        - Volume Indicators
          https://mrjbq7.github.io/ta-lib/func_groups/volume_indicators.html
        - Volatility Indicators
          https://mrjbq7.github.io/ta-lib/func_groups/volatility_indicators.html
        - Price Transform
          https://mrjbq7.github.io/ta-lib/func_groups/price_transform.html
        - Cycle Indicators
          https://mrjbq7.github.io/ta-lib/func_groups/cycle_indicators.html
        - Pattern Recognition
          https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html
        - Statistic Functions
          https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        - Math Transform
          https://mrjbq7.github.io/ta-lib/func_groups/math_transform.html
        - Math Operators
          https://mrjbq7.github.io/ta-lib/func_groups/math_operators.html

        :param algo_id: string - algo identifier label for debugging datasets
            during specific dates
        :param ticker: string - ticker
        :param dataset: dictionary of ``pd.DataFrame(s)`` to process
        """
        label = (
            '{} process ticker={}'.format(
                self.name,
                ticker))

        log.info(
            '{} - start'.format(
                label))

        daily_df = self.get_subscribed_dataset(
                dataset=dataset)

        # notice the self.num_points is now a member variable
        # because the BaseIndicator class's __init__
        # converts any self.config keys into useable
        # member variables automatically in your derived class
        log.info(
            '{} - processing - num_points={} daily_df={}'.format(
                label,
                self.num_points,
                len(daily_df.index)))
        """
        real = WILLR(high, low, close, timeperiod=14)
        """
        self.willr_value = None
        num_records = len(daily_df.index)
        if num_records > self.num_points:
            first_date = daily_df['date'].iloc[0]
            end_date = daily_df['date'].iloc[-1]
            start_row = num_records - self.num_points
            use_df = daily_df[start_row:num_records]
            """
            for idx, row in daily_df[start_row:-1].iterrows():
                high = row['high']
                low = row['low']
                open_val = row['open']
                close = row['close']
                row_date = row['date']
                log.info(
                    '{} - {} - WILLR(high={}, low={}, '
                    'close={}, period={})'.format(
                        label,
                        row_date,
                        high,
                        low,
                        close,
                        self.num_points))
            """
            highs = use_df['high'].values
            lows = use_df['low'].values
            closes = use_df['close'].values
            willr_values = talib.WILLR(
                highs,
                lows,
                closes,
                self.num_points)
            self.willr_value = willr_values[-1]
            log.info(
                '{} - end - {} to {} willr_value={}'.format(
                    label,
                    first_date,
                    end_date,
                    self.willr_value))
        else:
            log.info(
                '{} - end - willr={}'.format(
                    label,
                    self.willr_value))
    # end of process

# end of ExampleIndicatorWilliamsR


def get_indicator(
        **kwargs):
    """get_indicator

    Make sure to define the ``get_indicator`` for your custom
    algorithms to work as a backup with the ``sa.py`` tool...
    Not anticipating issues, but if we do with importlib
    this is the backup plan.

    Please file an issue if you see something weird and would like
    some help:
    https://github.com/AlgoTraders/stock-analysis-engine/issues

    :param kwargs: dictionary of keyword arguments
    """
    log.info('getting indicator')
    return ExampleIndicatorWilliamsR(**kwargs)
# end of get_indicator
