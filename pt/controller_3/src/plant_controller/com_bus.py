"""Communication bus abstractions for hardware peripherals.

This module provides thread-safe bus wrappers for I2C (via Blinka/adafruit)
and MODBUS RTU (via pymodbus). Sensors and pumps declare which bus they use
by inheriting from ``I2CInterface`` or ``MODBUSInterface``.

Bus type constants:
    _I2C: Canonical string identifier for the I2C bus ("i2c").
    _MODBUS: Canonical string identifier for the MODBUS bus ("MODBUS").
"""

import logging
logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod
import threading

import adafruit_tca9548a
from pymodbus.client import ModbusSerialClient

import anyio
import board

_I2C = "i2c"
_MODBUS = "MODBUS"


class Bus(ABC):
    """Abstract base class for communication buses.

    Provides thread-safety primitives for serial bus access. All bus
    operations that touch hardware should go through ``run_sync`` (async)
    or ``run_sync_blocking`` (sync) to ensure mutual exclusion.
    """

    def __init__(self):
        self._serial_lock = threading.Lock()
        pass

    async def run_sync(self, fn):
        """Run a synchronous function in a worker thread, holding the bus lock.

        Args:
            fn: Zero-argument callable to execute under the lock.

        Returns:
            The return value of fn().
        """
        def _locked():
            with self._serial_lock:
                return fn()
        return await anyio.to_thread.run_sync(_locked)

    def run_sync_blocking(self, fn):
        """Run a synchronous function on the current thread, holding the bus lock.

        Args:
            fn: Zero-argument callable to execute under the lock.

        Returns:
            The return value of fn().
        """
        with self._serial_lock:
            return fn()


class BlinkaI2CBus(Bus):
    """I2C bus implementation using Adafruit Blinka.

    Wraps the board's I2C interface and manages TCA9548A multiplexers
    for addressing multiple devices on the same bus.

    Attributes:
        wrapped_bus: The underlying board.I2C() instance.
        multiplexers: Dict mapping addresses to TCA9548A instances.
    """

    def __init__(self):
        self.wrapped_bus = board.I2C()
        self.multiplexers = {}
        super().__init__()
        logger.info("Blinka I2C bus initialized")

    def ensure_multiplexer(self, address: int) -> adafruit_tca9548a.TCA9548A:
        """Get or create a TCA9548A multiplexer at the given I2C address.

        Args:
            address: I2C address of the multiplexer (e.g. 0x70).

        Returns:
            The TCA9548A instance for that address.
        """
        if address not in self.multiplexers:
            self.multiplexers[address] = adafruit_tca9548a.TCA9548A(self.wrapped_bus, address=address)
            logger.info(f"Initialized new I2C multiplexer at address {address}")
        return self.multiplexers[address]


class MODBUS(Bus):
    """MODBUS RTU bus implementation using pymodbus.

    Wraps a pymodbus ModbusSerialClient and provides both synchronous and
    async (thread-offloaded) access patterns. Method calls are proxied to
    the underlying client with automatic locking.

    Attribute access patterns:
        - ``bus.write_coil(...)`` - synchronous, locked call to the client.
        - ``await bus.snagged_write_coil(...)`` - async, runs in a worker
          thread with the bus lock held. Prefix any client method with
          ``snagged_`` to get the async variant.

    Attributes:
        client: The underlying pymodbus ModbusSerialClient.
    """

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        baudrate: int = 9600,
        bytesize: int = 8,
        parity: str = 'N',
        stopbits: int = 1,
        timeout: float = 1.0
    ):
        """Initialize the MODBUS serial client.

        Args:
            port: Serial port path (default: /dev/ttyUSB0).
            baudrate: Communication speed (default: 9600).
            bytesize: Data bits per frame (default: 8).
            parity: Parity setting: 'N', 'E', or 'O' (default: 'N').
            stopbits: Number of stop bits (default: 1).
            timeout: Read timeout in seconds (default: 1.0).
        """
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )
        super().__init__()

    def __getattr__(self, name):
        """Proxy attribute access to the underlying pymodbus client.

        If the attribute name starts with 'snagged_', returns an async
        wrapper that runs the client method in a worker thread with the
        bus lock. Otherwise returns a synchronous locked wrapper.
        """
        split_name = name.split("_", 1)
        in_new_thread = False
        try:
            if split_name[0] == "snagged":
                name = split_name[1]
                in_new_thread = True
            attr = getattr(self.client, name)
            if callable(attr):
                if in_new_thread:
                    async def _locked_client_func_in_new_thread(*args, **kwargs):
                        return await self.run_sync(
                            lambda: attr(*args, **kwargs)
                        )
                    return _locked_client_func_in_new_thread
                else:
                    def _locked_client_func(*args, **kwargs):
                        return self.run_sync_blocking(
                            lambda: attr(*args, **kwargs)
                        )
                    return _locked_client_func
            else:
                return attr
        except AttributeError:
            raise AttributeError(f"Neither this '{type(self).__name__}' object nor the wrapped '{type(self.client).__name__}' object has any attribute '{name}'")

    async def connect(self):
        """Open the serial connection to the MODBUS network."""
        try:
            self.client.connect()
            logger.info("Connected to MODBUS client")
        except Exception as e:
            logger.error(f"Failed to connect to MODBUS client: {e}")
            raise e

    def close(self):
        """Close the serial connection."""
        with self._serial_lock:
            self.client.close()
        logger.info("Closed MODBUS client connection")


class BusInterface(ABC):
    """Mixin declaring which bus type a peripheral uses.

    Sensors and pumps must inherit from one of the concrete subclasses
    (I2CInterface or MODBUSInterface) so the dynamic loader can
    automatically select the correct bus instance.
    """

    @staticmethod
    @abstractmethod
    def bus_type() -> str:
        """Return the canonical bus type string for this peripheral.

        Returns:
            The bus type identifier (matches keys in the busses dict).
        """
        pass


class I2CInterface(BusInterface):
    """Mixin indicating a peripheral communicates via I2C."""

    @staticmethod
    def bus_type() -> str:
        """Return the I2C bus type identifier.

        Returns:
            The string 'i2c'.
        """
        return _I2C


class MODBUSInterface(BusInterface):
    """Mixin indicating a peripheral communicates via MODBUS RTU."""

    @staticmethod
    def bus_type() -> str:
        """Return the MODBUS bus type identifier.

        Returns:
            The string 'MODBUS'.
        """
        return _MODBUS


async def busses():
    """Initialize and connect all communication buses.

    Returns:
        Dict mapping bus type strings to initialized Bus instances.
    """
    i2c_bus = BlinkaI2CBus()
    modbus = MODBUS()
    await modbus.connect()
    return {
        _I2C: i2c_bus,
        _MODBUS: modbus
    }