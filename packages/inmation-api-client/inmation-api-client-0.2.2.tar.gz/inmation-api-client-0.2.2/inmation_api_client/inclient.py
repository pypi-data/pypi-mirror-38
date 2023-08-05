import asyncio
from sys import exit
from inspect import isfunction
from inmation_api_client.wsclient import WSClient
from inmation_api_client.model import SubscriptionType

class Client(object):
    """ client class. """
    def __init__(self, ioloop=None):
        #Set up the API Client
        self._ws_client = WSClient(ioloop)
    
    async def disconnect_ws(self):
        """ Disconnect from the WebSocket server. """
        await self._ws_client.close()

    def _get_wsclient(self):
        return self._ws_client

    @staticmethod
    def enable_debug():
        WSClient.DEBUG_LOG = True

    @staticmethod
    def disable_debug():
        WSClient.DEBUG_LOG = False

    def get_ioloop(self):
        return self._ws_client.get_ioloop()

    def run_async(self, tasks=[]):
        if not isinstance(tasks, list):
            print("run_async: The tasks argument must be of type list")
            return
        if not tasks:
            print('run_async: The tasks should not be an empty list')
        self._ws_client.run_async(tasks)

    async def connect_ws(self, url, options):
        """Connect to the WebSocket server.

        Args:
            url (str): URL of the WebSocket
            options (object): Options object

        Returns:
            void
        """
        try:
            await self._ws_client.connect(url, options)
        except ConnectionRefusedError as e:
            exit(str(e))

    async def exec_function(self, context, library_name, function_name, function_arg, cbk, options=None):
        """Execute function.

        Args:
            context (dict): dict with object like {"p": "/System/Core/Test/Item1"}
            library_name (str): Library Script name.
            function_name (str): Library function name.
            function_arg (dict): Library function arguments packed in a dictionary
            cbk (function): Callback
            options (object): Options object
        Returns:
            void
        """
        await self._ws_client.exec_function(context, library_name, function_name, function_arg, cbk, options)

    def _on(self, event_name, closure):
        """ Subscribe a callback to an event. """
        if not isfunction(closure):
            return
        
        self._ws_client.on(event_name, closure)

    def on_children_count_changed(self, closure):
        """ on_children_count_changed. """
        self._on(SubscriptionType.ChildrenCountChanged, closure)

    def on_config_version_changed(self, closure):
        """ on_configuration_version_changed. """
        self._on(SubscriptionType.ConfigurationChanged, closure)

    def on_ws_connection_changed(self, closure):
        """ on_ws_connection_changed. """
        self._on(SubscriptionType.ConnectionChanged, closure)

    def on_data_changed(self, closure):
        """ on_data_changed. """
        self._on(SubscriptionType.DataChanged, closure)

    def on_error(self, closure):
        """ on_error. """
        self._on(WSClient.ERROR, closure)

    def on_message(self, closure):
        """ on_message. """
        self._on(WSClient.MESSAGE, closure)

    def on_connection(self, closure):
        """ on_connection. """
        self._on(WSClient.CONNECTION, closure)

    def on_user_state_changed(self, closure):
        """ on_user_state_changed. """
        self._on(SubscriptionType.UserStateChanged, closure)

    async def run_script(self, context, script, cbk, options=None):
        """Run script.

        Args:
            context ([Identity]): list of Identity {"p": "/System/Core/Test/Item1"}
            script (str): Script body
            cbk (function): Callback
            options (options): Options object

        Returns:
            void
        """
        await self._ws_client.run_script(context, script, cbk, options)

    async def read(self, items, cbk, options=None):
        """ Read item values.

        Args:
            items ([Item]]): list of Item {"p": "/System/Core/Test/Item1"}
            cbk (function): Callback
            options (object): Options object
        Returns:
            void
        """
        await self._ws_client.read(items, cbk, options)

    async def read_historical_data(self, items, start_time, end_time, number_of_intervals, cbk, options=None):
        """Read historical item values

        Args:
            items ([HistoricalDataItem]): list of HistoricalDataItem {
                    "p": "/System/Core/Test/Item1"
                    "aggregate": "AGG_TYPE_RAW"
                }
            start_time (str): Start time in UTC format
            end_time (str): Ent time in UTC format
            number_of_intervals (int): Number of intervals
            cbk (function): Callback
            options (object): Options object

        Returns:
            void
        """
        await self._ws_client.read_historical_data(items, start_time, end_time, number_of_intervals, cbk, options)

    async def read_raw_historical_data(self, items, start_time, end_time, page_limit, cbk, options=None):
        """Read raw historical item values.

        Args:
            items ([Item]): list of Item {"p": "/System/Core/Test/Item1"}
            start_time (str): Start time in UTC format.
            end_time (str): End time in UTC format.
            page_limit (int): The maximum number of item values per page.
            cbk (function): Callback
            options (object): Options object

        Returns:
            void
        """
        await self._ws_client.read_raw_historical_data(items, start_time, end_time, page_limit, cbk, options)

    async def subscribe(self, items, s_type, cbk=None):
        """Subscribe to various changes.

        Args:            
            items ([Item]): list of Item {"p": "/System/Core/Test/Item1"}
            s_type (str): subscription type, SubscriptionType.DataChanged
            cbk (function): Callback

        Returns:
            void
        """
        if s_type in SubscriptionType.get_all():
            await self._ws_client.subscribe(items, s_type, cbk=None)

    async def unsubscribe(self, items, s_type, cbk=None):
        """Unsubscribe from various changes.

        Args:            
            items ([Item]): list of Item {"p": "/System/Core/Test/Item1"}
            s_type (str): subscription type, SubscriptionType.DataChanged
            cbk (function): Callback

        Returns:
            void
        """
        if s_type in SubscriptionType.get_all():
            await self._ws_client.unsubscribe(items, s_type, cbk=None)

    async def write(self, items, cbk, options=None):
        """Write item values.

        Args:
            items ([ItemValue]): list of ItemValue {
                    "p": "/System/Core/Test/Item1",
                    "v": 10.5,
                    "q":  0, // Quality (optional)
                    "t": "2017-06-19T12:41:19.56Z" // timestamp (optional)
                }
            cbk (function): Callback
            options (object): Options object
        Returns:
            void
        """
        await self._ws_client.write(items, cbk, options=None)

    @property
    def ws_connection_info(self):
        """wsConnectionInfo.

        Returns:
            object: WSConnectionInfo with sessionid and autheticated flag
        """
        return self._ws_client.connection_info
