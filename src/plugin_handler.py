import logging
import sys
import importlib
import os

from rich.logging import RichHandler

log = logging.getLogger("rich")
plugins = list()

log = logging.getLogger("rich")
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(
        rich_tracebacks=True,
        markup=True,
    )]
)


def import_plugin(args) -> None:
    global plugins

    # check if plugins are given
    if args.plugin is None or args.plugin == []:
        return None

    # plugins are not supported in frozen mode
    if getattr(sys, 'frozen', False):
        log.error(
            "Application is Frozen! Plugins are not supportet in a frozen state, since they require dynamic imports and execution!\nPlugin will not be used.")
        return None

    # search and import plugins
    for plugin in args.plugin:
        if (plugin is not None) and (plugin != []):
            if not os.path.exists(plugin):
                log.error("Could not find", plugin, "to be a valid path")
                continue
            # split plugin path
            plugin_path, plugin_name = os.path.split(plugin)

            log.debug(
                "loading plugin at {} {}".format(
                    plugin_path, plugin_name))

            # add plugins path to python search path
            sys.path.insert(0, plugin_path)

            # dynamically import plugin
            try:
                plugins.append(importlib.import_module(plugin_name))
            except Exception as e:
                log.error(
                    'Exception Occured while importing plugin',
                    exc_info=e)

    # call plugins init
    call_plugin(0, args)


def call_plugin(state, args, dataframe=None) -> any:
    global plugins
    log.debug("Calling Plugin with State: {}".format(state))

    # return if frozen
    if getattr(sys, 'frozen', False):
        return dataframe

    plugin_dataframe = None

    for plugin in plugins:
        if plugin is not None:
            plugin_dataframe = dataframe
            try:
                if state == 0:
                    plugin.init_hook(log, args)
                elif state == 1:
                    plugin_dataframe = plugin.read_hook(
                        log, args, plugin_dataframe)
                elif state == 2:
                    plugin_dataframe = plugin.modify_hook(
                        log, args, plugin_dataframe)
                elif state == 3:
                    plugin_dataframe = plugin.scale_hook(
                        log, args, plugin_dataframe)
                elif state == 4:
                    plugin.save_hook(log, args, plugin_dataframe)

            except Exception as e:
                log.error(
                    'Exception Occured while calling plugin (State: {})'.format(
                        state),
                    exc_info=e)

    if plugin_dataframe is not None:
        return plugin_dataframe
    else:
        return dataframe
