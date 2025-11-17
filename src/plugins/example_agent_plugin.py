"""
Example Agent Plugin
Demonstrates how to create a plugin for the Plugin Manager
"""
from src.core.plugin_manager import PluginBase, PluginMetadata, PluginType, PluginHealth, PluginStatus
from datetime import datetime
from loguru import logger


class WeatherAgentPlugin(PluginBase):
    """
    Example: Weather Information Agent

    Demonstrates:
    - Plugin metadata
    - Lifecycle hooks (on_load, on_start, etc.)
    - Health checks
    - Background tasks
    """

    @classmethod
    def get_metadata(cls) -> PluginMetadata:
        """Plugin metadata"""
        return PluginMetadata(
            id="weather_agent",
            name="Weather Information Agent",
            version="1.0.0",
            description="Provides weather information for locations worldwide",
            author="Mindframe Team",
            plugin_type=PluginType.AGENT,
            dependencies=[],  # No dependencies
            enabled=True
        )

    def __init__(self):
        super().__init__()
        self.api_key = None
        self.cache = {}
        self.requests_handled = 0

    async def on_load(self):
        """
        Called when plugin is loaded

        Initialize resources here
        """
        logger.info("Weather Agent: Initializing...")

        # Load configuration
        self.api_key = "demo_api_key_12345"  # In production: from config

        # Initialize cache
        self.cache = {}

        logger.info("Weather Agent: Initialized successfully")

    async def on_start(self):
        """
        Called when plugin starts running

        Start background tasks here
        """
        await super().on_start()
        logger.info("Weather Agent: Started")

        # In production: Start background cache refresh task

    async def on_stop(self):
        """
        Called when plugin stops

        Clean up background tasks here
        """
        logger.info("Weather Agent: Stopping...")

        # In production: Stop background tasks

        logger.info("Weather Agent: Stopped")

    async def on_unload(self):
        """
        Called before plugin is unloaded

        Final cleanup here
        """
        logger.info("Weather Agent: Unloading...")

        # Clear cache
        self.cache.clear()

        logger.info("Weather Agent: Unloaded")

    async def health_check(self) -> PluginHealth:
        """
        Health check

        Check if agent is functioning properly
        """
        errors = []
        warnings = []

        # Check API key
        if not self.api_key:
            errors.append("API key not configured")

        # Check cache size
        if len(self.cache) > 1000:
            warnings.append("Cache size large (>1000 entries)")

        # Check request count
        if self.requests_handled == 0:
            warnings.append("No requests handled yet")

        uptime = 0.0
        if self._started_at:
            uptime = (datetime.now() - self._started_at).total_seconds()

        healthy = len(errors) == 0

        return PluginHealth(
            plugin_id=self.metadata.id,
            healthy=healthy,
            status=PluginStatus.RUNNING if healthy else PluginStatus.ERROR,
            errors=errors,
            warnings=warnings,
            last_check=datetime.now(),
            uptime_seconds=uptime
        )

    # ========================================================================
    # AGENT FUNCTIONALITY
    # ========================================================================

    async def get_weather(self, location: str) -> dict:
        """
        Get weather for location

        This is the actual agent functionality
        """
        self.requests_handled += 1

        # Check cache
        if location in self.cache:
            logger.info(f"Weather cache hit for {location}")
            return self.cache[location]

        # In production: Call actual weather API
        # For demo, return mock data
        weather_data = {
            "location": location,
            "temperature": 22,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": 10,
            "timestamp": datetime.now().isoformat()
        }

        # Cache result
        self.cache[location] = weather_data

        logger.info(f"Weather fetched for {location}: {weather_data['temperature']}°C, {weather_data['condition']}")

        return weather_data

    async def get_forecast(self, location: str, days: int = 5) -> list:
        """Get weather forecast"""
        # In production: Call forecast API
        forecast = []
        for day in range(days):
            forecast.append({
                "day": day + 1,
                "temperature_high": 25 + day,
                "temperature_low": 15 + day,
                "condition": "Partly Cloudy",
                "precipitation_chance": 20
            })

        return forecast
