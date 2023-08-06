import pkg_resources


class NoProcessorAvailable(Exception): pass


class PluginController(object):
    plugins = None

    def find_processor(self, filetype, resource_name):
        self.load_plugins()

        specific = (filetype + '.' + resource_name).lower()
        general = filetype.lower()

        if specific in self.plugins:
            return self.plugins[specific]
        if general in self.plugins:
            return self.plugins[general]

        raise NoProcessorAvailable("Could not find processors for '{type}'".format(
            type=specific
        ))

    def load_plugins(self):
        if self.plugins is None:
            self.plugins = {}
            for entry_point in pkg_resources.iter_entry_points('datagovuk.plugins.processors'):
                try:
                    plugin_class = entry_point.load()
                    plugin = plugin_class()
                    for handler in plugin.handlers:
                        self.plugins[handler] = plugin
                except pkg_resources.DistributionNotFound as e:
                    pass
                    # Continue to load entry_points


plugins = PluginController()
