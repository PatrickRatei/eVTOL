# Substitution functions, for both generic and configuration-specific inputs

from gpkit import ureg
from collections import OrderedDict

# Generic data (i.e. for all configs)
generic_data = {}
time_frame = "2050"  # Years 2025 and 2050
use_case = "Sub-Urban"  # Intra-City, Airport Shuttle, Sub-Urban, Megacity

# Configurations included in the trade study
configs = OrderedDict()
configs["Helicopter"] = {}
configs["Coaxial heli"] = {}
configs["Compound heli"] = {}
configs["Multirotor"] = {}
configs["Lift + cruise"] = {}
configs["Tilt wing"] = {}
configs["Tilt rotor"] = {}
# configs["Tilt duct"] = {}
# configs["Autogyro"] = {}

# Acoustic computation inputs
generic_data["delta_S"] = 500 * ureg.ft
generic_data["Strouhal_number"] = 0.28

# Time frame options
if time_frame == "2025":
    generic_data["autonomousEnabled"] = True
    generic_data["isSizingMissionPiloted"] = True
    generic_data["isRevenueMissionPiloted"] = True
    generic_data["isDeadheadMissionPiloted"] = False
    generic_data["reserve"] = "20-minute loiter"
    airframe_cost_per_weight = 500.0 * ureg.lbf ** -1
    avionics_purchase_price = 100000.0
    airframe_lifetime = 10000.0 * ureg.hour
    avionics_lifetime = 10000.0 * ureg.hour
    battery_energy_density = 300.0 * ureg.Wh / ureg.kg
    battery_power_density = 3.0 * ureg.kW / ureg.kg
    battery_energy_fraction = 0.8
    battery_cost_per_energy = 250.0 * ureg.kWh ** -1
    battery_cycle_life = 800.0
    aircraft_per_remote_pilot = 4
    charger_power = 250.0 * ureg.kW
    cost_per_energy = 0.21 * ureg.kWh ** -1
    IOC_fraction = 0.40
    deadhead_ratio = 0.35

elif time_frame == "2050":
    generic_data["autonomousEnabled"] = True
    generic_data["isSizingMissionPiloted"] = False
    generic_data["isRevenueMissionPiloted"] = False
    generic_data["isDeadheadMissionPiloted"] = False
    generic_data["reserve"] = "5-nmi diversion"
    airframe_cost_per_weight = 200.0 * ureg.lbf ** -1
    avionics_purchase_price = 60000.0
    airframe_lifetime = 20000.0 * ureg.hour
    avionics_lifetime = 20000.0 * ureg.hour
    battery_energy_density = 600.0 * ureg.Wh / ureg.kg
    battery_power_density = 5.0 * ureg.kW / ureg.kg
    battery_energy_fraction = 0.9
    battery_cost_per_energy = 150.0 * ureg.kWh ** -1
    battery_cycle_life = 2000.0
    aircraft_per_remote_pilot = 8
    charger_power = 1000.0 * ureg.kW
    cost_per_energy = 0.15 * ureg.kWh ** -1
    IOC_fraction = 0.30
    deadhead_ratio = 0.15

else:
    error_string = "Time frame " + time_frame + " not recognized."
    raise ValueError(error_string)

# Use case options
if use_case == "Intra-City":
    sizing_takeoff_segment = 6.0 * ureg.minute
    sizing_cruise_segment = 50.0 * ureg.km
    sizing_landing_segment = 6.0 * ureg.minute
    takeoff_segment = 1.5 * ureg.minute
    cruise_segment = 50.0 * ureg.km
    landing_segment = 1.5 * ureg.minute
    v_cruise = 100 * ureg.kph
    weight_per_crew = 198.4 * ureg.lbf
    weight_per_passenger = 198.4 * ureg.lbf
    n_passengers = 4

elif use_case == "Airport Shuttle":
    sizing_takeoff_segment = 2.0 * ureg.minute
    sizing_cruise_segment = 30.0 * ureg.km
    sizing_landing_segment = 2.0 * ureg.minute
    takeoff_segment = 0.5 * ureg.minute
    cruise_segment = 30.0 * ureg.km
    landing_segment = 0.5 * ureg.minute
    v_cruise = 150 * ureg.kph
    weight_per_crew = 198.4 * ureg.lbf
    weight_per_passenger = 242.5 * ureg.lbf
    n_passengers = 4

