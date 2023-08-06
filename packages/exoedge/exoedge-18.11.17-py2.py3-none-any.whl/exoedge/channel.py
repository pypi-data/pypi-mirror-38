# -*- coding: utf-8 -*-
# pylint: disable=C0103,R0902,W1202
"""
Module to generate data from arbitrary source modules as defined in config_io.
"""
import os
import sys
import time
import json
import threading
import inspect
from exoedge import logger
from exoedge.namespaces import ChannelNamespace
from exoedge.sources import ExoEdgeSource
from murano_client.client import WatchQueue, StoppableThread

path = os.path.dirname(
    os.path.realpath(__file__)
).rsplit('/', 1)[0] + '/exoedge/sources'
sys.path.append(path)

LOG = logger.getLogger(__name__)


class NeverEndingCallbacks(object):
    def __init__(self, callback, interval, function, args, kwargs):
        self.callback = callback
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.call_again()

    def call_again(self):
        LOG.warning(
            "call_again: calling: {} with: {} and {}"
            .format(self.function, self.args, self.kwargs)
        )
        self.callback(self.function(*self.args, **self.kwargs))
        self.timer = threading.Timer(
            self.interval,
            self.call_again)
        self.timer.start()

    def start(self):
        LOG.info("starting timer...")
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

class Channel(ChannelNamespace, object):
    """
    A Channel creates Signal data for ExoSense.

    This class provides methods to get new data from a source specified in
    config_io.
    """
    def __init__(self, **kwargs):
        """
            Channel initialized and started by
            config_io.ConfigIO.add_channel()
        """
        LOG.info("Channel kwargs: {}".format(kwargs))
        if kwargs.get('__no_derived__'):
            kwargs['__ns_no_defaults__'] = True
            kwargs.pop('__no_derived__')
        ChannelNamespace.__init__(self, **kwargs)

        # DERIVED
        if not kwargs.get('__ns_no_defaults__'):
            self.downsampler = DownSampler(self.protocol_config.down_sample) # pylint: disable=E1101
            self.ROCH = ReportOnChangeHandler(
                self.protocol_config.report_on_change,  # pylint: disable=E1101
                tolerance=self.protocol_config.report_on_change_tolerance) # pylint: disable=E1101
        elif '__ns_no_defaults__' in kwargs:
            kwargs.pop('__ns_no_defaults__')
        self.last_value = None
        self.last_report_time = 0
        self.last_sample = 0
        self.q_out = WatchQueue()
        self.q_error_out = WatchQueue()
        self.source = None
        self.callback_timer = None

    def start_source(self):
        """
            TODO
        """
        LOG.warning(
            "Starting source:: {}"
            .format(dict(self))
        )

        if self.protocol_config.application.startswith(u'Modbus_'): # pylint: disable=E1101
            src = __import__('exoedge_modbus')
            self.source = src.ModbusExoEdgeSource()
            self.source.get_source()

        elif self.protocol_config.application == u'CANOpen': # pylint: disable=E1101
            src = __import__('exoedge_canopen')
            self.source = src.CanopenExoEdgeSource()
            self.source.get_source()

        elif self.protocol_config.application == u'ExoSimulator': # pylint: disable=E1101
            LOG.critical("Loading ExoSimulator...")
            if 'exoedge.sources.exo_simulator' in sys.modules:
                LOG.warning("ExoSimulator already loaded.")
                self.source = None
            else:
                src = __import__('exoedge.sources.exo_simulator')
                self.source = src.sources.exo_simulator.ExoSimulator()
                self.source.get_source()

        elif self.protocol_config.application == 'ExoEdgeSource': # pylint: disable=E1101
            module = self.protocol_config.app_specific_config.get('module') # pylint: disable=E1101
            if module in sys.modules:
                LOG.critical(
                    "ExoEdgeSource module {} already loaded."
                    .format(module)
                )
                src = None
            else:
                LOG.critical(
                    "Loading ExoEdgeSource module: {}"
                    .format(module)
                )
                src = __import__(module)
                LOG.info("module imported: {}".format(src))
                src_class = None
                for e in dir(src):
                    src_attr = getattr(src, e)
                    if inspect.isclass(src_attr):
                        if issubclass(src_attr, ExoEdgeSource) and e != 'ExoEdgeSource':
                            src_class = src_attr
                if src_class:
                    LOG.critical(
                        "Starting ExoEdgeSource: {}"
                        .format(src_class)
                    )
                    self.source = src_class(
                        name='.'.join([module, src_class.__name__])
                    ).get_source()
                    LOG.critical(
                        "ExoEdgeSource {} is_started? {}"
                        .format(self.source, self.source.is_started())
                    )
                else:
                    LOG.critical(
                        "No class in {} that inherits from ExoEdgeSource"
                        .format(src)
                    )

        else:
            # classic style
            LOG.critical(
                "no supported source found. using generic module.function(*args, **kwargs) style.")
            src = __import__(self.protocol_config.app_specific_config['module']) # pylint: disable=E1101
            self.callback_timer = NeverEndingCallbacks(
                self.put_sample,
                self.protocol_config.sample_rate / 1000.0, # pylint: disable=E1101
                getattr(src, self.protocol_config.app_specific_config['function']), # pylint: disable=E1101
                self.protocol_config.app_specific_config['positionals'], # pylint: disable=E1101
                self.protocol_config.app_specific_config['parameters'] # pylint: disable=E1101
            )

        LOG.critical("Source started:: {}".format(self.source))

    def stop_source(self):
        """
            Tear down channel objects, stop threads, etc.
        """
        LOG.warning("stopping source: {}".format(self))
        if self.protocol_config.application.startswith(u'Modbus_'): # pylint: disable=E1101
            if 'exoedge_modbus' in sys.modules:
                sys.modules.pop('exoedge_modbus')
            if self.source:
                self.source.stop()
                self.source.join(0.5)
        elif self.protocol_config.application == u'CANOpen': # pylint: disable=E1101
            if 'exoedge_canopen' in sys.modules:
                sys.modules.pop('exoedge_canopen')
            if self.source:
                self.source.stop()
                self.source.join(0.5)
        elif self.protocol_config.application == u'ExoSimulator': # pylint: disable=E1101
            if 'exoedge.sources.exo_simulator' in sys.modules:
                sys.modules.pop('exoedge.sources.exo_simulator')
            if self.source:
                self.source.stop()
                self.source.join(0.5)
        elif isinstance(self.source, ExoEdgeSource):
            self.source.stop()
            # this so import of ExoEdgeSource will happen correctly
            # in start_source() after successive reloads of config_io
            module = self.protocol_config.app_specific_config.get('module') # pylint: disable=E1101
            if module in sys.modules:
                sys.modules.pop(module)
            if self.source:
                self.source.stop()
                self.source.join(0.5)
        elif self.callback_timer:
            self.callback_timer.cancel()
            # wait for one interval for graceful shutdown
            time.sleep(self.callback_timer.interval)
        else:
            LOG.critical("Don't know how to stop source: <({} ){}>"
                         .format(type(self.source), self.source))
        # self.source = None

    def is_sample_time(self, blocking=False):
        """ Sleep for the sample rate

        # FEATURE_IMPLEMENTATION: sample_rate
        """
        sr = self.protocol_config.sample_rate / 1000.0 # pylint: disable=E1101
        if blocking:
            time.sleep(sr)
        diff = time.time() - self.last_sample
        is_sample_time = diff >= sr
        return is_sample_time

    def put_sample(self, sample):
        """ Place data in queue.

        In the future, this method will be switchable and optionally send
        data to gmq or SQL database, e.g. send_data_to_gmq(data)

        Parameters:
        sample:           Datapoint to be placed in queue.
        """
        LOG.info(
            "putting sample({}): {}"
            .format(self.name, sample) # pylint: disable=E1101
        )
        data = Data(
            sample,
            gain=self.protocol_config.multiplier, # pylint: disable=E1101
            offset=self.protocol_config.offset) # pylint: disable=E1101
        self.q_out.put(data)
        self.last_sample = data.ts

    def put_channel_error(self, error):
        """
            Helper method for sending data on the __error channel.
        """
        LOG.info(
            "putting error: {}"
            .format(error)
        )
        self.q_error_out.put(str(error))
        self.last_sample = time.time()

    def set_report_stats(self, last_value, last_report_time):
        """
            Update channel stats last_value and last_report_time.
        """
        LOG.debug(
            "stats ({}): {}, {}"
            .format(self.name, last_value, last_report_time) # pylint: disable=E1101
        )
        self.last_value = last_value
        self.last_report_time = last_report_time

    def is_report_time(self):
        """
            Determine whether or not it is time to send queued channel data.
        """
        now = time.time()
        should_report_by = self.last_report_time + self.protocol_config.report_rate / 1000.0 # pylint: disable=E1101
        if self.protocol_config.report_on_change or now >= should_report_by: # pylint: disable=E1101
            return True
        return False

