# Vehicle configuration top-level trade study

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../models"))

import numpy as np
from gpkit import Model, ureg
from copy import deepcopy
from matplotlib import pyplot as plt
from matplotlib import rc
from aircraft_models import OnDemandAircraft
from mission_models import (
    OnDemandSizingMission,
    OnDemandRevenueMission,
    OnDemandDeadheadMission,
)
from cost_models import OnDemandMissionCost
from noise_models import vortex_noise
from standard_substitutions import generic_data, configs

configs = deepcopy(configs)


# Optimize and do noise analysis
for config in configs:

    print("Solving configuration: " + config)

    aircraft = OnDemandAircraft()
    aircraft = aircraft.standard_substitutions(
        config=config, autonomousEnabled=generic_data["autonomousEnabled"]
    )

    sizing_mission = OnDemandSizingMission(aircraft=aircraft)
    sizing_mission = sizing_mission.standard_substitutions(
        piloted=generic_data["isSizingMissionPiloted"],
        reserve=generic_data["reserve"],
    )

    revenue_mission = OnDemandRevenueMission(aircraft=aircraft)
    revenue_mission = revenue_mission.standard_substitutions(
        piloted=generic_data["isRevenueMissionPiloted"]
    )

    deadhead_mission = OnDemandDeadheadMission(aircraft=aircraft)
    deadhead_mission = deadhead_mission.standard_substitutions(
        piloted=generic_data["isDeadheadMissionPiloted"]
    )

    mission_cost = OnDemandMissionCost(
        aircraft=aircraft,
        revenue_mission=revenue_mission,
        deadhead_mission=deadhead_mission,
    )
    mission_cost = mission_cost.standard_substitutions(
        isRevenueMissionPiloted=generic_data["isRevenueMissionPiloted"],
        isDeadheadMissionPiloted=generic_data["isDeadheadMissionPiloted"],
    )

    objective_function = mission_cost.cpt
    problem = Model(
        objective_function,
        [aircraft, sizing_mission, revenue_mission, deadhead_mission, mission_cost],
    )
    solution = problem.solve(verbosity=0)

    configs[config]["solution"] = solution

    # Noise computations
    T_perRotor = solution(
        "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.T_perRotor"
    )
    T_A = solution(
        "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.T/A"
    )
    V_tip = solution(
        "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.v_{tip}"
    )
    s = solution("OnDemandAircraft.Rotors.s")
    Cl_mean = solution(
        "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.Cl_{mean}"
    )
    N = solution("OnDemandAircraft.Rotors.N")
    c_avg = solution("OnDemandAircraft.Rotors.c_{avg}")
    t_avg = solution("OnDemandAircraft.Rotors.t_{avg}")
    rho = solution(
        "OnDemandSizingMission.HoverTakeoff.HoverFlightState.FixedStandardAtmosphere.\\rho"
    )

    delta_S = generic_data["delta_S"]
    St = generic_data["Strouhal_number"]

    # Unweighted
    f_peak, SPL, spectrum = vortex_noise(
        T_perRotor,
        T_A,
        V_tip,
        s,
        Cl_mean,
        N,
        c_avg,
        t_avg,
        rho,
        delta_S,
        St,
        weighting="None",
    )

    configs[config]["SPL"] = SPL
    configs[config]["f_{peak}"] = f_peak

    # A-weighted
    f_peak, SPL, spectrum = vortex_noise(
        T_perRotor,
        T_A,
        V_tip,
        s,
        Cl_mean,
        N,
        c_avg,
        t_avg,
        rho,
        delta_S,
        St,
        weighting="A",
    )

    configs[config]["SPL_A"] = SPL


# Plotting commands
plt.ion()
plt.rc("axes", axisbelow=True)
plt.show()


y_pos = np.arange(len(configs))
labels = [""] * len(configs)
for i, config in enumerate(configs):
    if config == "Compound heli":
        labels[i] = config.replace(" ", "\n")  # Replace spaces with newlines
    elif config == "Coaxial heli":
        labels[i] = config.replace(" ", "\n")  # Replace spaces with newlines
    else:
        labels[i] = config


