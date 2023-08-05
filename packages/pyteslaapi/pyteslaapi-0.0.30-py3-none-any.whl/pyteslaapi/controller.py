import time
import logging
from multiprocessing import RLock
from pyteslaapi.connection import Connection
from pyteslaapi.BatterySensor import Battery, Range
from pyteslaapi.Lock import Lock, ChargerLock
from pyteslaapi.Climate import Climate, TempSensor
from pyteslaapi.BinarySensor import ParkingSensor, ChargerConnectionSensor
from pyteslaapi.Charger import ChargerSwitch, RangeSwitch
from pyteslaapi.GPS import GPS, Odometer
from pyteslaapi.vehicle import VehicleDevice
from pyteslaapi.DriveSensor import DriveSensor

_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, email, password, update_interval, wake=True, wake_interval=10800, drive_interval=60):
        self.__connection = Connection(email, password)
        self.__vehicle_devices = []
        self.__vehicles = []
        self.__should_wake = wake
        self.wake_interval = wake_interval
        self.drive_interval = drive_interval
        self.update_interval = update_interval
        self.__update = {}
        self.__climate = {}
        self.__charging = {}
        self.__state = {}
        self.__driving = {}
        self.__gui = {}
        self.__last_update_time = {}
        self.__lock = RLock()
        cars = self.__connection.get('vehicles')['response']
        for car in cars:
            car_id = car['id']
            self.__vehicles.append(VehicleDevice(car, self))
            self.__climate[car_id] = False
            self.__charging[car_id] = False
            self.__state[car_id] = False
            self.__driving[car_id] = False
            self.__gui[car_id] = False
            self.__last_update_time[car_id] = 0
            self.__update[car_id] = True
            self.update(car_id, True)
            self.__vehicle_devices.append(Climate(car, self))
            self.__vehicle_devices.append(Battery(car, self))
            self.__vehicle_devices.append(Range(car, self))
            self.__vehicle_devices.append(TempSensor(car, self))
            self.__vehicle_devices.append(Lock(car, self))
            self.__vehicle_devices.append(ChargerLock(car, self))
            self.__vehicle_devices.append(ChargerConnectionSensor(car, self))
            self.__vehicle_devices.append(ChargerSwitch(car, self))
            self.__vehicle_devices.append(RangeSwitch(car, self))
            self.__vehicle_devices.append(ParkingSensor(car, self))
            self.__vehicle_devices.append(GPS(car, self))
            self.__vehicle_devices.append(Odometer(car, self))
            self.__vehicle_devices.append(DriveSensor(car, self))

    def post(self, vehicle_id, command, data={}):
        return self.__connection.post('vehicles/%i/%s' % (vehicle_id, command), data)

    def get(self, vehicle_id, command):
        return self.__connection.get('vehicles/%i/%s' % (vehicle_id, command))

    def data_request(self, vehicle_id, name):
        return self.get(vehicle_id, 'data_request/%s' % name)['response']

    def command(self, vehicle_id, name, data={}):
        return self.post(vehicle_id, 'command/%s' % name, data)

    def list_vehicle_devices(self):
        return self.__vehicle_devices

    def list_vehicles(self):
        return self.__vehicles

    def wake_up(self, vehicle_id):
        self.post(vehicle_id, 'wake_up')

    def __check_driving_interval(self, car_id):
        return (time.time() - self.__last_update_time[car_id] > self.drive_interval)

    def __check_update_interval(self, car_id):
        return (time.time() - self.__last_update_time[car_id] > self.update_interval)

    def __check_wake_interval(self, car_id, first_update):
        if self.__should_wake is False and first_update is False:
            return (time.time() - self.__last_update_time[car_id] > self.wake_interval)
        return (time.time() - self.__last_update_time[car_id] > self.update_interval)

    def update(self, car_id, first_update=False):
        with self.__lock:
            self.__vehicles= []
            should_update = False
            cars = self.__connection.get('vehicles')['response']
            for car in cars:
                # self.__vehicles.append(VehicleDevice(car, self))
                if car['id'] == car_id:
                    if first_update:
                        should_update = True
                    elif (car['state'] == 'online' and
                        self.__driving[car_id] and
                        self.__driving[car_id]['shift_state'] and
                        self.__driving[car_id]['shift_state'] != "P"):
                        should_update = self.__check_driving_interval(car_id)
                    elif car['state'] == 'online':
                        should_update = self.__check_update_interval(car_id)
                    else:
                        should_update = self.__check_wake_interval(car_id, first_update)

            if (self.__update[car_id] and should_update):
                self.wake_up(car_id)
                _LOGGER.debug("Requesting tesla state data")
                data = self.get(car_id, 'data')
                _LOGGER.debug(data)
                if data and data['response']:
                    _LOGGER.debug("Received data from tesla")
                    self.__climate[car_id] = data['response']['climate_state']
                    self.__charging[car_id] = data['response']['charge_state']
                    self.__state[car_id] = data['response']['vehicle_state']
                    self.__driving[car_id] = data['response']['drive_state']
                    self.__gui[car_id] = data['response']['gui_settings']
                    self.__last_update_time[car_id] = time.time()
                    return True
            _LOGGER.debug("Update from tesla failed")
            return False

    def get_climate_params(self, car_id):
        return self.__climate[car_id]

    def get_charging_params(self, car_id):
        return self.__charging[car_id]

    def get_state_params(self, car_id):
        return self.__state[car_id]

    def get_drive_params(self, car_id):
        return self.__driving[car_id]

    def get_gui_params(self, car_id):
        return self.__gui[car_id]

    def get_updates(self, car_id=None):
        if car_id is not None:
            return self.__update[car_id]
        else:
            return self.__update

    def set_updates(self, car_id, value):
        self.__update[car_id] = value
