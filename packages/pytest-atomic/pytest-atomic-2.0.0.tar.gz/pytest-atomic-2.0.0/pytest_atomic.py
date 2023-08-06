import pytest


class Section:

    def __init__(self, config):
        try:
            self._sections = config.inicfg.config.sections.get('atomic', dict())
        except AttributeError:
            self._sections = dict()

    @property
    def enable(self):
        return self._sections.get('enable', 'false').lower() == 'true'

    @property
    def electronic(self):
        return self._sections.get('electronic', 'true').lower() == 'true'


class Atomic:
    def __init__(self, config: Section):
        self.config = config

    def pytest_runtest_setup(self, item):
        if item.get_closest_marker('atomic'):
            item.parent._previous_failed = False
        if getattr(item.parent, '_previous_failed', False):
            if not item.get_closest_marker('electronic'):
                pytest.skip(item.parent._skip_reason)
            else:
                if not self.config.electronic:
                    pytest.skip(item.parent._skip_reason)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        report = outcome.get_result()
        if report.failed and item.get_closest_marker('atomic'):
            item.parent._previous_failed = True
            item.parent._skip_reason = item.get_closest_marker('atomic').args[0] if item.get_closest_marker(
                'atomic').args else 'This is atomic testsuit!'


def pytest_configure(config):
    c = Section(config)
    if c.enable:
        atomic_plugin = Atomic(c)
        config._atomic_plugin = atomic_plugin
        config.pluginmanager.register(atomic_plugin)


def pytest_unconfigure(config):
    plugin = getattr(config, '_atomic_plugin', None)
    if plugin is not None:
        del config._atomic_plugin
        config.pluginmanager.unregister(plugin)
