# Sweep to evaluate the sensitivity of each design to battery energy density

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import numpy as np
from gpkit import Model, ureg
from matplotlib import pyplot as plt
from aircraft_models import OnDemandAircraft 
from aircraft_models import OnDemandSizingMission, OnDemandRevenueMission
from aircraft_models import OnDemandDeadheadMission, OnDemandMissionCost
from study_input_data import generic_data, configuration_data

#General data
eta_cruise = generic_data["\eta_{cruise}"] 
eta_electric = generic_data["\eta_{electric}"]
weight_fraction = generic_data["weight_fraction"]
C_m = generic_data["C_m"]
n = generic_data["n"]

reserve_type = generic_data["reserve_type"]
autonomousEnabled = generic_data["autonomousEnabled"]
charger_power = generic_data["charger_power"]

vehicle_cost_per_weight = generic_data["vehicle_cost_per_weight"]
battery_cost_per_C = generic_data["battery_cost_per_C"]
pilot_wrap_rate = generic_data["pilot_wrap_rate"]
mechanic_wrap_rate = generic_data["mechanic_wrap_rate"]
MMH_FH = generic_data["MMH_FH"]
deadhead_ratio = generic_data["deadhead_ratio"]

sizing_mission_type = generic_data["sizing_mission"]["type"]
sizing_N_passengers = generic_data["sizing_mission"]["N_passengers"]
sizing_mission_range = generic_data["sizing_mission"]["range"]
sizing_time_in_hover = generic_data["sizing_mission"]["time_in_hover"]

revenue_mission_type = generic_data["revenue_mission"]["type"]
revenue_N_passengers = generic_data["revenue_mission"]["N_passengers"]
revenue_mission_range = generic_data["revenue_mission"]["range"]
revenue_time_in_hover = generic_data["revenue_mission"]["time_in_hover"]

deadhead_mission_type = generic_data["deadhead_mission"]["type"]
deadhead_N_passengers = generic_data["deadhead_mission"]["N_passengers"]
deadhead_mission_range = generic_data["deadhead_mission"]["range"]
deadhead_time_in_hover = generic_data["deadhead_mission"]["time_in_hover"]

# Delete certain configurations
configs = configuration_data.copy()
del configs["Tilt duct"]
del configs["Multirotor"]
del configs["Autogyro"]

#Optimize remaining configurations
for config in configs:

	print "Solving configuration: " + config

	#set up C_m arrays (different for each configuration)
	if config == "Helicopter":
		C_m = np.linspace(350,600,10)*ureg.Wh/ureg.kg
	elif config == "Coaxial heli":
		C_m = np.linspace(300,600,11)*ureg.Wh/ureg.kg
	elif config == "Lift + cruise":
		C_m = np.linspace(250,600,13)*ureg.Wh/ureg.kg
	else:
		C_m = np.linspace(200,600,15)*ureg.Wh/ureg.kg

	C_m = ("sweep",C_m)

	c = configs[config]

	V_cruise = c["V_{cruise}"]
	V_loiter = V_cruise #approximation
	L_D = c["L/D"]
	T_A = c["T/A"]
	Cl_mean_max = c["Cl_{mean_{max}}"]
	N = c["N"]

	Aircraft = OnDemandAircraft(N=N,L_D=L_D,eta_cruise=eta_cruise,C_m=C_m,
		Cl_mean_max=Cl_mean_max,weight_fraction=weight_fraction,n=n,eta_electric=eta_electric,
		cost_per_weight=vehicle_cost_per_weight,cost_per_C=battery_cost_per_C,
		autonomousEnabled=autonomousEnabled)

	SizingMission = OnDemandSizingMission(Aircraft,mission_range=sizing_mission_range,
		V_cruise=V_cruise,V_loiter=V_loiter,N_passengers=sizing_N_passengers,
		time_in_hover=sizing_time_in_hover,reserve_type=reserve_type,
		mission_type=sizing_mission_type)
	SizingMission.substitutions.update({SizingMission.fs0.topvar("T/A"):T_A})

	RevenueMission = OnDemandRevenueMission(Aircraft,mission_range=revenue_mission_range,
		V_cruise=V_cruise,N_passengers=revenue_N_passengers,time_in_hover=revenue_time_in_hover,
		charger_power=charger_power,mission_type=revenue_mission_type)

	DeadheadMission = OnDemandDeadheadMission(Aircraft,mission_range=deadhead_mission_range,
		V_cruise=V_cruise,N_passengers=deadhead_N_passengers,time_in_hover=deadhead_time_in_hover,
		charger_power=charger_power,mission_type=deadhead_mission_type)

	MissionCost = OnDemandMissionCost(Aircraft,RevenueMission,DeadheadMission,
		pilot_wrap_rate=pilot_wrap_rate,mechanic_wrap_rate=mechanic_wrap_rate,MMH_FH=MMH_FH,\
		deadhead_ratio=deadhead_ratio)

	problem = Model(MissionCost["cost_per_trip"],
		[Aircraft, SizingMission, RevenueMission, DeadheadMission, MissionCost])

	solution = problem.solve(verbosity=0)

	configs[config]["solution"] = solution

	configs[config]["C_m_array"] = solution("C_m_OnDemandAircraft/Battery")

	configs[config]["MTOW"] = solution("MTOW_OnDemandAircraft")
	configs[config]["W_{battery}"] = solution("W_OnDemandAircraft/Battery")
	configs[config]["cost_per_trip_per_passenger"] = solution("cost_per_trip_per_passenger_OnDemandMissionCost")
	configs[config]["SPL"] = 20*np.log10(solution("p_{ratio}_OnDemandSizingMission"))
		

