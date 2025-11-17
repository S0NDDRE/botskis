"""
Dependency Injection Container
Loose coupling and easy testing
"""
from typing import Dict, Type, Any, Optional, Callable
from enum import Enum
from loguru import logger


# ============================================================================
# LIFETIME SCOPES
# ============================================================================

class Lifetime(str, Enum):
    """Service lifetime scopes"""
    SINGLETON = "singleton"  # One instance for entire app
    TRANSIENT = "transient"  # New instance every time
    SCOPED = "scoped"  # One instance per request/scope


# ============================================================================
# DEPENDENCY INJECTION CONTAINER
# ============================================================================

class DIContainer:
    """
    Dependency Injection Container

    Benefits:
    - Loose coupling between components
    - Easy testing (swap real services with mocks)
    - Centralized configuration
    - Lifecycle management

    Example usage:
    ```python
    # Register services
    container = DIContainer()
    container.register(IPaymentService, StripePaymentService, Lifetime.SINGLETON)
    container.register(IEmailService, SendGridEmailService, Lifetime.TRANSIENT)

    # Resolve services
    payment = container.resolve(IPaymentService)
    await payment.charge(customer_id=123, amount=99.00)

    # Testing: swap with mock
    container.register(IPaymentService, MockPaymentService, Lifetime.SINGLETON)
    payment = container.resolve(IPaymentService)  # Returns mock
    ```
    """

    def __init__(self):
        self._services: Dict[Type, dict] = {}
        self._singletons: Dict[Type, Any] = {}
        self._scoped_instances: Dict[str, Dict[Type, Any]] = {}
        self._current_scope: Optional[str] = None

    # ========================================================================
    # REGISTRATION
    # ========================================================================

    def register(
        self,
        interface: Type,
        implementation: Type,
        lifetime: Lifetime = Lifetime.TRANSIENT
    ):
        """
        Register service

        Args:
            interface: Interface (abstract class or protocol)
            implementation: Concrete implementation
            lifetime: Service lifetime (singleton/transient/scoped)

        Example:
        ```python
        container.register(IPaymentService, StripePaymentService, Lifetime.SINGLETON)
        ```
        """
        self._services[interface] = {
            "implementation": implementation,
            "lifetime": lifetime
        }

        logger.debug(
            f"Registered {interface.__name__} -> {implementation.__name__} "
            f"({lifetime})"
        )

    def register_instance(self, interface: Type, instance: Any):
        """
        Register existing instance as singleton

        Args:
            interface: Interface type
            instance: Pre-created instance

        Example:
        ```python
        stripe_client = StripeClient(api_key="...")
        container.register_instance(IPaymentService, stripe_client)
        ```
        """
        self._singletons[interface] = instance
        self._services[interface] = {
            "implementation": type(instance),
            "lifetime": Lifetime.SINGLETON
        }

        logger.debug(f"Registered instance {interface.__name__}")

    def register_factory(
        self,
        interface: Type,
        factory: Callable,
        lifetime: Lifetime = Lifetime.TRANSIENT
    ):
        """
        Register factory function

        Args:
            interface: Interface type
            factory: Function that creates instance
            lifetime: Service lifetime

        Example:
        ```python
        def create_payment_service():
            api_key = get_config("stripe_api_key")
            return StripePaymentService(api_key)

        container.register_factory(IPaymentService, create_payment_service)
        ```
        """
        self._services[interface] = {
            "factory": factory,
            "lifetime": lifetime
        }

        logger.debug(f"Registered factory {interface.__name__} ({lifetime})")

    # ========================================================================
    # RESOLUTION
    # ========================================================================

    def resolve(self, interface: Type) -> Any:
        """
        Resolve service instance

        Args:
            interface: Interface type to resolve

        Returns:
            Service instance

        Example:
        ```python
        payment_service = container.resolve(IPaymentService)
        await payment_service.charge(...)
        ```
        """
        if interface not in self._services:
            raise ValueError(
                f"Service {interface.__name__} not registered. "
                f"Did you forget to call container.register()?"
            )

        service_config = self._services[interface]
        lifetime = service_config["lifetime"]

        # Singleton: return cached instance
        if lifetime == Lifetime.SINGLETON:
            if interface in self._singletons:
                return self._singletons[interface]

            instance = self._create_instance(service_config)
            self._singletons[interface] = instance
            return instance

        # Scoped: return scoped instance
        elif lifetime == Lifetime.SCOPED:
            if not self._current_scope:
                raise RuntimeError(
                    "Cannot resolve scoped service outside of scope. "
                    "Use 'with container.create_scope():'"
                )

            scope_cache = self._scoped_instances[self._current_scope]
            if interface in scope_cache:
                return scope_cache[interface]

            instance = self._create_instance(service_config)
            scope_cache[interface] = instance
            return instance

        # Transient: create new instance every time
        else:
            return self._create_instance(service_config)

    def _create_instance(self, service_config: dict) -> Any:
        """Create service instance"""
        if "factory" in service_config:
            # Use factory function
            factory = service_config["factory"]
            return factory()
        else:
            # Use constructor
            implementation = service_config["implementation"]

            # Check if implementation has dependencies
            # (constructor parameters that are registered services)
            try:
                import inspect
                sig = inspect.signature(implementation.__init__)
                params = list(sig.parameters.values())[1:]  # Skip 'self'

                # Resolve dependencies
                dependencies = []
                for param in params:
                    if param.annotation != inspect.Parameter.empty:
                        if param.annotation in self._services:
                            dep = self.resolve(param.annotation)
                            dependencies.append(dep)

                # Create instance with dependencies
                if dependencies:
                    return implementation(*dependencies)
                else:
                    return implementation()

            except Exception as e:
                logger.warning(f"Auto-wiring failed for {implementation.__name__}: {e}")
                # Fallback: create without dependencies
                return implementation()

    # ========================================================================
    # SCOPED RESOLUTION
    # ========================================================================

    class Scope:
        """Context manager for scoped resolution"""

        def __init__(self, container: 'DIContainer', scope_id: str):
            self.container = container
            self.scope_id = scope_id

        def __enter__(self):
            self.container._current_scope = self.scope_id
            self.container._scoped_instances[self.scope_id] = {}
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Cleanup scoped instances
            del self.container._scoped_instances[self.scope_id]
            self.container._current_scope = None

    def create_scope(self, scope_id: Optional[str] = None) -> Scope:
        """
        Create resolution scope

        Scoped services live for the duration of the scope

        Example:
        ```python
        # Each request gets its own scope
        with container.create_scope(f"request_{request_id}"):
            db_session = container.resolve(IDatabaseSession)
            # Use db_session...
            # db_session automatically cleaned up when scope exits
        ```
        """
        import uuid
        scope_id = scope_id or str(uuid.uuid4())
        return self.Scope(self, scope_id)

    # ========================================================================
    # UTILITIES
    # ========================================================================

    def is_registered(self, interface: Type) -> bool:
        """Check if service is registered"""
        return interface in self._services

    def get_registered_services(self) -> list:
        """Get list of registered service interfaces"""
        return list(self._services.keys())

    def clear(self):
        """Clear all registrations (useful for testing)"""
        self._services.clear()
        self._singletons.clear()
        self._scoped_instances.clear()
        logger.debug("Container cleared")


# ============================================================================
# GLOBAL CONTAINER
# ============================================================================

# Singleton container instance
_global_container: Optional[DIContainer] = None


def get_container() -> DIContainer:
    """Get global DI container"""
    global _global_container
    if _global_container is None:
        _global_container = DIContainer()
    return _global_container


# ============================================================================
# SERVICE INTERFACES (Examples)
# ============================================================================

class IPaymentService:
    """Payment service interface"""
    async def charge(self, customer_id: int, amount: float) -> dict:
        raise NotImplementedError

    async def refund(self, charge_id: str, amount: float) -> dict:
        raise NotImplementedError


class IEmailService:
    """Email service interface"""
    async def send(self, to: str, subject: str, body: str) -> bool:
        raise NotImplementedError


class IDatabaseSession:
    """Database session interface"""
    async def query(self, sql: str):
        raise NotImplementedError

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'DIContainer',
    'Lifetime',
    'get_container',
    'IPaymentService',
    'IEmailService',
    'IDatabaseSession'
]
