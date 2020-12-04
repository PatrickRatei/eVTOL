# Substitution functions, for both generic and configuration-specific inputs

from gpkit import ureg
from collections import OrderedDict

# Generic data (i.e. for all configs)
generic_data = {}
generic_data["UseCase"] = "Intra-City"
generic_data["TimeFrame"] = "2025"
generic_data["autonomousEnabled"] = True
generic_data["isSizingMissionPiloted"] = True
generic_data["isRevenueMissionPiloted"] = True
generic_data["isDeadheadMissionPiloted"] = False
generic_data["reserve"] = "20-minute loiter"

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

# Use case options
if generic_data["TimeFrame"] == "2025":
    generic_data["isSizingMissionPiloted"] = True
    generic_data["isRevenueMissionPiloted"] = True
    generic_data["isDeadheadMissionPiloted"] = False

elif generic_data["TimeFrame"] == "2050":
    generic_data["isSizingMissionPiloted"] = False
    generic_data["isRevenueMissionPiloted"] = False
    generic_data["isDeadheadMissionPiloted"] = False


def on_demand_aircraft_substitutions(
    aircraft, config="Lift + cruise", autonomousEnabled=True
):

    aircraft.substitutions.update(
        {
            aircraft.g: 9.807 * ureg.m / ureg.s ** 2,
            aircraft.eta_levelFlight: 0.85,
            aircraft.airframe.cost_per_weight: 350.0 * ureg.lbf ** -1,
            aircraft.airframe.lifetime: 20000.0 * ureg.hour,
            aircraft.avionics.lifetime: 20000 * ureg.hour,
            aircraft.battery.E_frac: 0.64,
            aircraft.battery.e: 300.0 * ureg.Wh / ureg.kg,
            aircraft.battery.p: 3.0 * ureg.kW / ureg.kg,
            aircraft.battery.cost_per_energy: 400.0 * ureg.kWh ** -1,
            aircraft.battery.cycle_life: 2000.0,
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
                aircraft.avionics.purchase_price: 60000.0,
            }
        )
    else:
        aircraft.substitutions.update(
            {
                aircraft.avionics.purchase_price: 1.0,  # Negligibly small
            }
        )

    if config == "Multirotor":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.43,
                aircraft.v_cruise: 50.0 * ureg.mph,
                aircraft.L_D_cruise: 3.5,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 8.0,
                aircraft.rotors.T_A_max: 3.75 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.6,
            }
        )

    elif config == "Autogyro":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.5,
                aircraft.v_cruise: 100.0 * ureg.mph,
                aircraft.L_D_cruise: 3.5,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 1,
                aircraft.rotors.T_A_max: 3.75 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.8,
            }
        )

    elif config == "Helicopter":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.43,
                aircraft.v_cruise: 100.0 * ureg.mph,
                aircraft.L_D_cruise: 4.25,
                aircraft.tailRotor_power_fraction_hover: 0.15,
                aircraft.tailRotor_power_fraction_levelFlight: 0.15,
                aircraft.rotors.N: 1.0,
                aircraft.rotors.T_A_max: 4.5 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.6,
            }
        )

    elif config == "Tilt duct":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.55,
                aircraft.v_cruise: 150.0 * ureg.mph,
                aircraft.L_D_cruise: 10.0,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 36.0,
                aircraft.rotors.T_A_max: 40.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    elif config == "Coaxial heli":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.43,
                aircraft.v_cruise: 150.0 * ureg.mph,
                aircraft.L_D_cruise: 5.5,
                aircraft.tailRotor_power_fraction_hover: 0.001,
                aircraft.tailRotor_power_fraction_levelFlight: 0.001,
                aircraft.rotors.N: 2.0,
                aircraft.rotors.T_A_max: 7.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.6,
            }
        )

    elif config == "Lift + cruise":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.53,
                aircraft.v_cruise: 93.0 * ureg.mph,
                aircraft.L_D_cruise: 10.0,
                aircraft.tailRotor_power_fraction_hover: 0.005,
                aircraft.tailRotor_power_fraction_levelFlight: 0.005,
                aircraft.rotors.N: 8.0,
                aircraft.rotors.T_A_max: 15.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    elif config == "Tilt wing":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.55,
                aircraft.v_cruise: 150.0 * ureg.mph,
                aircraft.L_D_cruise: 12.0,
                aircraft.tailRotor_power_fraction_hover: 0.005,
                aircraft.tailRotor_power_fraction_levelFlight: 0.005,
                aircraft.rotors.N: 8.0,
                aircraft.rotors.T_A_max: 15.0 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 1.0,
            }
        )

    elif config == "Compound heli":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.5,
                aircraft.v_cruise: 150.0 * ureg.mph,
                aircraft.L_D_cruise: 9.0,
                aircraft.tailRotor_power_fraction_hover: 0.15,
                aircraft.tailRotor_power_fraction_levelFlight: 0.10,
                aircraft.rotors.N: 1.0,
                aircraft.rotors.T_A_max: 4.5 * ureg.lbf / ureg.ft ** 2,
                aircraft.rotors.Cl_mean_max: 0.8,
            }
        )

    elif config == "Tilt rotor":
        aircraft.substitutions.update(
            {
                aircraft.empty_mass_fraction: 0.55,
                aircraft.v_cruise: 150.0 * ureg.mph,
                aircraft.L_D_cruise: 14.0,
                aircraft.tailRotor_power_fraction_hover: 0.005,
                aircraft.tailRotor_power_fraction_levelFlight: 0.005,
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
            mission.crew.W_unit: 190.0 * ureg.lbf,
            mission.passengers.W_unit: 200.0 * ureg.lbf,
            mission.passengers.N: 3.0,
            mission.takeoff_segment.t_segment: 2.0 * ureg.minute,
            mission.cruise_segment.d_segment: 16.2 * ureg.nautical_mile,
            mission.landing_segment.t_segment: 2.0 * ureg.minute,
        }
    )

    if piloted:
        mission.substitutions.update(
            {
                mission.crew.N: 1,
            }
        )

    else:
        mission.substitutions.update(
            {
                mission.crew.N: 0.001,  # Negligibly small
            }
        )

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
            mission.crew.W_unit: 190.0 * ureg.lbf,
            mission.passengers.W_unit: 200.0 * ureg.lbf,
            mission.passengers.N: 3.0,
            mission.takeoff_segment.t_segment: 30.0 * ureg.s,
            mission.cruise_segment.d_segment: 16.2 * ureg.nautical_mile,
            mission.landing_segment.t_segment: 30.0 * ureg.s,
            mission.ground_segment.t_passenger: 5.0 * ureg.min,
            mission.ground_segment.charger.P: 200.0 * ureg.kW,
            mission.ground_segment.charger.eta: 0.9,
        }
    )

    if piloted:
        mission.substitutions.update(
            {
                mission.crew.N: 1,
            }
        )

    else:
        mission.substitutions.update(
            {
                mission.crew.N: 0.001,  # Negligibly small
            }
        )

    return mission


