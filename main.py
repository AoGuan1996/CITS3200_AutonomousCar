import time
from display import Display
from vision import Vision
from agent import Agent
from world import World
from zenwheels.comms import CarCommunicator


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

	# Initialise car comms.
	comms = CarCommunicator()

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
		print(msgHeader+"Passing map "+scenario_config["Map"]["Name"]+" to world")
		world = World(agents, vehicles, scenario_config["Map"]["Image"], scenario_config["Map"]["Waypoints"])

		# Main loop.
		print(msgHeader + "Entering main loop.")
		while True:
			display.update(world.get_world_data())
			if display.done:
				break

			for agent in agents:
				agent.update_world_knowledge(world.get_world_data())
		print(msgHeader + "Exited main loop.")

		# Stop agents.
		print(msgHeader + "Stopping agents.")
		for agent in agents:
			agent.stop()

		print(msgHeader + "Exiting scenario.")

	print(msgHeader + "Exiting simulator.")

