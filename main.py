import time
from display import Display
from vision import Vision
from agent import Agent
from world import World
import datetime


if __name__ == "__main__":
	msgHeader = "[MAIN]: "

	print("")
	print("========================================")
	print("         TABLETOP CAR SIMULATOR         ")
	print("========================================")
	print("")

	# Initialise display.
	display = Display()
	# Display splash screen.
	display.splash_screen()

	# Calibrate once at the beginning.
	display.calibration_screen()
	time.sleep(2)

	while True:
		display.done = False

		# Menu.
		scenario_config = display.menu()
		if not scenario_config:
			break

		# Scenario initialisation.
		agents = []
		vehicles = []
		for car_parameters in scenario_config["Active Cars"]:
			agent = Agent(car_parameters["ID"], agentType=car_parameters["Type"],
						  vehicleType=car_parameters["Vehicle"], strategyFile=car_parameters["Strategy"])
			agents.append(agent)
			vehicles.append(agent.vehicle)
		if not agents:
			errorMsg = msgHeader + "No cars enabled."
			print(errorMsg)
			display.error_message(errorMsg)
			time.sleep(2)
			continue
			
		world = World(agents, vehicles, scenario_config["Map"]["Image"], scenario_config["Map"]["Waypoints"])

		# Main loop.
		print(msgHeader + "Entering main loop.")
		dt = datetime.datetime(2019, 1, 1)
		dt_time = dt.now().time()
		start_time = datetime.timedelta(seconds=dt_time.second, milliseconds=dt_time.microsecond/1000, 
										minutes=dt_time.minute, hours=dt_time.hour)
		laps = []
		laps.append(start_time)
		while True:
			if display.lap:
				dt_time = dt.now().time()
				current_time = datetime.timedelta(seconds=dt_time.second, milliseconds=dt_time.microsecond/1000, 
										minutes=dt_time.minute, hours=dt_time.hour)
				laps.append(current_time - start_time)
			display.lap = False
			display.update(world.get_world_data(), laps)
			if display.done:
				break
			
			if display.race_complete:
				######## Do something when the race is finished - e.g. splash screen showing lap times, leaderboard, etc. #########
				pass
				
			for agent in agents:
				agent.update_world_knowledge(world.get_world_data())
		print(msgHeader + "Exited main loop.")

		# Stop agents.
		print(msgHeader + "Stopping agents.")
		for agent in agents:
			agent.stop()

		print(msgHeader + "Exiting scenario.")

	print(msgHeader + "Exiting simulator.")