class ExecuteDataOut(StoppableThread):
    def __init__(self, channel, data_out_value):
        StoppableThread.__init__(self, name="DataOut-{}".format(channel.name))
        self.channel = channel
        self.data_out_value = data_out_value

    def run(self):
        LOG.critical(
            "{} starting..."
            .format(self.__class__.__name__)
        )

        if self.channel.protocol_config.application.startswith(u'Modbus_'): # pylint: disable=E1101
            src = __import__('exoedge_modbus')
            source = src.ModbusExoEdgeSource()
            source.put_data_out(self.channel, self.data_out_value)

        elif self.channel.protocol_config.application == "CANOpen": # pylint: disable=E1101
            src = __import__('exoedge_canopen')
            source = src.CANOpenExoEdgeSource()
            source.put_data_out(self.channel, self.data_out_value)

        elif self.channel.protocol_config.application == u'ExoSimulator': # pylint: disable=E1101
            src = __import__('exoedge.sources.exo_simulator')
            source = src.sources.exo_simulator.ExoSimulator()
            source.put_data_out(self.channel, self.data_out_value)

        else:
            # classic style
            LOG.critical("Unsupported source. Using 'module.function(*args, **kwargs)' style.")
            LOG.info("channel: {}".format(dict(self.channel)))
            module = __import__(self.channel.protocol_config.app_specific_config['module']) # pylint: disable=E1101

            function = getattr(
                module,
                self.channel.protocol_config.app_specific_config['function'] # pylint: disable=E1101
            )
            positionals = self.data_out_value.get('positionals')
            parameters = self.data_out_value.get('parameters')
            LOG.info("module: {}".format(module))
            LOG.info("function: {}".format(function))
            LOG.info("positionals: {}".format(positionals))
            LOG.info("parameters: {}".format(parameters))
            try:
                # call function
                result = function(*positionals, **parameters)
                LOG.warning("result: {}".format(result))
                self.channel.put_sample(result)
            except Exception as exc:
                msg = "Unable to call {}.{}(*{}, **{})".format(
                    module, function, positionals, parameters
                )
                LOG.exception(msg)
                self.channel.put_channel_error("{}\n{}".format(msg, exc))