style = {}
style["rotation"] = 90
style["legend_ncols"] = 2
style["bar_width_wide"] = 0.7
style["bar_width_medium"] = 0.3
style["bar_width_narrow"] = 0.2
style["offsets"] = [-0.25, 0, 0.25]
style["colors"] = ["grey", "w", "k", "lightgrey"]

style["fontsize"] = {}
style["fontsize"]["xticks"] = 12
style["fontsize"]["yticks"] = 12
style["fontsize"]["xlabel"] = 18
style["fontsize"]["ylabel"] = 16
style["fontsize"]["title"] = 16
style["fontsize"]["legend"] = 11
style["fontsize"]["text_label"] = 18


# Mass breakdown
fig1 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    m_airframe = (
        configs[config]["solution"]("OnDemandAircraft.Airframe.m").to(ureg.kg).magnitude
    )
    m_battery = (
        configs[config]["solution"]("OnDemandAircraft.Battery.m").to(ureg.kg).magnitude
    )
    MTOM = configs[config]["solution"]("OnDemandAircraft.MTOM").to(ureg.kg).magnitude
    m_remainder = MTOM - m_airframe - m_battery

    if i == 0:
        plt.bar(
            i,
            m_airframe,
            align="center",
            bottom=0,
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Airframe",
        )
        plt.bar(
            i,
            m_battery,
            align="center",
            bottom=m_airframe,
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
            label="Battery",
        )
        plt.bar(
            i,
            m_remainder,
            align="center",
            bottom=m_airframe + m_battery,
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Crew & passengers",
        )
    else:
        plt.bar(
            i,
            m_airframe,
            align="center",
            bottom=0,
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            m_battery,
            align="center",
            bottom=m_airframe,
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
        )
        plt.bar(
            i,
            m_remainder,
            align="center",
            bottom=m_airframe + m_battery,
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )

plt.grid()
[ymin, ymax] = plt.gca().get_ylim()
plt.ylim(ymax=1.7 * ymax)
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Mass (kg)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Mass Breakdown",   fontsize=style["fontsize"]["title"])
plt.legend(loc="upper right", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_01_MassBreakdown.pdf")


# Energy use by mission segment (sizing mission)
fig2 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):
    solution = configs[config]["solution"]

    E_cruise = (
        solution(
            "OnDemandSizingMission.Cruise.OnDemandAircraftLevelFlightFlightPerformance.BatteryPerformance.E"
        )
        .to(ureg.kWh)
        .magnitude
    )
    E_hover = (
        (
            solution(
                "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.BatteryPerformance.E"
            )
            + solution(
                "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.BatteryPerformance.E"
            )
        )
        .to(ureg.kWh)
        .magnitude
    )
    E_reserve = (
        solution(
            "OnDemandSizingMission.Reserve.OnDemandAircraftLevelFlightFlightPerformance.BatteryPerformance.E"
        )
        .to(ureg.kWh)
        .magnitude
    )

    if i == 0:
        plt.bar(
            i,
            E_cruise,
            align="center",
            bottom=0,
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Cruise",
        )
        plt.bar(
            i,
            E_hover,
            align="center",
            bottom=E_cruise,
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
            label="Hover",
        )
        plt.bar(
            i,
            E_reserve,
            align="center",
            bottom=E_cruise + E_hover,
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Reserve",
        )
    else:
        plt.bar(
            i,
            E_cruise,
            align="center",
            bottom=0,
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            E_hover,
            align="center",
            bottom=E_cruise,
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
        )
        plt.bar(
            i,
            E_reserve,
            align="center",
            bottom=E_cruise + E_hover,
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )


