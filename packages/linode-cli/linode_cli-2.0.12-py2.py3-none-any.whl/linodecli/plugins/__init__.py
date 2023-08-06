from importlib import import_module
from os import listdir
from os.path import dirname

from linodecli.configuration import CLIConfig


# find first-party installed plugins
_available_files = listdir(dirname(__file__))
available = [f[:-3] for f in _available_files if f.endswith('.py') and f != '__init__.py']

# find third-party plugins are registered
cli_config = CLIConfig('', '', skip_config=True)
registered_plugins = cli_config.config.get('plugins', 'DEFAULT', fallback='').split(',')

available += registered_plugins

def invoke(name, args, context):
    """
    Given the plugin name, executes a plugin
    """
    if name not in available:
        raise ValueError('No plugin named {}'.format(name))

    plugin = import_module('linodecli.plugins.'+name)
    plugin.call(args, context)


class PluginContext:
    """
    This class contains all context information provided to plugins when invoked.
    This includes access to the underlying CLI object to access the user's account,
    and the CLI access token the user has provided.
    """
    def __init__(self, token, client):
        """
        Constructs a new PluginContext with the given information
        """
        self.token = token
        self.client = client
