import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import Dict, List, Type
from pydantic import BaseModel

class PluginMetadata(BaseModel):
    name: str
    commands: List[str]
    engine: str
    dependencies: List[str] = []

class BasePlugin(ABC):
    def __init__(self):
        self.metadata = self.get_metadata()

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        pass

    @abstractmethod
    def register_commands(self, group):
        """Register click commands to the main group."""
        pass

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}

    def load_plugins(self, package_name: str = "toolbox.plugins"):
        package = importlib.import_module(package_name)
        for _, name, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                plugin_module_name = f"{package_name}.{name}"
                try:
                    module = importlib.import_module(plugin_module_name)
                    # Look for a class that inherits from BasePlugin
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if (isinstance(item, type) and 
                            issubclass(item, BasePlugin) and 
                            item is not BasePlugin):
                            plugin_instance = item()
                            self.plugins[plugin_instance.metadata.name] = plugin_instance
                except Exception as e:
                    print(f"Failed to load plugin {name}: {e}")

plugin_manager = PluginManager()