plt.grid()
[ymin, ymax] = plt.gca().get_ylim()
plt.ylim(ymax=1.4 * ymax)
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Energy (kWh)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Energy Use",       fontsize=style["fontsize"]["title"])
plt.legend(loc="upper right", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_02_EnergyUse.pdf")


# Power draw by mission segment (sizing mission)
fig3 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):
    solution = configs[config]["solution"]

    P_electric = np.zeros(3)
    P_electric[0] = (
        solution("OnDemandSizingMission.Cruise.LevelFlightState.P_{electric}")
        .to(ureg.kW)
        .magnitude
    )  # Cruise
    P_electric[1] = (
        solution("OnDemandSizingMission.HoverTakeoff.HoverFlightState.P_{electric}")
        .to(ureg.kW)
        .magnitude
    )  # Hover
    P_electric[2] = (
        solution("OnDemandSizingMission.Reserve.LevelFlightState.P_{electric}")
        .to(ureg.kW)
        .magnitude
    )  # Reserve

    for j, offset in enumerate(style["offsets"]):
        if i == 0:
            if j == 0:
                label = "Cruise"
            elif j == 1:
                label = "Hover"
            elif j == 2:
                label = "Reserve"

            plt.bar(
                i + offset,
                P_electric[j],
                align="center",
                alpha=1,
                width=style["bar_width_narrow"],
                color=style["colors"][j],
                edgecolor="k",
                label=label,
            )
        else:
            plt.bar(
                i + offset,
                P_electric[j],
                align="center",
                alpha=1,
                width=style["bar_width_narrow"],
                color=style["colors"][j],
                edgecolor="k",
            )

