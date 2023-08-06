import importlib
import importlib.util
import inspect
import os


class PluginBase:
    @classmethod
    def __implemented_methods__(cls):
        result = []

        for plugin_base in cls.__bases__:
            if not issubclass(plugin_base, cls):
                continue

            for attr in dir(plugin_base):
                if attr.startswith("_") or getattr(cls, attr) == getattr(plugin_base, attr):
                    continue

                result.append(attr)

        return result


def _set_or_create(value, generator, on=None, args: list=None, kwargs: dict=None):
    if not args:
        args = []
    if not kwargs:
        kwargs = {}

    if value == on:
        return generator(*args, **kwargs)

    return value


class PluginSystemLoader:
    base_class = PluginBase

    def __init__(self, plugin_module_base="plugins", recursive=False, path=None, follow_link=False, debug=False):
        self.plugin_module_base = plugin_module_base
        self.path = _set_or_create(path, self._get_plugin_folder, None)

        self.follow_link = follow_link
        self.recursive = recursive
        self.debug = debug
        self.modules = None
        self.plugins = None

        self.reload(discard=True)

    def reload(self, discard=False):
        if discard:
            self.modules = None
            self.plugins = None

        modules = self._enumerate_plugin_folder(self.path, self.follow_link, self.recursive)
        self.modules = self._load_modules(modules, self.debug)
        self.plugins = self._load_plugins()

    def _get_plugin_folder(self):
        for path in importlib.import_module(self.plugin_module_base).__path__:
            return path

        raise ModuleNotFoundError(self.plugin_module_base)

    def _enumerate_plugin_folder(self, folder, follow_link=False, recursive=False):
        files = []
        for sub_element in os.listdir(folder):
            sub_element = os.path.join(folder, sub_element)
            if os.path.islink(sub_element) and not follow_link:
                continue
            elif os.path.isfile(sub_element):
                files.append(sub_element)
            elif os.path.isdir(sub_element) and recursive:
                files.extend(self._enumerate_plugin_folder(sub_element, follow_link))

        return files

    @classmethod
    def _load_modules(cls, module_paths, debug=False):
        modules = []
        for path in module_paths:
            spec = importlib.util.spec_from_file_location("module", path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                modules.append(module)
            except Exception as e:
                if debug:
                    raise e
                print(e)
                continue

        return modules

    def _load_plugins(self):
        plugins = []

        for module in self.modules:
            for attr in dir(module):
                if attr.startswith("_"):
                    continue

                attr = getattr(module, attr)

                if inspect.isclass(attr)\
                        and issubclass(attr, self.base_class)\
                        and not (attr == self.base_class
                                 or attr == PluginBase == attr):
                    plugins.append(attr)

        return plugins
