"""
Dynamic Plugin Manager System
Hot-reload support for agents, integrations, and modules
"""
import importlib
import importlib.util
import inspect
import sys
from typing import Dict, List, Optional, Type, Callable, Any
from pathlib import Path
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from loguru import logger
import hashlib
import os


# ============================================================================
# PLUGIN TYPES & STATUS
# ============================================================================

class PluginType(str, Enum):
    """Types of plugins"""
    AGENT = "agent"
    INTEGRATION = "integration"
    PAYMENT_PROVIDER = "payment_provider"
    ANALYTICS = "analytics"
    MIDDLEWARE = "middleware"
    AUTHENTICATION = "authentication"


class PluginStatus(str, Enum):
    """Plugin lifecycle status"""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    RUNNING = "running"
    ERROR = "error"
    DISABLED = "disabled"


# ============================================================================
# PLUGIN MODELS
# ============================================================================

class PluginMetadata(BaseModel):
    """Plugin metadata"""
    id: str
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    dependencies: List[str] = []
    api_version: str = "1.0.0"
    enabled: bool = True


class PluginInfo(BaseModel):
    """Complete plugin information"""
    metadata: PluginMetadata
    status: PluginStatus
    file_path: str
    loaded_at: Optional[datetime] = None
    last_reload: Optional[datetime] = None
    error_message: Optional[str] = None
    file_hash: str


class PluginHealth(BaseModel):
    """Plugin health check result"""
    plugin_id: str
    healthy: bool
    status: PluginStatus
    errors: List[str] = []
    warnings: List[str] = []
    last_check: datetime
    uptime_seconds: float


# ============================================================================
# PLUGIN BASE CLASS
# ============================================================================

class PluginBase:
    """
    Base class for all plugins

    All plugins must inherit from this class and implement required methods
    """

    def __init__(self):
        self.metadata: Optional[PluginMetadata] = None
        self._started_at: Optional[datetime] = None

    @classmethod
    def get_metadata(cls) -> PluginMetadata:
        """
        Return plugin metadata

        Override this method in your plugin
        """
        raise NotImplementedError("Plugin must implement get_metadata()")

    async def on_load(self):
        """
        Called when plugin is loaded

        Use this for initialization (connect to DB, load config, etc.)
        """
        pass

    async def on_unload(self):
        """
        Called before plugin is unloaded

        Use this for cleanup (close connections, save state, etc.)
        """
        pass

    async def on_start(self):
        """
        Called when plugin starts running

        Use this to start background tasks, listeners, etc.
        """
        self._started_at = datetime.now()

    async def on_stop(self):
        """
        Called when plugin stops running

        Use this to stop background tasks
        """
        pass

    async def health_check(self) -> PluginHealth:
        """
        Health check for plugin

        Override to add custom health checks
        """
        uptime = 0.0
        if self._started_at:
            uptime = (datetime.now() - self._started_at).total_seconds()

        return PluginHealth(
            plugin_id=self.metadata.id if self.metadata else "unknown",
            healthy=True,
            status=PluginStatus.RUNNING,
            last_check=datetime.now(),
            uptime_seconds=uptime
        )


# ============================================================================
# PLUGIN MANAGER
# ============================================================================

