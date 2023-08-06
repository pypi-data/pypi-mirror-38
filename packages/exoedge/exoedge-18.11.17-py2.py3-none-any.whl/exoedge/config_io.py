# pylint: disable=W0141,W0110,C0103,W1202
"""
    ExoEdge ConfigIO module to handle Channel creation from a config_io object.
"""
from exoedge.configs import ExoEdgeConfig
from exoedge import logger
from exoedge.namespaces import get_nested_object
from exoedge.channel import Channel, DataOutChannel
from exoedge.constants import DEFAULTS

LOG = logger.getLogger(__name__)

class ConfigIO(ExoEdgeConfig, object):
    """
    This class provides methods to create channels from a
    config_io and to format the data_in object to be sent
    to Murano.

    Required Inputs:
        device: a murano_client.client.Client() object
                for the connection to Murano.

    Optional Inputs:
        config:         a config_io object (dictionary).
        config_io_file: path to a JSON file containing
                        the config_io object.
        wait_timeout:   timeout, in seconds, between
                        printing 'no new config' to
                        the log (default:1.0).

    """
    resource = 'config_io'
    def __init__(self, **kwargs):
        ExoEdgeConfig.__init__(
            self,
            name="ConfigIO",
            device=kwargs.get('device'),
            config_file=kwargs.get(
                'config_io_file',
                DEFAULTS['config_io_file']
            )
        )
        self.wait_timeout = float(kwargs.get('wait_timeout', 1.0))
        self.set_config(kwargs.get('config'))
        # schema: {"$channel_id": <Channel instance>}
        self.channels = {}

    def stop(self):
        """ Stop all activity.

        Stops activity of all Channel threads, Channel-
        Watcher threads, and the ConfigIO thread.
        """
        LOG.warning("Stopping ConfigIO...")
        self.stop_all_channels()
        super(ConfigIO, self).stop()

    def has_channels(self):
        """ Return whether or not ConfigIO has channels.

        Used to determine if there are channels to stop.
        """
        return bool(self.channels)

    def _add_channel(self, name, ch_cfg):
        """ Create Channel and DataOutChannel objects.

        Create a Channels and DataOutChannels from a channel
        configuration object. Store them in the ConfigIO.channels
        dictionary.

        Parameters:
        ch_cfg:     the object representation of the channel
                    taken from config_io.
        name:       the key of the ch_cfg object in config_io

        """
        LOG.info('adding channel %s', name)
        ch_cfg['name'] = name
        if get_nested_object(ch_cfg, ['properties', 'data_out']):
            self.channels[name] = DataOutChannel(**ch_cfg)
        else:
            self.channels[name] = Channel(**ch_cfg)

    def stop_all_channels(self):
        """ Stop Channel threads.

        Call channel.stop() for all Channels in ConfigIO.channels.
        Called by ConfigIO.run() when a new config_io is received.
        """
        LOG.warning('stopping all channels')
        for _, channel in self.channels.items():
            LOG.warning("Stopping ExoEdgeSource: {}".format(channel))
            channel.stop_source()
        self.channels = {}

    def run(self):
        """ Update ConfigIO and Channels upon new config_io.

        Waits for a new config_io event set by ConfigIO.set_config_io() and
        subsequently stops existing channels before creating new channels from
        the newly received config_io object. Starts Channels and ChannelWatchers.
        """
        LOG.debug('starting')
        while not self.is_stopped():
            if self.event_new_config.wait(self.wait_timeout):
                with self._lock:
                    if self.config:
                        LOG.debug('Received config_io')

                        if self.has_channels():
                            self.stop_all_channels()

                        if 'channels' in self.config.keys():
                            for name, cfg in self.config['channels'].items():
                                self._add_channel(name, cfg)

                            # start all Channels and ChannelWatchers
                            for channel in self.channels.values():
                                LOG.warning("STARTING CHANNEL: {}".format(dict(channel)))
                                channel.start_source()

                        else:
                            LOG.critical('Received new config_io without channels.')
                    else:
                        LOG.info("No new config_io received.")
                self.event_new_config.clear()

            else:
                LOG.debug('no new config')
        LOG.debug('exiting')