elif use_case == "Sub-Urban":
    sizing_takeoff_segment = 2.0 * ureg.minute
    sizing_cruise_segment = 70.0 * ureg.km
    sizing_landing_segment = 2.0 * ureg.minute
    takeoff_segment = 0.5 * ureg.minute
    cruise_segment = 70.0 * ureg.km
    landing_segment = 0.5 * ureg.minute
    v_cruise = 150 * ureg.kph
    weight_per_crew = 198.4 * ureg.lbf
    weight_per_passenger = 198.4 * ureg.lbf
    n_passengers = 4

elif use_case == "Inter-City":
    sizing_takeoff_segment = 2.0 * ureg.minute
    sizing_cruise_segment = 200.0 * ureg.km
    sizing_landing_segment = 2.0 * ureg.minute
    takeoff_segment = 0.5 * ureg.minute
    cruise_segment = 150.0 * ureg.km
    landing_segment = 0.5 * ureg.minute
    v_cruise = 240 * ureg.kph
    weight_per_crew = 198.4 * ureg.lbf
    weight_per_passenger = 220.5 * ureg.lbf
    n_passengers = 10

elif use_case == "Megacity":
    sizing_takeoff_segment = 2.0 * ureg.minute
    sizing_cruise_segment = 100.0 * ureg.km
    sizing_landing_segment = 2.0 * ureg.minute
    takeoff_segment = 0.5 * ureg.minute
    cruise_segment = 100.0 * ureg.km
    landing_segment = 0.5 * ureg.minute
    v_cruise = 150 * ureg.kph
    weight_per_crew = 198.4 * ureg.lbf
    weight_per_passenger = 198.4 * ureg.lbf
    n_passengers = 6

elif use_case == "Wildfire":
    sizing_takeoff_segment = 8.0 * ureg.minute
    sizing_cruise_segment = 100.0 * ureg.km
    sizing_landing_segment = 8.0 * ureg.minute
    takeoff_segment = 2.0 * ureg.minute
    cruise_segment = 100.0 * ureg.km
    landing_segment = 2.0 * ureg.minute
    v_cruise = 150 * ureg.kph
    weight_per_crew = 198.4 * ureg.lbf
    weight_per_passenger = 3306.0 * ureg.lbf
    n_passengers = 1

else:
    error_string = "Use case " + use_case + " not recognized."
    raise ValueError(error_string)

# Vehicle speed limits
v_max_multirotor = 120 * ureg.kph
if v_cruise > v_max_multirotor:
    v_cruise_multirotor = v_max_multirotor
else:
    v_cruise_multirotor = v_cruise

v_max_helicopter = 250 * ureg.kph
if v_cruise > v_max_helicopter:
    v_cruise_helicopter = v_max_helicopter
else:
    v_cruise_helicopter = v_cruise