class DataOutChannel(Channel):
    """
        Class for processing command and control from ExoSense
        via the data_out resource.

        Each instance represents an asynchronous thread. All
    """
    resource = 'data_out'
    def __init__(self, **kwargs):
        LOG.critical("DataOutChannel kwargs: {}".format(kwargs))
        Channel.__init__(self, **kwargs)

    def start_source(self):
        LOG.critical(
            "This is a 'data_out' channel, "
            "only ExoSense-initiated commands results in channel data.")

    def stop_source(self):
        pass

    def is_sample_time(self, blocking=False):
        return False

    def is_report_time(self):
        return True

    def execute(self, data_out_value):
        LOG.critical("Starting DataOut source:: {}".format(dict(self)))
        LOG.critical("DataOut payload:: {}".format(data_out_value))

        data_out_thread = ExecuteDataOut(self, data_out_value)
        data_out_thread.start()


class Data(tuple):
    """ Class to attach a timestamp to new data that is generated """
    def __new__(cls, d, **kwargs):
        """ Subclasses tuple. (timestamp, data) """
        cls.ts = time.time()
        cls.offset = kwargs.get('offset')
        cls.gain = kwargs.get('gain')
        if not isinstance(d, bool):
            try:
                cls.d = d * cls.gain + cls.offset
            except TypeError:
                cls.d = d
            # Attempt to JSON serialize the data point. If not
            # serializable, force into string.
            try:
                LOG.debug("data (json): {}".format(json.dumps(cls.d)))
            except TypeError:
                cls.d = str(cls.d)
        else:
            # support bool-type data
            cls.d = d

        return tuple.__new__(Data, (cls.ts, cls.d))

    def age(self):
        """ Return age of data point in seconds """
        return time.time() - self.ts


class DownSampler(object):
    """ Class to deal with down sampling Channel data

    Methods:
    max:            Maximum value in list
    min:            Minimum value in list
    sum:            Sum of values in list
    avg:            Average of values in list
    act:            Last value in list ("actual value")
    """
    method_mapper = {
        'max': max,
        'min': min,
        'sum': sum,
        'avg': lambda ls: float(sum(ls))/len(ls),
        'act': lambda ls: ls[-1]    # ls.pop()
    }

    def __init__(self, method):
        """
        Initialized by Channel.__init__()
        """
        # TODO: remove this method check once THEMVE-2944 is fixed.
        if method == 'actual':
            method = 'ACT'
        self.method = method.lower()
        self._fn = self.method_mapper.get(self.method)
        if self._fn is None:
            LOG.critical("Couldn't map method: {}, using default: ACT".format(method))
            self._fn = self.method_mapper.get('act')

    def __repr__(self):
        return '<{}: {}>'.format(self.method, self._fn)

    def down_sample(self, data):
        """ Down sample data

        Assume data is list of tuples, e.g.
        [(ts, val), (ts, val), ...]
        """
        LOG.debug('Performing downsample %s on %s', self.method, data)
        try:
            return self._fn([d[1] for d in data])
        except:
            # kludge for non-tuple data
            return self._fn(data)


class ReportOnChangeHandler(object):
    def __init__(self, roc, tolerance=None):
        self.roc = roc
        self.tolerance = tolerance

    def filter_data(self, current, last):
        if self.roc and last is not None:
            # don't do math if you don't need to
            if self.tolerance:
                LOG.info(
                    "validating whether {} <= {} <= {}"
                    .format(
                        last - self.tolerance,
                        current,
                        last + self.tolerance)
                )
                if (last - self.tolerance) <= current <= (last + self.tolerance):
                    LOG.info("within range; not reporting")
                    return
            else:
                #
                if last == current:
                    return
        return current

