from rpi_automator.modules.BaseModule import BaseModule
from rpi_automator.dto.ModuleResult import ModuleResult
from rpi_automator.dto.RelaySwitchData import RelaySwitchData

import logging
from datetime import datetime
from datetime import timedelta
from RPi import GPIO

logger = logging.getLogger()


class RelaySwitch(BaseModule):
    """
        Module interacting with a connected relay board controlling power to a connected device.
        config:
            type: modules/RelaySwitch
            name: <set>,
            cron: <string, cron syntax>,
            duration: <int, duration in seconds, triggers the value_toggle value at this time>
            value: <initial value to send to relay>
            value_toggle: <toggle value to send to relay to send after <duration> seconds>
            enabled: <boolean, enable or disable this module>
    """

    def __init__(self, config):
        BaseModule.__init__(self, config)
        self.pin = config['pin']
        self.value_initial = self.current_value = config['value']
        self.value_toggle = config['value_toggle']
        self.send(self.current_value)

    def run(self, module_result):

        self.send(self.current_value)

        logger.debug("RelaySwitch(self.name) is now %s", str(self.current_value))

        previous_value = self.current_value
        self.current_value = not self.current_value

        duration = int(self.config['duration']) # seconds
        result = ModuleResult(self, RelaySwitchData(duration))

        # if we're set to change values in 'duration' seconds
        if self.current_value != self.value_initial and 'duration' in self.config:
            run_at = datetime.now() + timedelta(seconds=duration)

            logger.info("Will toggle at %s", run_at)

            self.schedule_run(run_at, name=self.name + str(self.current_value), module_result=result)

        # if this run is the result of a previous run and we've reached the toggle state
        if module_result and module_result.module == self and previous_value == self.value_toggle:
            module_result.data.completion_time = datetime.now().isoformat()
            return module_result

        return result

    def send(self, value):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, value)