class PluginManager:
    """
    Dynamic Plugin Manager

    Features:
    - Hot-reload (no server restart needed)
    - Dependency management
    - Version control
    - Health monitoring
    - Error recovery
    """

    def __init__(self, plugin_dirs: List[str] = None):
        """
        Initialize plugin manager

        Args:
            plugin_dirs: List of directories to scan for plugins
        """
        self.plugin_dirs = plugin_dirs or [
            "src/plugins",
            "src/agents/custom",
            "src/integrations/custom"
        ]

        self.plugins: Dict[str, PluginInfo] = {}
        self.instances: Dict[str, PluginBase] = {}
        self.hooks: Dict[str, List[Callable]] = {}

        logger.info(f"Plugin Manager initialized. Scanning directories: {self.plugin_dirs}")

    # ========================================================================
    # PLUGIN LOADING
    # ========================================================================

    async def discover_plugins(self) -> List[str]:
        """
        Discover all plugins in plugin directories

        Returns list of plugin file paths
        """
        discovered = []

        for plugin_dir in self.plugin_dirs:
            path = Path(plugin_dir)
            if not path.exists():
                logger.warning(f"Plugin directory does not exist: {plugin_dir}")
                continue

            # Find all .py files
            for file_path in path.rglob("*.py"):
                if file_path.name.startswith("__"):
                    continue  # Skip __init__.py, __pycache__, etc.

                discovered.append(str(file_path))

        logger.info(f"Discovered {len(discovered)} potential plugins")
        return discovered

    async def load_plugin(self, file_path: str) -> Optional[str]:
        """
        Load plugin from file

        Args:
            file_path: Path to plugin file

        Returns:
            Plugin ID if successful, None if failed
        """
        try:
            # Calculate file hash (for change detection)
            file_hash = self._calculate_file_hash(file_path)

            # Load module dynamically
            module_name = Path(file_path).stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                logger.error(f"Failed to load spec for {file_path}")
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Find plugin class (must inherit from PluginBase)
            plugin_class = None
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, PluginBase) and obj is not PluginBase:
                    plugin_class = obj
                    break

            if not plugin_class:
                logger.warning(f"No PluginBase subclass found in {file_path}")
                return None

            # Get metadata
            metadata = plugin_class.get_metadata()

            # Check if already loaded
            if metadata.id in self.plugins:
                logger.warning(f"Plugin {metadata.id} already loaded. Use reload instead.")
                return None

            # Create plugin info
            plugin_info = PluginInfo(
                metadata=metadata,
                status=PluginStatus.LOADING,
                file_path=file_path,
                file_hash=file_hash
            )

            # Check dependencies
            if not await self._check_dependencies(metadata.dependencies):
                plugin_info.status = PluginStatus.ERROR
                plugin_info.error_message = "Missing dependencies"
                self.plugins[metadata.id] = plugin_info
                return None

            # Instantiate plugin
            instance = plugin_class()
            instance.metadata = metadata

            # Call on_load hook
            await instance.on_load()

            # Store
            self.plugins[metadata.id] = plugin_info
            self.instances[metadata.id] = instance

            plugin_info.status = PluginStatus.LOADED
            plugin_info.loaded_at = datetime.now()

            logger.info(
                f"✅ Plugin loaded: {metadata.name} v{metadata.version} "
                f"({metadata.plugin_type})"
            )

            # Emit event
            await self._emit_event("plugin_loaded", metadata.id)

            return metadata.id

        except Exception as e:
            logger.error(f"Failed to load plugin from {file_path}: {str(e)}")
            if file_path in [p.file_path for p in self.plugins.values()]:
                # Update existing plugin info
                for pid, pinfo in self.plugins.items():
                    if pinfo.file_path == file_path:
                        pinfo.status = PluginStatus.ERROR
                        pinfo.error_message = str(e)
            return None

    async def unload_plugin(self, plugin_id: str) -> bool:
        """
        Unload plugin

        Args:
            plugin_id: ID of plugin to unload

        Returns:
            True if successful
        """
        if plugin_id not in self.plugins:
            logger.warning(f"Plugin {plugin_id} not found")
            return False

        try:
            # Stop if running
            if self.plugins[plugin_id].status == PluginStatus.RUNNING:
                await self.stop_plugin(plugin_id)

            # Call on_unload hook
            instance = self.instances.get(plugin_id)
            if instance:
                await instance.on_unload()

            # Remove from memory
            del self.instances[plugin_id]
            del self.plugins[plugin_id]

            logger.info(f"Plugin unloaded: {plugin_id}")

            # Emit event
            await self._emit_event("plugin_unloaded", plugin_id)

            return True

        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_id}: {str(e)}")
            return False

    async def reload_plugin(self, plugin_id: str) -> bool:
        """
        Reload plugin (unload + load)

        Useful during development for hot-reloading changes

        Args:
            plugin_id: ID of plugin to reload

        Returns:
            True if successful
        """
        if plugin_id not in self.plugins:
            logger.warning(f"Plugin {plugin_id} not found")
            return False

        file_path = self.plugins[plugin_id].file_path

        # Unload
        success = await self.unload_plugin(plugin_id)
        if not success:
            return False

        # Reload
        new_id = await self.load_plugin(file_path)
        if not new_id:
            return False

        logger.info(f"Plugin reloaded: {plugin_id}")
        return True

    # ========================================================================
    # PLUGIN LIFECYCLE
    # ========================================================================

    async def start_plugin(self, plugin_id: str) -> bool:
        """
        Start running plugin

        Args:
            plugin_id: ID of plugin to start

        Returns:
            True if successful
        """
        if plugin_id not in self.plugins:
            logger.warning(f"Plugin {plugin_id} not found")
            return False

        if self.plugins[plugin_id].status == PluginStatus.RUNNING:
            logger.warning(f"Plugin {plugin_id} already running")
            return True

        try:
            instance = self.instances[plugin_id]
            await instance.on_start()

            self.plugins[plugin_id].status = PluginStatus.RUNNING

            logger.info(f"Plugin started: {plugin_id}")
            await self._emit_event("plugin_started", plugin_id)

            return True

        except Exception as e:
            logger.error(f"Failed to start plugin {plugin_id}: {str(e)}")
            self.plugins[plugin_id].status = PluginStatus.ERROR
            self.plugins[plugin_id].error_message = str(e)
            return False

    async def stop_plugin(self, plugin_id: str) -> bool:
        """
        Stop running plugin

        Args:
            plugin_id: ID of plugin to stop

        Returns:
            True if successful
        """
        if plugin_id not in self.plugins:
            logger.warning(f"Plugin {plugin_id} not found")
            return False

        if self.plugins[plugin_id].status != PluginStatus.RUNNING:
            logger.warning(f"Plugin {plugin_id} not running")
            return True

        try:
            instance = self.instances[plugin_id]
            await instance.on_stop()

            self.plugins[plugin_id].status = PluginStatus.LOADED

            logger.info(f"Plugin stopped: {plugin_id}")
            await self._emit_event("plugin_stopped", plugin_id)

            return True

        except Exception as e:
            logger.error(f"Failed to stop plugin {plugin_id}: {str(e)}")
            return False

    # ========================================================================
    # PLUGIN HEALTH & MONITORING
    # ========================================================================

    async def get_plugin_health(self, plugin_id: str) -> Optional[PluginHealth]:
        """
        Get plugin health status

        Args:
            plugin_id: ID of plugin

        Returns:
            PluginHealth or None if not found
        """
        if plugin_id not in self.instances:
            return None

        instance = self.instances[plugin_id]
        health = await instance.health_check()

        return health

    async def get_all_health(self) -> Dict[str, PluginHealth]:
        """
        Get health status of all plugins

        Returns:
            Dict of plugin_id -> PluginHealth
        """
        health_results = {}

        for plugin_id in self.instances.keys():
            health = await self.get_plugin_health(plugin_id)
            if health:
                health_results[plugin_id] = health

        return health_results

    # ========================================================================
    # PLUGIN QUERIES
    # ========================================================================

    def get_plugin(self, plugin_id: str) -> Optional[PluginInfo]:
        """Get plugin info"""
        return self.plugins.get(plugin_id)

    def get_all_plugins(self) -> List[PluginInfo]:
        """Get all plugins"""
        return list(self.plugins.values())

    def get_plugins_by_type(self, plugin_type: PluginType) -> List[PluginInfo]:
        """Get plugins of specific type"""
        return [
            p for p in self.plugins.values()
            if p.metadata.plugin_type == plugin_type
        ]

    def get_plugin_instance(self, plugin_id: str) -> Optional[PluginBase]:
        """Get plugin instance"""
        return self.instances.get(plugin_id)

    # ========================================================================
    # AUTO-RELOAD ON FILE CHANGE
    # ========================================================================

    async def watch_for_changes(self):
        """
        Watch plugin files for changes and auto-reload

        Useful for development
        """
        import asyncio

        while True:
            for plugin_id, plugin_info in list(self.plugins.items()):
                current_hash = self._calculate_file_hash(plugin_info.file_path)

                if current_hash != plugin_info.file_hash:
                    logger.info(f"File changed detected for {plugin_id}, reloading...")
                    await self.reload_plugin(plugin_id)

            await asyncio.sleep(2)  # Check every 2 seconds

    # ========================================================================
    # HOOKS & EVENTS
    # ========================================================================

    def register_hook(self, event: str, callback: Callable):
        """
        Register hook for plugin events

        Events:
        - plugin_loaded
        - plugin_unloaded
        - plugin_started
        - plugin_stopped
        - plugin_error
        """
        if event not in self.hooks:
            self.hooks[event] = []

        self.hooks[event].append(callback)

    async def _emit_event(self, event: str, plugin_id: str):
        """Emit event to all registered hooks"""
        if event in self.hooks:
            for callback in self.hooks[event]:
                try:
                    await callback(plugin_id)
                except Exception as e:
                    logger.error(f"Error in hook {callback.__name__}: {str(e)}")

    # ========================================================================
    # UTILITIES
    # ========================================================================

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    async def _check_dependencies(self, dependencies: List[str]) -> bool:
        """Check if all dependencies are loaded"""
        for dep_id in dependencies:
            if dep_id not in self.plugins:
                logger.error(f"Missing dependency: {dep_id}")
                return False

            if self.plugins[dep_id].status not in [PluginStatus.LOADED, PluginStatus.RUNNING]:
                logger.error(f"Dependency {dep_id} not loaded")
                return False

        return True


# ============================================================================
# GLOBAL PLUGIN MANAGER INSTANCE
# ============================================================================

# Singleton instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get global plugin manager instance"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'PluginManager',
    'PluginBase',
    'PluginType',
    'PluginStatus',
    'PluginMetadata',
    'PluginInfo',
    'PluginHealth',
    'get_plugin_manager'
]
