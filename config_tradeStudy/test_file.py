import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/" + ".."))

import numpy as np
from gpkit import Model, ureg
from aircraft_models import OnDemandAircraft
from aircraft_models import OnDemandSizingMission, OnDemandRevenueMission
from aircraft_models import OnDemandDeadheadMission, OnDemandMissionCost
from study_input_data import generic_data, configuration_data
from copy import deepcopy


def test(generic_data, configuration_data, config):

    configs = configuration_data.copy()
    c = configs[config]

    problem_subDict = {}

    Aircraft = OnDemandAircraft(autonomousEnabled=generic_data["autonomousEnabled"])
    problem_subDict.update(
        {
            Aircraft.L_D_cruise: c["L/D"],  # estimated L/D in cruise
            Aircraft.eta_cruise: generic_data[
                "\eta_{cruise}"
            ],  # propulsive efficiency in cruise
            Aircraft.tailRotor_power_fraction_hover: c[
                "tailRotor_power_fraction_hover"
            ],
            Aircraft.tailRotor_power_fraction_levelFlight: c[
                "tailRotor_power_fraction_levelFlight"
            ],
            Aircraft.cost_per_weight: generic_data[
                "vehicle_cost_per_weight"
            ],  # vehicle cost per unit empty weight
            Aircraft.battery.C_m: generic_data["C_m"],  # battery energy density
            Aircraft.battery.cost_per_C: generic_data[
                "battery_cost_per_C"
            ],  # battery cost per unit energy capacity
            Aircraft.rotors.N: c["N"],  # number of propellers
            Aircraft.rotors.Cl_mean_max: c[
                "Cl_{mean_{max}}"
            ],  # maximum allowed mean lift coefficient
            Aircraft.structure.weight_fraction: c[
                "weight_fraction"
            ],  # empty weight fraction
            Aircraft.electricalSystem.eta: generic_data[
                "\eta_{electric}"
            ],  # electrical system efficiency
        }
    )

    SizingMission = OnDemandSizingMission(
        Aircraft,
        mission_type=generic_data["sizing_mission"]["type"],
        reserve_type=generic_data["reserve_type"],
    )
    problem_subDict.update(
        {
            SizingMission.mission_range: generic_data["sizing_mission"][
                "range"
            ],  # mission range
            SizingMission.V_cruise: c["V_{cruise}"],  # cruising speed
            SizingMission.t_hover: generic_data["sizing_mission"][
                "t_{hover}"
            ],  # hover time
            SizingMission.T_A: c["T/A"],  # disk loading
            SizingMission.passengers.N_passengers: generic_data["sizing_mission"][
                "N_passengers"
            ],  # Number of passengers
        }
    )

    RevenueMission = OnDemandRevenueMission(
        Aircraft, mission_type=generic_data["revenue_mission"]["type"]
    )
    problem_subDict.update(
        {
            RevenueMission.mission_range: generic_data["revenue_mission"][
                "range"
            ],  # mission range
            RevenueMission.V_cruise: c["V_{cruise}"],  # cruising speed
            RevenueMission.t_hover: generic_data["revenue_mission"][
                "t_{hover}"
            ],  # hover time
            RevenueMission.passengers.N_passengers: generic_data["revenue_mission"][
                "N_passengers"
            ],  # Number of passengers
            RevenueMission.time_on_ground.charger_power: generic_data[
                "charger_power"
            ],  # Charger power
        }
    )

    DeadheadMission = OnDemandDeadheadMission(
        Aircraft, mission_type=generic_data["deadhead_mission"]["type"]
    )
    problem_subDict.update(
        {
            DeadheadMission.mission_range: generic_data["deadhead_mission"][
                "range"
            ],  # mission range
            DeadheadMission.V_cruise: c["V_{cruise}"],  # cruising speed
            DeadheadMission.t_hover: generic_data["deadhead_mission"][
                "t_{hover}"
            ],  # hover time
            DeadheadMission.passengers.N_passengers: generic_data["deadhead_mission"][
                "N_passengers"
            ],  # Number of passengers
            DeadheadMission.time_on_ground.charger_power: generic_data[
                "charger_power"
            ],  # Charger power
        }
    )

    MissionCost = OnDemandMissionCost(Aircraft, RevenueMission, DeadheadMission)
    problem_subDict.update(
        {
            MissionCost.revenue_mission_costs.operating_expenses.pilot_cost.wrap_rate: generic_data[
                "pilot_wrap_rate"
            ],  # pilot wrap rate
            MissionCost.revenue_mission_costs.operating_expenses.maintenance_cost.wrap_rate: generic_data[
                "mechanic_wrap_rate"
            ],  # mechanic wrap rate
            MissionCost.revenue_mission_costs.operating_expenses.maintenance_cost.MMH_FH: generic_data[
                "MMH_FH"
            ],  # maintenance man-hours per flight hour
            MissionCost.deadhead_mission_costs.operating_expenses.pilot_cost.wrap_rate: generic_data[
                "pilot_wrap_rate"
            ],  # pilot wrap rate
            MissionCost.deadhead_mission_costs.operating_expenses.maintenance_cost.wrap_rate: generic_data[
                "mechanic_wrap_rate"
            ],  # mechanic wrap rate
            MissionCost.deadhead_mission_costs.operating_expenses.maintenance_cost.MMH_FH: generic_data[
                "MMH_FH"
            ],  # maintenance man-hours per flight hour
            MissionCost.deadhead_ratio: generic_data[
                "deadhead_ratio"
            ],  # deadhead ratio
            # MissionCost.NdNr: 0.25,
        }
    )

    problem = Model(
        MissionCost["cost_per_trip"],
        [Aircraft, SizingMission, RevenueMission, DeadheadMission, MissionCost],
    )
    # problem = Model(Aircraft["TOGW"],[Aircraft, SizingMission])
    problem.substitutions.update(problem_subDict)

    try:
        solution = problem.solve(verbosity=0)
        return solution
    except:
        return problem

    # problem_subDict = None
    # problem = None


if __name__ == "__main__":

    # deadhead_N_passengers_array = [0.5 0.1 0.01 0.001 0.0001 0.00001]
    deadhead_N_passengers_array = [0.5, 0.1, 0.01, 0.001, 0.0001, 0.00001]

    for np in deadhead_N_passengers_array:
        for i in range(1, 51):
            # print "Test run %0.0f" % i

            """
            configs = configuration_data.copy()
            del configs["Tilt duct"]
            del configs["Multirotor"]
            del configs["Autogyro"]
            del configs["Helicopter"]
            del configs["Coaxial heli"]

            #config_array = ["Lift + cruise","Lift + cruise"]
            """
            generic_data["deadhead_mission"]["N_passengers"] = np
            solution = test(generic_data, configuration_data, "Lift + cruise")

        print(
            "Cost per trip is $%0.2f with %0.5f deadhead passengers. %0.0f iterations."
            % (
                solution("cost_per_trip"),
                solution("N_{passengers}_OnDemandDeadheadMission/Passengers"),
                i,
            )
        )
