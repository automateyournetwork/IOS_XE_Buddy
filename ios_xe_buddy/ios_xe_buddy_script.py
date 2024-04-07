import os
import json
import logging
from pyats import aetest
from pyats.log.utils import banner

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
# ----------------
# Connected to devices
# ----------------
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect()
# ----------------
# Mark the loop for Learn Interfaces
# ----------------
    @aetest.subsection
    def loop_mark(self, testbed):
        aetest.loop.mark(Show_IP_Route_Langchain, device_name=testbed.devices)

# ----------------
# Test Case #1
# ----------------
class Show_IP_Route_Langchain(aetest.Testcase):
    """pyATS Get and Save Show IP Route"""

    @aetest.test
    def setup(self, testbed, device_name):
        """ Testcase Setup section """
        # Set current device in loop as self.device
        self.device = testbed.devices[device_name]

        # Read the configuration from the file
        with open('command.txt', 'r') as file:
            self.command = file.read()

    @aetest.test
    def capture_parse_command(self):
        if "show run" in self.command:
            self.parsed_command = self.device.execute("show run")

            with open('Command_Output.txt', 'w') as f:
                f.write(self.parsed_command)

        elif "show log" in self.command:
            self.parsed_command = self.device.execute("show logging")

            with open('Command_Output.txt', 'w') as f:
                f.write(self.parsed_command)

        elif "show tech" in self.command:
            self.parsed_command = self.device.execute("show logging")

            with open('Command_Output.txt', 'w') as f:
                f.write(self.parsed_command)        
        else:
            try:
                self.parsed_command = self.device.parse(self.command)
                self.version_data_to_write = {"info": self.parsed_command}

                with open('Command_Output.json', 'w') as f:
                    f.write(json.dumps(self.version_data_to_write, indent=4, sort_keys=True))
            except:
                print("Unable to parse show command please reference the available parsers here - https://developer.cisco.com/docs/genie-docs/")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        testbed.disconnect()

# for running as its own executable
if __name__ == '__main__':
    aetest.main()