"""ADT Pulse sensor, can be a door, window or motion sensor."""

class ADTPulseSensor():
    """Class to represent a ADT Pulse sensor."""

    def __init__(self, json_data):
        """Set up ADT Pulse sensor."""
        self._name = json_data["name"]
        self._id = json_data["id"]
        self._zone = json_data["zone"]
        self._dev_index = json_data["devIndex"]
        self._tags = json_data["tags"].split(',')
        state = json_data["state"]
        self._bypassed = state["bypassed"]
        self._is_tripped = state["isTripped"]
        self._status = state["statusTxt"]

    @property
    def status(self):
        """Gets sensor status."""
        return self._get_status()

    def _get_status(self):
        """Indirect accessor the 'status' property."""
        return self._status

    @property
    def name(self):
        """Gets sensor name."""
        return self._get_name()

    def _get_name(self):
        """Indirect accessor the 'name' property."""
        return self._name

    @property
    def id(self):
        """Gets sensor id."""
        return self._get_id()

    def _get_id(self):
        """Indirect accessor the 'id' property."""
        return self._id

    @property
    def zone(self):
        """Gets sensor zone."""
        return self._get_id()

    def _get_zone(self):
        """Indirect accessor the 'zone' property."""
        return self._zone

    @property
    def tags(self):
        """Gets sensor tags."""
        return self._get_tags()

    def _get_tags(self):
        """Indirect accessor the 'tags' property."""
        return self._tags

    @property
    def is_tripped(self):
        """Is the sensor tripped."""
        return self._get_is_tripped()

    def _get_is_tripped(self):
        """Indirect accessor the 'is_tripped' property."""
        return self._is_tripped

    @property
    def bypassed(self):
        """Is the sensor bypassed."""
        return self._get_bypassed()

    def _get_bypassed(self):
        """Indirect accessor the 'bypassed' property."""
        return self._bypassed
