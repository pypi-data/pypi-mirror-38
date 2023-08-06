"""
ExoEdge module. Provides high-level functionality to play nicely
with Exosite's Remote Condition Monitoring solution for Industrial IoT.
"""
# pylint: disable=W1202
import json
import time
from murano_client.client import StoppableThread, WatchQueue
from exoedge import logger

LOG = logger.getLogger(__name__)


class DataIn(StoppableThread, object):
    """
        This class has two threads for getting outbound data
        into the data_in resource:

        * DataInWriter:
            Waits on a queue for payload objects to write to data_in.

        * DataInWriter.DataWatcher
            Monitors all channels continuously and iteratively and
            puts all channel data (including __error channel) in the
            DataInWriter queue.

        Any channel that has its 'put_sample' or 'put_channel_error'
        method called will be processed for upload here.
    """
    def __init__(self, **kwargs):
        """
        DataInWriter initialized by ExoEdge.go()

        Parameters:
            device: murano_client.client.Client() object.
            config_io: exoedge.config_io.ConfigIO() object.
        """
        StoppableThread.__init__(self, name='DataInWriter')
        self.device = kwargs.get('device')
        self.config_io = kwargs.get('config_io')
        self.q_outbound_data = WatchQueue()

    def channel_data_watcher(self):
        """ Process Channel queues for data and errors. This thread is
        responsible for all channel data getting into the outbound queue.
        """
        while True:
            data_in = {}
            __error_channel = {'__error': []}
            for name, channel in self.config_io.channels.items():
                if not channel.q_out.empty():
                    # FEATURE_IMPLEMENTATION: report_rate
                    if channel.is_report_time():
                        downsampled = channel.downsampler.down_sample(
                            list(channel.q_out.queue))
                        # FEATURE_IMPLEMENTATION: report_on_change
                        if not channel.protocol_config.report_on_change:
                            data_in[name] = downsampled
                            channel.set_report_stats(downsampled, time.time())
                        else:
                            # FEATURE_IMPLEMENTATION: report_on_change_tolerance
                            # LOG.critical("report_on_change: {}: {}: {}: {}".format(name, channel, downsampled, channel.last_value))
                            value = channel.ROCH.filter_data(downsampled, channel.last_value)
                            if value is not None:
                                LOG.warning("report_on_change_tolerance (changed): {} :: {}"
                                            .format(value, channel.last_value))
                                data_in[name] = value
                                channel.set_report_stats(value, time.time())
                            else:
                                LOG.info("report_on_change_tolerance (unchanged): ({}) > {} :: {}"
                                         .format(
                                             channel.protocol_config.report_on_change_tolerance,
                                             downsampled,
                                             channel.last_value
                                         )
                                        )
                        channel.q_out.queue.clear()
                while not channel.q_error_out.empty():
                    error = channel.q_error_out.safe_get(timeout=0.001)
                    if error:
                        __error_channel['__error'].append({name: error})

            if data_in:
                self.q_outbound_data.put(data_in)
            if __error_channel.get('__error'):
                self.q_outbound_data.put(__error_channel)
            time.sleep(0.01)

    def run(self):
        """
            Process the outbound queue that DataInWriter.DataWatcher
            fills with channel data and errors.
        """
        LOG.debug('starting')
        data_watcher = StoppableThread(
            name="DataInWriter.DataWatcher",
            target=self.channel_data_watcher
        )
        data_watcher.setDaemon(True)
        data_watcher.start()

        # keep the logs less noisy
        last_debug_msg = 0.0
        while not self.is_stopped():

            data = self.q_outbound_data.safe_get(timeout=0.5)

            if data:
                LOG.critical(
                    'WRITING DATA: {}'
                    .format(data)
                )
                self.device.tell(
                    resource='data_in',
                    timestamp=time.time(),
                    payload=json.dumps(data)
                )
            else:
                now = time.time()
                if now - last_debug_msg >= 5.0:
                    LOG.debug('NO DATA TO SEND')
                    last_debug_msg = now

        LOG.debug('exiting')