def on_demand_aircraft_substitutions(
    aircraft, config="Lift + cruise", autonomousEnabled=True
):

    aircraft.substitutions.update(
        {
            aircraft.g: 9.807 * ureg.m / ureg.s ** 2,
            aircraft.eta_levelFlight: 0.85,
            aircraft.airframe.cost_per_weight: airframe_cost_per_weight,
            aircraft.airframe.lifetime: airframe_lifetime,
            aircraft.avionics.lifetime: avionics_lifetime,
            aircraft.battery.E_frac: battery_energy_fraction,
            aircraft.battery.e: battery_energy_density,
            aircraft.battery.p: battery_power_density,
            aircraft.battery.cost_per_energy: battery_cost_per_energy,
            aircraft.battery.cycle_life: battery_cycle_life,
            aircraft.rotors.B: 5.0,
            aircraft.rotors.s: 0.1,
            aircraft.rotors.t_c: 0.12,
            aircraft.rotors.ki: 1.2,
            aircraft.rotors.Cd0: 0.01,
            aircraft.rotors.M_tip_max: 0.9,
            aircraft.electrical_system.eta: 0.9,
        }
    )

    if autonomousEnabled:
        aircraft.substitutions.update(
            {
                aircraft.avionics.purchase_price: avionics_purchase_price,
            }
        )
    else:
        aircraft.substitutions.update(
            {
                aircraft.avionics.purchase_price: 1.0,  # Negligibly small
            }
        )

    if config == "Autogyro":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.5,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 3.5,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 1,
                aircraft.rotors.T_A_max: 3.75 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.8,
            }
        )

    elif config == "Tilt duct":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.55,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 10.0,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 36.0,
                aircraft.rotors.T_A_max: 40.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    elif config == "Helicopter":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.43,
                aircraft.v_cruise: v_cruise_helicopter,
                aircraft.L_D_cruise: 4.25,
                aircraft.tailRotor_power_fraction_hover: 0.15,
                aircraft.tailRotor_power_fraction_levelFlight: 0.15,
                aircraft.rotors.N: 1.0,
                aircraft.rotors.T_A_max: 4.5 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.6,
            }
        )

    elif config == "Coaxial heli":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.43,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 5.5,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 2.0,
                aircraft.rotors.T_A_max: 7.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.6,
            }
        )

    elif config == "Compound heli":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.5,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 9.0,
                aircraft.tailRotor_power_fraction_hover: 0.15,
                aircraft.tailRotor_power_fraction_levelFlight: 0.10,
                aircraft.rotors.N: 1.0,
                aircraft.rotors.T_A_max: 4.5 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.8,
            }
        )

    elif config == "Multirotor":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.43,
                aircraft.v_cruise: v_cruise_multirotor,
                aircraft.L_D_cruise: 3.0,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 8.0,
                aircraft.rotors.T_A_max: 3.75 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.6,
            }
        )

    elif config == "Lift + cruise":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.53,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 10.0,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 8.0,
                aircraft.rotors.T_A_max: 15.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    elif config == "Tilt wing":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.55,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 12.0,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 8.0,
                aircraft.rotors.T_A_max: 15.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    elif config == "Tilt rotor":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.55,
                aircraft.v_cruise: v_cruise,
                aircraft.L_D_cruise: 14.0,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 12.0,
                aircraft.rotors.T_A_max: 15.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    else:
        error_string = "Configuration " + config + " not recognized."
        raise ValueError(error_string)

    return aircraft


def on_demand_sizing_mission_substitutions(
    mission, piloted=True, reserve="20-minute loiter"
):

    mission.substitutions.update(
        {
            mission.crew.W_unit: weight_per_crew,
            mission.passengers.W_unit: weight_per_passenger,
            mission.passengers.N: n_passengers,
            mission.takeoff_segment.t_segment: sizing_takeoff_segment,
            mission.cruise_segment.d_segment: sizing_cruise_segment,
            mission.landing_segment.t_segment: sizing_landing_segment,
        }
    )

    if piloted:
        mission.substitutions.update(
            {mission.crew.N: 1, mission.passengers.N: n_passengers - 1}
        )

    else:
        mission.substitutions.update({mission.crew.N: 0.001})

    if reserve == "20-minute loiter":
        mission.substitutions.update(
            {
                mission.reserve_segment.t_segment: 20.0 * ureg.minute,
                mission.v_reserve_nondim: ((1.0 / 3.0) ** (1.0 / 4.0)),
                mission.L_D_reserve_nondim: ((3.0 ** 0.5) / 2.0),
            }
        )

    elif reserve == "30-minute loiter":
        mission.substitutions.update(
            {
                mission.reserve_segment.t_segment: 30.0 * ureg.minute,
                mission.v_reserve_nondim: ((1.0 / 3.0) ** (1.0 / 4.0)),
                mission.L_D_reserve_nondim: ((3.0 ** 0.5) / 2.0),
            }
        )

    elif reserve == "5-nmi diversion":
        mission.substitutions.update(
            {
                mission.reserve_segment.d_segment: 5.0 * ureg.nautical_mile,
                mission.v_reserve_nondim: 1.0,
                mission.L_D_reserve_nondim: 1.0,
            }
        )

    elif reserve == "2-nmi diversion":
        mission.substitutions.update(
            {
                mission.reserve_segment.d_segment: 2.0 * ureg.nautical_mile,
                mission.v_reserve_nondim: 1.0,
                mission.L_D_reserve_nondim: 1.0,
            }
        )

    else:
        error_string = "Reserve type " + reserve + " not recognized."
        raise ValueError(error_string)

    return mission