def on_demand_deadhead_mission_substitutions(mission, piloted=False):

    mission.substitutions.update(
        {
            mission.crew.W_unit: 190.0 * ureg.lbf,
            mission.passengers.W_unit: 200.0 * ureg.lbf,
            mission.passengers.N: 0.001,  # Negligibly small
            mission.takeoff_segment.t_segment: 30.0 * ureg.s,
            mission.cruise_segment.d_segment: 30.0 * ureg.nautical_mile,
            mission.landing_segment.t_segment: 30.0 * ureg.s,
            mission.ground_segment.t_passenger: 5.0 * ureg.min,
            mission.ground_segment.charger.P: 200.0 * ureg.kW,
            mission.ground_segment.charger.eta: 0.9,
        }
    )

    if piloted:
        mission.substitutions.update(
            {
                mission.crew.N: 1,
            }
        )

    else:
        mission.substitutions.update(
            {
                mission.crew.N: 0.001,  # Negligibly small
            }
        )

    return mission


def on_demand_mission_cost_substitutions(
    mission_cost, isRevenueMissionPiloted=True, isDeadheadMissionPiloted=False
):

    mission_cost.substitutions.update(
        {
            mission_cost.deadhead_ratio: 0.2,
            mission_cost.revenue_mission_cost.operating_expenses.pilot_cost.wrap_rate: 70.0
            * ureg.hr ** -1,
            mission_cost.deadhead_mission_cost.operating_expenses.pilot_cost.wrap_rate: 70.0
            * ureg.hr ** -1,
            mission_cost.revenue_mission_cost.operating_expenses.maintenance_cost.wrap_rate: 60.0
            * ureg.hr ** -1,
            mission_cost.deadhead_mission_cost.operating_expenses.maintenance_cost.wrap_rate: 60.0
            * ureg.hr ** -1,
            mission_cost.revenue_mission_cost.operating_expenses.maintenance_cost.MMH_FH: 0.6,
            mission_cost.deadhead_mission_cost.operating_expenses.maintenance_cost.MMH_FH: 0.6,
            mission_cost.revenue_mission_cost.operating_expenses.energy_cost.cost_per_energy: 0.12
            * ureg.kWh ** -1,
            mission_cost.deadhead_mission_cost.operating_expenses.energy_cost.cost_per_energy: 0.12
            * ureg.kWh ** -1,
            mission_cost.revenue_mission_cost.operating_expenses.IOC_fraction: 0.12,
            mission_cost.deadhead_mission_cost.operating_expenses.IOC_fraction: 0.12,
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
                / 8,  # 8 aircraft per bunker pilot
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
                / 8,  # 8 aircraft per bunker pilot
            }
        )

    return mission_cost