# Plotting commands
plt.ion()
fig1 = plt.figure(figsize=(17,11), dpi=80)
plt.show()

style = {}
style["linestyle"] = ["-","-","-","-","--","--","--","--"]
style["marker"] = ["s","o","^","v","s","o","^","v"]
style["fillstyle"] = ["full","full","full","full","none","none","none","none"]
style["markersize"] = 10

C_m = C_m[1] #convert back to array from tuple

#Maximum takeoff weight
plt.subplot(2,2,1)
for i, config in enumerate(configs):
	c = configs[config]
	plt.plot(c["C_m_array"].to(ureg.Wh/ureg.kg).magnitude,c["MTOW"].to(ureg.lbf).magnitude,
		color="black",linewidth=1.5,linestyle=style["linestyle"][i],marker=style["marker"][i],
		fillstyle=style["fillstyle"][i],markersize=style["markersize"],label=config)
plt.grid()
plt.ylim(ymin=0)
plt.xlabel('Battery energy density (Wh/kg)', fontsize = 16)
plt.ylabel('Weight (lbf)', fontsize = 16)
plt.title("Maximum Takeoff Weight",fontsize = 20)
plt.legend(numpoints = 1,loc='upper right', fontsize = 12)

#Battery weight
plt.subplot(2,2,2)
for i, config in enumerate(configs):
	c = configs[config]
	plt.plot(c["C_m_array"].to(ureg.Wh/ureg.kg).magnitude,c["W_{battery}"].to(ureg.lbf).magnitude,
		color="black",linewidth=1.5,linestyle=style["linestyle"][i],marker=style["marker"][i],
		fillstyle=style["fillstyle"][i],markersize=style["markersize"],label=config)
plt.grid()
plt.ylim(ymin=0)
plt.xlabel('Battery energy density (Wh/kg)', fontsize = 16)
plt.ylabel('Weight (lbf)', fontsize = 16)
plt.title("Battery Weight",fontsize = 20)
plt.legend(numpoints = 1,loc='upper right', fontsize = 12)

#Trip cost per passenger
plt.subplot(2,2,3)
for i, config in enumerate(configs):
	c = configs[config]
	plt.plot(c["C_m_array"].to(ureg.Wh/ureg.kg).magnitude,c["cost_per_trip_per_passenger"],
		color="black",linewidth=1.5,linestyle=style["linestyle"][i],marker=style["marker"][i],
		fillstyle=style["fillstyle"][i],markersize=style["markersize"],label=config)
plt.grid()
plt.ylim(ymin=0)
plt.xlabel('Battery energy density (Wh/kg)', fontsize = 16)
plt.ylabel('Cost ($US)', fontsize = 16)
plt.title("Cost per Trip, per Passenger",fontsize = 20)
plt.legend(numpoints = 1,loc='upper right', fontsize = 12)

#Sound pressure level (in hover)
plt.subplot(2,2,4)
for i, config in enumerate(configs):
	c = configs[config]
	plt.plot(c["C_m_array"].to(ureg.Wh/ureg.kg).magnitude,c["SPL"],
		color="black",linewidth=1.5,linestyle=style["linestyle"][i],marker=style["marker"][i],
		fillstyle=style["fillstyle"][i],markersize=style["markersize"],label=config)
plt.grid()
plt.xlabel('Battery energy density (Wh/kg)', fontsize = 16)
plt.ylabel('SPL (dB)', fontsize = 16)
plt.title("Sound Pressure Level in Hover (sizing mission)",fontsize = 20)
plt.legend(numpoints = 1,loc='upper right', fontsize = 12)


if reserve_type == "FAA":
	num = solution["constants"]["t_{loiter}_OnDemandSizingMission"].to(ureg.minute).magnitude
	reserve_type_string = " (%0.0f-minute loiter time)" % num
if reserve_type == "Uber":
	num = solution["constants"]["R_{divert}_OnDemandSizingMission"].to(ureg.nautical_mile).magnitude
	reserve_type_string = " (%0.0f-nm diversion distance)" % num

if autonomousEnabled:
	autonomy_string = "autonomy enabled"
else:
	autonomy_string = "pilot required"

title_str = "Aircraft parameters: structural mass fraction = %0.2f; %s\n" \
	% (weight_fraction, autonomy_string) \
	+ "Sizing mission (%s): range = %0.0f nm; %0.0f passengers; %0.0fs hover time; reserve type = " \
	% (sizing_mission_type, sizing_mission_range.to(ureg.nautical_mile).magnitude, sizing_N_passengers, sizing_time_in_hover.to(ureg.s).magnitude) \
	+ reserve_type + reserve_type_string + "\n"\
	+ "Revenue mission (%s): range = %0.0f nm; %0.1f passengers; %0.0fs hover time; no reserve; charger power = %0.0f kW\n" \
	% (revenue_mission_type, revenue_mission_range.to(ureg.nautical_mile).magnitude, \
		revenue_N_passengers, revenue_time_in_hover.to(ureg.s).magnitude, charger_power.to(ureg.kW).magnitude) \
	+ "Deadhead mission (%s): range = %0.0f nm; %0.1f passengers; %0.0fs hover time; no reserve; deadhead ratio = %0.1f" \
	% (deadhead_mission_type, deadhead_mission_range.to(ureg.nautical_mile).magnitude, \
		deadhead_N_passengers, deadhead_time_in_hover.to(ureg.s).magnitude, deadhead_ratio)

plt.suptitle(title_str,fontsize = 16)

plt.tight_layout()#makes sure subplots are spaced neatly
plt.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.86)#adds space at the top for the title
