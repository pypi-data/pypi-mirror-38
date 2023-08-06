Example Usage:

```
from roboteq import RoboteqDevice

from roboteq.roboteq_constants import _MMOD, _G, _RWD, _MXMD, _MXRPM

device = RoboteqDevice()
device.connect("/dev/serial/by-id/usb-Roboteq_Motor_Controller_FBL2XXX-if00")


time.sleep(0.1)
device.set_config(_MMOD, 0, 6)
time.sleep(0.1)
device.command_motor(_G, 1, 0)
time.sleep(0.1)
device.command_motor(_G, 2, 0)
time.sleep(0.1)
device.set_config(_RWD, 1000)
time.sleep(0.1)
device.set_config(_MXMD, 1)
time.sleep(0.1)
device.send_command(_MXRPM, 1, 500)
time.sleep(0.1)
device.send_command(_MXRPM, 2, 500)
time.sleep(0.1)
```