def on_demand_revenue_mission_substitutions(mission, piloted=True):

    mission.substitutions.update(
        {
            mission.crew.W_unit: weight_per_crew,
            mission.passengers.W_unit: weight_per_passenger,
            mission.passengers.N: n_passengers,
            mission.takeoff_segment.t_segment: takeoff_segment,
            mission.cruise_segment.d_segment: cruise_segment,
            mission.landing_segment.t_segment: landing_segment,
            mission.ground_segment.t_passenger: 5.0 * ureg.min,
            mission.ground_segment.charger.P: charger_power,
            mission.ground_segment.charger.eta: 0.9,
        }
    )

    if piloted:
        mission.substitutions.update(
            {mission.crew.N: 1, mission.passengers.N: n_passengers - 1}
        )

    else:
        mission.substitutions.update({mission.crew.N: 0.001})

    return mission


def on_demand_deadhead_mission_substitutions(mission, piloted=False):

    mission.substitutions.update(
        {
            mission.crew.W_unit: weight_per_crew,
            mission.passengers.W_unit: weight_per_passenger,
            mission.passengers.N: 0.001,  # Negligibly small
            mission.takeoff_segment.t_segment: takeoff_segment,
            mission.cruise_segment.d_segment: cruise_segment,
            mission.landing_segment.t_segment: takeoff_segment,
            mission.ground_segment.t_passenger: 5.0 * ureg.min,
            mission.ground_segment.charger.P: charger_power,
            mission.ground_segment.charger.eta: 0.9,
        }
    )

    if piloted:
        mission.substitutions.update(
            {mission.crew.N: 1, mission.passengers.N: n_passengers - 1}
        )

    else:
        mission.substitutions.update({mission.crew.N: 0.001})

    return mission


def on_demand_mission_cost_substitutions(
    mission_cost, isRevenueMissionPiloted=True, isDeadheadMissionPiloted=False
):

    mission_cost.substitutions.update(
        {
            mission_cost.deadhead_ratio: deadhead_ratio,
            mission_cost.revenue_mission_cost.operating_expenses.pilot_cost.wrap_rate: 100.0
            * ureg.hr ** -1,
            mission_cost.deadhead_mission_cost.operating_expenses.pilot_cost.wrap_rate: 100.0
            * ureg.hr ** -1,
            mission_cost.revenue_mission_cost.operating_expenses.maintenance_cost.wrap_rate: 60.0
            * ureg.hr ** -1,
            mission_cost.deadhead_mission_cost.operating_expenses.maintenance_cost.wrap_rate: 60.0
            * ureg.hr ** -1,
            mission_cost.revenue_mission_cost.operating_expenses.maintenance_cost.MMH_FH: 0.6,
            mission_cost.deadhead_mission_cost.operating_expenses.maintenance_cost.MMH_FH: 0.6,
            mission_cost.revenue_mission_cost.operating_expenses.energy_cost.cost_per_energy: cost_per_energy,
            mission_cost.deadhead_mission_cost.operating_expenses.energy_cost.cost_per_energy: cost_per_energy,
            mission_cost.revenue_mission_cost.operating_expenses.IOC_fraction: IOC_fraction,
            mission_cost.deadhead_mission_cost.operating_expenses.IOC_fraction: IOC_fraction,
        }
    )

    if isRevenueMissionPiloted:
        mission_cost.substitutions.update(
            {
                mission_cost.revenue_mission_cost.operating_expenses.pilot_cost.pilots_per_aircraft: 1.5,  # 1.5 pilots per aircraft
            }
        )

    else:
        mission_cost.substitutions.update(
            {
                mission_cost.revenue_mission_cost.operating_expenses.pilot_cost.pilots_per_aircraft: 1.0
                / aircraft_per_remote_pilot,  # 6 aircraft per bunker pilot
            }
        )

    if isDeadheadMissionPiloted:
        mission_cost.substitutions.update(
            {
                mission_cost.deadhead_mission_cost.operating_expenses.pilot_cost.pilots_per_aircraft: 1.5,  # 1.5 pilots per aircraft
            }
        )

    else:
        mission_cost.substitutions.update(
            {
                mission_cost.deadhead_mission_cost.operating_expenses.pilot_cost.pilots_per_aircraft: 1.0
                / aircraft_per_remote_pilot,  # 6 aircraft per bunker pilot
            }
        )

    return mission_cost
