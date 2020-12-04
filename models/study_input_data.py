# Contains study input data

from gpkit import ureg
from collections import OrderedDict

# Generic data (i.e. for all configs)
generic_data = {}

# Acoustic computation inputs
generic_data["delta_S"] = 500 * ureg.ft
generic_data["Strouhal_number"] = 0.28

# Mission inputs
generic_data["autonomousEnabled"] = True
generic_data["isSizingMissionPiloted"] = True
generic_data["isRevenueMissionPiloted"] = True
generic_data["isDeadheadMissionPiloted"] = False
generic_data["reserve"] = "20-minute loiter"

# Configurations included in the trade study
configs = OrderedDict()
# configs["Helicopter"] = {}
configs["Coaxial heli"] = {}
configs["Compound heli"] = {}
# configs["Multirotor"] = {}
# configs["Lift + cruise"] = {}
# configs["Tilt wing"] = {}
# configs["Tilt rotor"] = {}
# configs["Tilt duct"] = {}
# configs["Autogyro"] = {}