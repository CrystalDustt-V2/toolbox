import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import Dict, List, Type
from pydantic import BaseModel

class PluginMetadata(BaseModel):
    name: str
    commands: List[str]
    engine: str
    version: str = "0.3.1-dev"
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

    def create_scaffold(self, plugin_name: str):
        """Create a new plugin directory with a template __init__.py."""
        plugin_name = plugin_name.lower().replace("-", "_")
        plugins_dir = Path(__file__).parent.parent / "plugins"
        new_plugin_dir = plugins_dir / plugin_name
        
        if new_plugin_dir.exists():
            raise Exception(f"Plugin '{plugin_name}' already exists.")
            
        new_plugin_dir.mkdir(parents=True)
        
        template = f"""import click
from toolbox.core.plugin import BasePlugin, PluginMetadata

class {plugin_name.capitalize()}Plugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name}",
            commands=["hello"],
            engine="python"
        )

    def register_commands(self, group):
        @group.group(name="{plugin_name}")
        def {plugin_name}_group():
            \"\"\"{plugin_name.capitalize()} plugin commands.\"\"\"
            pass

        @{plugin_name}_group.command(name="hello")
        @click.argument("name", default="World")
        def hello_command(name):
            \"\"\"A simple hello command.\"\"\"
            click.echo(f"Hello, {{name}}! This is the {plugin_name} plugin.")
"""
        with open(new_plugin_dir / "__init__.py", "w") as f:
            f.write(template)
        
        return str(new_plugin_dir)

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
