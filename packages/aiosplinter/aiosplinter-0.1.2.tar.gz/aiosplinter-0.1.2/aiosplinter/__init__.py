import sys

import importlib
import inspect
import types

from aioify import aioify
import selenium.webdriver
import splinter
import poetry_version

webdrivers = []
for _, module in inspect.getmembers(object=selenium.webdriver):
    # noinspection PyUnresolvedReferences
    if isinstance(module, types.ModuleType):
        webdrivers_module = importlib.import_module(name=module.__name__)
        if hasattr(webdrivers_module, 'webdriver'):
            webdrivers.append(webdrivers_module.webdriver.WebDriver)


__version__ = poetry_version.extract(source_file=__file__)
aiosplinter = aioify(obj=splinter, name=__name__, skip=webdrivers, wrap_return_values=True)

sys.modules[__name__] = aiosplinter
from aiosplinter import *