[ymin, ymax] = plt.gca().get_ylim()
plt.ylim(ymax=1.6 * ymax)
plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Power (kW)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Battery Power Draw", fontsize=style["fontsize"]["title"])
plt.legend(loc="upper right", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_03_BatteryPowerDraw.pdf")


# Mission time
fig4 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    t_flight = (
        configs[config]["solution"]("OnDemandRevenueMission.t_{flight}")
        .to(ureg.min)
        .magnitude
    )
    t_charge = (
        configs[config]["solution"]("OnDemandRevenueMission.TimeOnGround.t_{segment}")
        .to(ureg.min)
        .magnitude
    )

    if i == 0:
        plt.bar(
            i,
            t_flight,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Flight time",
        )
        plt.bar(
            i,
            t_charge,
            bottom=t_flight,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Charging time",
        )
    else:
        plt.bar(
            i,
            t_flight,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            t_charge,
            bottom=t_flight,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )

plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Time (minutes)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Mission Time",      fontsize=style["fontsize"]["title"])
plt.legend(loc="lower left", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_04_MissionTime.pdf")


# Trip cost
fig5 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    cpt_revenue = configs[config]["solution"]("revenue_cost_per_trip").magnitude
    cpt_deadhead = configs[config]["solution"]("deadhead_cost_per_trip").magnitude

    if i == 0:
        plt.bar(
            i,
            cpt_revenue,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Revenue mission",
        )
        plt.bar(
            i,
            cpt_deadhead,
            bottom=cpt_revenue,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Deadhead effect",
        )
    else:
        plt.bar(
            i,
            cpt_revenue,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            cpt_deadhead,
            bottom=cpt_revenue,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )

plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Cost ($US/trip)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Trip Cost ",       fontsize=style["fontsize"]["title"])
plt.legend(loc="lower left", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_05_TripCost.pdf")


# Cost per Passenger Kilometer
fig6 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    cpsk = (
        configs[config]["solution"]("OnDemandMissionCost.cost_per_passenger_km")
        .to(ureg.km ** -1)
        .magnitude
    )
    plt.bar(i, cpsk, align="center", alpha=1, color="k", edgecolor="k")

plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Cost ($US/km)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Cost per Passenger Kilometer",  fontsize=style["fontsize"]["title"])

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_06_CostPerPassengerKilometer.pdf")


# Vehicle Purchase Price
fig7 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    c_airframe = (
        configs[config]["solution"](
            "OnDemandAircraft.Airframe.purchase_price"
        ).magnitude
        / 1e3
    )
    c_avionics = (
        configs[config]["solution"](
            "OnDemandAircraft.Avionics.purchase_price"
        ).magnitude
        / 1e3
    )
    c_battery = (
        configs[config]["solution"]("OnDemandAircraft.Battery.purchase_price").magnitude
        / 1e3
    )

    if i == 0:
        plt.bar(
            i,
            c_airframe,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Airframe",
        )
        plt.bar(
            i,
            c_avionics,
            bottom=c_airframe,
            align="center",
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
            label="Avionics",
        )
        plt.bar(
            i,
            c_battery,
            bottom=c_airframe + c_avionics,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Battery",
        )
    else:
        plt.bar(
            i,
            c_airframe,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            c_avionics,
            bottom=c_airframe,
            align="center",
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
        )
        plt.bar(
            i,
            c_battery,
            bottom=c_airframe + c_avionics,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )

plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Price ($thousands US)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Purchase Price",         fontsize=style["fontsize"]["title"])
plt.legend(loc="lower left", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_07_PurchasePrice.pdf")


# Capital Expenses (revenue mission)
fig8 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    c_airframe = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.CapitalExpenses.AirframeAcquisitionCost.cost_per_mission"
    ).magnitude
    c_avionics = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.CapitalExpenses.AvionicsAcquisitionCost.cost_per_mission"
    ).magnitude
    c_battery = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.CapitalExpenses.BatteryAcquisitionCost.cost_per_mission"
    ).magnitude

    if i == 0:
        plt.bar(
            i,
            c_airframe,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Airframe",
        )
        plt.bar(
            i,
            c_avionics,
            bottom=c_airframe,
            align="center",
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
            label="Avionics",
        )
        plt.bar(
            i,
            c_battery,
            bottom=c_airframe + c_avionics,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Battery",
        )
    else:
        plt.bar(
            i,
            c_airframe,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            c_avionics,
            bottom=c_airframe,
            align="center",
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
        )
        plt.bar(
            i,
            c_battery,
            bottom=c_airframe + c_avionics,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )

plt.grid()
[ymin, ymax] = plt.gca().get_ylim()
plt.ylim(ymax=1.35 * ymax)
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Cost ($US/mission)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Mission Capital Expenses", fontsize=style["fontsize"]["title"])
plt.legend(loc="upper right", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_08_MissionCapitalExpenses.pdf")


# Operating Expenses (revenue mission)
fig9 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    c_pilot = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.OperatingExpenses.PilotCost.cost_per_mission"
    ).magnitude
    c_maintenance = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.OperatingExpenses.MaintenanceCost.cost_per_mission"
    ).magnitude
    c_energy = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.OperatingExpenses.EnergyCost.cost_per_mission"
    ).magnitude
    IOC = configs[config]["solution"](
        "OnDemandMissionCost.RevenueMissionCost.OperatingExpenses.IndirectOperatingCost.cost_per_mission"
    ).magnitude

    if i == 0:
        plt.bar(
            i,
            c_pilot,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
            label="Pilot",
        )
        plt.bar(
            i,
            c_maintenance,
            bottom=c_pilot,
            align="center",
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
            label="Maintenance",
        )
        plt.bar(
            i,
            c_energy,
            bottom=c_pilot + c_maintenance,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
            label="Energy",
        )
        plt.bar(
            i,
            IOC,
            bottom=c_pilot + c_maintenance + c_energy,
            align="center",
            alpha=1,
            color=style["colors"][3],
            edgecolor="k",
            label="IOC",
        )
    else:
        plt.bar(
            i,
            c_pilot,
            bottom=0,
            align="center",
            alpha=1,
            color=style["colors"][0],
            edgecolor="k",
        )
        plt.bar(
            i,
            c_maintenance,
            bottom=c_pilot,
            align="center",
            alpha=1,
            color=style["colors"][1],
            edgecolor="k",
        )
        plt.bar(
            i,
            c_energy,
            bottom=c_pilot + c_maintenance,
            align="center",
            alpha=1,
            color=style["colors"][2],
            edgecolor="k",
        )
        plt.bar(
            i,
            IOC,
            bottom=c_pilot + c_maintenance + c_energy,
            align="center",
            alpha=1,
            color=style["colors"][3],
            edgecolor="k",
        )

plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("Cost ($US/mission)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Mission Operating Expenses", fontsize=style["fontsize"]["title"])
plt.legend(loc="lower left", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_09_MissionOperatingExpenses.pdf")

# Sound Pressure Level (sizing mission)
fig10 = plt.figure(figsize=(4, 3.7), dpi=80)
for i, config in enumerate(configs):

    SPL_A = configs[config]["SPL_A"].magnitude

    plt.bar(i, SPL_A, align="center", alpha=1, color="k", edgecolor="k")

plt.grid()
plt.xticks(
    y_pos, labels, fontsize=style["fontsize"]["xticks"], rotation=style["rotation"]
)
plt.yticks(fontsize=style["fontsize"]["yticks"])
plt.ylabel("SPL (dBA)", fontsize=style["fontsize"]["ylabel"])
# plt.title("Hover Sound", fontsize=style["fontsize"]["title"])
# plt.legend(loc="lower left", fontsize=style["fontsize"]["legend"], framealpha=1)

plt.tight_layout()
plt.subplots_adjust(left=0.23, right=0.98, bottom=0.30, top=0.98)
plt.savefig("config_tradeStudy_plot_10_SoundPressureLevel.pdf")

# Data output (to screen and to text file)
outputs = [
    "Max takeoff mass",
    "Airframe mass",
    "Battery mass",
    "Mission time",
    "Flight time",
    "Charging time",
    "Purchase price",
    "Trip cost",
    "Cost per passenger-km",
]
output_units = [
    "kg",
    "kg",
    "kg",
    "minutes",
    "minutes",
    "minutes",
    "$US (thousands)",
    "dimensionless",
    "km**-1",
]
output_spaces = ["", "\t", "\t", "\t", "\t", "\t", "\t", "\t", ""]

outputs += [
    "Rotor diameter",
    "Tip speed",
    "Tip Mach number",
    "Thrust coefficient",
    "Power coefficient",
    "Figure of merit",
]
output_units += [
    "m",
    "m/s",
    "dimensionless",
    "dimensionless",
    "dimensionless",
    "dimensionless",
]
output_spaces += [
    "\t",
    "\t",
    "\t",
    "",
    "",
    "\t",
]

outputs += ["Hover SPL (unweighted)", "Hover SPL (A-weighted)", "Vortex peak frequency"]
output_units += ["dimensionless", "dimensionless", "turn/s"]
output_spaces += ["", "", ""]

output_string = "Tabulated Data by Configuration\n"
output_string += "\n"
output_string += "Configuration\t\t\t"
for config in configs:
    output_string += config
    output_string += "\t"

output_string += "Units\n"
output_string += "\n"

for i, output in enumerate(outputs):

    units = output_units[i]
    output_space = output_spaces[i]
    output_string += output + "\t\t" + output_space

    for j, config in enumerate(configs):

        solution = configs[config]["solution"]

        if output == "Max takeoff mass":
            var_string = "OnDemandAircraft.MTOM"
            precision = "%0.0f"

        elif output == "Airframe mass":
            var_string = "OnDemandAircraft.Airframe.m"
            precision = "%0.0f"

        elif output == "Battery mass":
            var_string = "OnDemandAircraft.Battery.m"
            precision = "%0.0f"

        elif output == "Mission time":
            var_string = "OnDemandRevenueMission.t_{mission}"
            precision = "%0.1f"

        elif output == "Flight time":
            var_string = "OnDemandRevenueMission.t_{flight}"
            precision = "%0.1f"

        elif output == "Charging time":
            var_string = "OnDemandRevenueMission.TimeOnGround.t_{segment}"
            precision = "%0.1f"

        elif output == "Trip cost":
            var_string = "cost_per_trip"
            precision = "%0.0f"

        elif output == "Cost per passenger-km":
            var_string = "cost_per_passenger_km"
            precision = "%0.2f"

        elif output == "Purchase price":
            var_strings = [
                "OnDemandAircraft.Airframe.purchase_price",
                "OnDemandAircraft.Avionics.purchase_price",
                "OnDemandAircraft.Battery.purchase_price",
            ]
            precision = "%0.0f"

            output_string += precision % (
                sum(solution(v) for v in var_strings).to(ureg.dimensionless).magnitude
                / 1e3
            )
            output_string += "\t\t"

            continue

        elif output == "Rotor diameter":
            var_string = "OnDemandAircraft.Rotors.D"
            precision = "%0.2f"

        elif output == "Combined area of all rotor disks":
            var_string = "OnDemandAircraft.Rotors.A_{total}"
            precision = "%0.1f"

        elif output == "Tip speed":
            var_string = "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.v_{tip}"
            precision = "%0.1f"

        elif output == "Tip Mach number":
            var_string = "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.M_{tip}"
            precision = "%0.2f"

        elif output == "Thrust coefficient":
            var_string = "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.CT"
            precision = "%0.4f"

        elif output == "Power coefficient":
            var_string = "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.CP"
            precision = "%0.4f"

        elif output == "Figure of merit":
            var_string = "OnDemandSizingMission.HoverTakeoff.OnDemandAircraftHoverPerformance.RotorsPerformance.FOM"
            precision = "%0.3f"

        elif output == "Hover SPL (unweighted)":

            precision = "%0.1f"

            output_string += precision % configs[config]["SPL"]
            output_string += "\t\t"

            continue

        elif output == "Hover SPL (A-weighted)":

            precision = "%0.1f"

            output_string += precision % configs[config]["SPL_A"]
            output_string += "\t\t"

            continue

        elif output == "Vortex peak frequency":

            precision = "%0.0f"

            output_string += (
                precision % configs[config]["f_{peak}"].to(ureg(units)).magnitude
            )
            output_string += "\t\t"

            continue

        output_string += precision % solution(var_string).to(ureg(units)).magnitude
        output_string += "\t\t"

    output_string += units + "\n"

print("\n\n")
print(output_string)

text_file = open("config_trade_study_tabulatedData.txt", "w")
text_file.write(output_string)
text_file.close()


"""
# Sound pressure level (in hover) 
plt.subplot(3,3,9)

for i, config in enumerate(configs):
	SPL_sizing   = configs[config]["SPL"]
	SPL_sizing_A = configs[config]["SPL_A"]

	if i==0:
		plt.bar(i-0.2, SPL_sizing,   width=style["bar_width_medium"], align='center', alpha=1, color=style["colors"][0], edgecolor='k', label="Unweighted")
		plt.bar(i+0.2, SPL_sizing_A, width=style["bar_width_medium"], align='center', alpha=1, color=style["colors"][2], edgecolor='k', label="A-weighted")
	else:
		plt.bar(i-0.2, SPL_sizing,   width=style["bar_width_medium"], align='center', alpha=1, color=style["colors"][0], edgecolor='k')
		plt.bar(i+0.2, SPL_sizing_A, width=style["bar_width_medium"], align='center', alpha=1, color=style["colors"][2], edgecolor='k')

SPL_req = 62
plt.plot([np.min(y_pos)-1, np.max(y_pos)+1], [SPL_req, SPL_req], color="black", linewidth=3, linestyle="--", label="62 dBA")
plt.xlim(xmin=np.min(y_pos)-1,xmax=np.max(y_pos)+1)
plt.ylim(ymin=51, ymax=77)
plt.grid()
plt.xticks(y_pos, labels,     fontsize=style["fontsize"]["xticks"], rotation=style["rotation"])
plt.yticks(                   fontsize=style["fontsize"]["yticks"])
plt.ylabel('SPL (dB)',        fontsize=style["fontsize"]["ylabel"])
plt.title("Hover Sound (sizing mission)",   fontsize=style["fontsize"]["title"])
plt.legend(loc="lower right", fontsize=style["fontsize"]["legend"], framealpha=1)
"""