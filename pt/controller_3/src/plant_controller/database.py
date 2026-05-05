"""Database access layer for the plant controller.

Wraps InfluxDB client functionality, providing methods to write sensor
measurements and watering events, and to query historical data.
"""

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

from influxdb_client_3 import InfluxDBClient3

from .datapoint import Datapoint


class DatabaseClient(InfluxDBClient3):
    """Extended InfluxDB client with convenience methods for plant data.

    Inherits from InfluxDBClient3 and adds domain-specific read/write
    methods that work with Datapoint objects.
    """

    def write_measurements(
        self,
        physical_unit: str,
        data: Datapoint | list[Datapoint]
    ):
        """Write one or more datapoints to the database.

        Args:
            physical_unit: Name of the unit (used for table naming).
            data: A single Datapoint or list of Datapoints to persist.
        """
        if isinstance(data, Datapoint):
            self.write(data.to_point(physical_unit))
        else:
            self.write([dp.to_point(physical_unit) for dp in data])

    def read_measurements(
        self,
        physical_unit: str,
        parameter: str,
        limit: int | None = None,
        since_timestamp: datetime | None = None
    ):
        """Query historical measurements from the database.

        Args:
            physical_unit: Name of the unit to query.
            parameter: Parameter name (e.g. 'temperature', 'watering').
            limit: Maximum number of records to return (most recent first).
            since_timestamp: Only return records after this time.

        Returns:
            A pandas DataFrame of matching records, ordered by time descending.
        """
        query = (
            f'SELECT * FROM ' + Datapoint.format_for_table_name(
                physical_unit,
                parameter
            )
            + (f" WHERE time > '{since_timestamp.isoformat()}'" if since_timestamp else '')
            + f' ORDER BY time DESC'
            + (f' LIMIT {limit}' if limit else '')
        )
        _logger.debug(f'Executing query: {query}')
        return self.query(
            query
        ).to_pandas()


class Database:
    """Database connection configuration and client factory.

    Attributes:
        token: Authentication token for InfluxDB.
        name: Database (bucket) name.
        host: InfluxDB host URL.
    """

    def __init__(
        self,
        token: str,
        name: str = 'plant-controller',
        host: str = 'http://127.0.0.1:8181',
    ):
        self.token=token
        self.name=name
        self.host=host

    def exists(self) -> bool:
        """Check if the database exists (currently always returns True)."""
        return True

    def initialize(self):
        """Initialize the database (no-op, reserved for future use)."""
        pass

    def spawn_client(self) -> DatabaseClient:
        """Create and return a new DatabaseClient connected to this database."""
        return DatabaseClient(
            host=self.host,
            database=self.name,
            token=self.token
        )
