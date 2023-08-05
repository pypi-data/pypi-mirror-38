"""ADT PUlse alarm device."""

from adtpulsepy.devices.sensor import ADTPulseSensor

class ADTPulseAlarm():
    """Class to represent the ADT Pulse alarm as a device."""

    def __init__(self, json_data):
        """Set up ADT Pulse alarm device."""
        self._sensors = []
        self._name = "ADT Pulse Alarm"
        state = json_data["summary"]["state"]
        self._arm_type = state["armType"]
        self._status_text = state["sensorStatusTxt"]
        self._sensors_motion = state["numMotion"]
        self._sensors_open = state["numOpen"]
        self._sensors_trouble = state["numTrouble"]
        self._sensors_status = state["sensorStatusTxt"]
        for sensor in json_data["sensor"]["items"]:
            self._add_sensor(sensor)

    def _add_sensor(self, sensor_json):
        """Adds a sensor to the alarm device."""
        self._sensors.append(ADTPulseSensor(sensor_json))

    @property
    def name(self):
        """Gets or sets the alarm name."""
        return self._get_name()

    @name.setter
    def name(self, name):
        return self._set_name(name)

    def _get_name(self):
        """Indirect accessor the 'name' property."""
        return self._name

    def _set_name(self, name):
        """Indirect setter to set the 'name' property."""
        self._name = name

    @property
    def sensors(self):
        """Gets all the ADT Pulse sensors."""
        return self._get_sensors()

    def _get_sensors(self):
        """Indirect accessor to return 'sensors' property."""
        return self._sensors

    @property
    def arm_type(self):
        """Gets the arm type of the alarm."""
        return self._get_arm_type()

    def _get_arm_type(self):
        """Indirect accessor the 'arm_type' property."""
        return self._arm_type

    @property
    def sensors_motion(self):
        """Gets count of sensors that detect motion."""
        return self._get_sensors_motion()

    def _get_sensors_motion(self):
        """Indirect accessor the 'sensors_motion' property."""
        return self._sensors_motion

    @property
    def sensors_open(self):
        """Gets count of sensors that have an open state."""
        return self._get_sensors_open()

    def _get_sensors_open(self):
        """Indirect accessor the 'sensors_open' property."""
        return self._sensors_open

    @property
    def sensors_trouble(self):
        """Gets count of sensors that detect trouble."""
        return self._get_sensors_trouble()

    def _get_sensors_trouble(self):
        """Indirect accessor the 'sensors_trouble' property."""
        return self._sensors_trouble

    @property
    def status(self):
        """Gets alarm status."""
        return self._get_status()

    def _get_status(self):
        """Indirect accessor the 'status_text' property."""
        return self._status_text
