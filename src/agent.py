from langchain.agents import create_agent
import requests
import time

# Create functions that will act as tools for the agent


def get_train_lines_in_nyc():
    """Get the train lines in NYC."""
    response = requests.get("https://demo.transiter.dev/systems/us-ny-subway/routes")
    result = response.json()
    route_names = [route["id"] for route in result["routes"]]
    return route_names


def get_stops_on_a_train_line(train_line):
    """Given a train line, return the stops on that line.
    It returns only a list of stop names for the given train line."""
    response = requests.get(
        f"https://demo.transiter.dev/systems/us-ny-subway/routes/{train_line}"
    )
    result = response.json()
    for service_map in result["serviceMaps"]:
        if service_map["configId"] == "realtime":
            route_stops = [stop["name"] for stop in service_map["stops"]]
            return route_stops
    return []


def get_stop_id_for_stop_name(train_line, stop_name):
    """Given a train line and a stop name, return the stop ID.
    It returns the stop ID for the given stop name on the given train line.
    Use this to find the ID whenever you need a stop ID to call a specific fucntion"""
    response = requests.get(
        f"https://demo.transiter.dev/systems/us-ny-subway/routes/{train_line}"
    )
    result = response.json()
    for service_map in result["serviceMaps"]:
        if service_map["configId"] == "realtime":
            stop_ids = [
                stop["id"] for stop in service_map["stops"] if stop["name"] == stop_name
            ]
            if stop_ids:
                return stop_ids[0]
    return None


def get_train_timings_for_stop_id(stop_id):
    """Given a stop ID, return the train timings for that stop.
    The timings are returned as a list of dictionaries, where each dictionary contains the trip ID, headsign, and arrival time in minutes."""
    response = requests.get(f"https://demo.transiter.dev/systems/us-ny-subway/stops/{stop_id}")
    result = response.json()
    stop_times = result['stopTimes']
    timings = "trip_id,train,headsign,arrival_time_in_mins\n"
    for stoptime in stop_times:
        trip = stoptime['trip']['id']
        train = stoptime['trip']['route']['id']
        headsign = stoptime['headsign']
        arrival_time_epoch = float(stoptime['arrival']['time'])
        arrival_time_in_mins = int((arrival_time_epoch - time.time()) // 60)
        if arrival_time_in_mins >= 0 and arrival_time_in_mins < 30:  # Only include upcoming trains within 100 minutes
            timings += f"{trip},{train},{headsign},{arrival_time_in_mins}\n"
    return timings


def get_timings_for_train_trip(train_line, trip_id):
    """Given a train line and a trip ID, return the timings for that train trip.
    The timings are returned as a list of dictionaries, where each dictionary contains the stop name, arrival time in minutes, and arrival time formatted as HH:MM AM/PM.
    """
    response = requests.get(
        f"https://demo.transiter.dev/systems/us-ny-subway/routes/{train_line}/trips/{trip_id}"
    )
    result = response.json()
    timings = "stop_name,arrival_time_in_mins,arrival_time_formatted\n"
    for stoptime in result["stopTimes"]:
        stop_name = stoptime["stop"]["name"]
        arrival_time_epoch = float(stoptime["arrival"]["time"])
        arrival_time_in_mins = int((arrival_time_epoch - time.time()) // 60)
        arrival_time_hh_mm = time.strftime(
            "%I:%M %p", time.localtime(arrival_time_epoch)
        )
        timings += f"{stop_name},{arrival_time_in_mins},{arrival_time_hh_mm}\n"
    return timings


# Create a system prompt describing the agent's role and set guidelines for using the tools

system_prompt = """
You are a helpful assistant that provides information about the NYC subway system such as train timings, stops, and routes.

<tools>
Use the following tools to answer questions about the NYC subway system:

- get_train_lines_in_nyc()
- get_stops_on_a_train_line(train_line)
- get_stop_id_for_stop_name(train_line, stop_name)
- get_train_timings_for_stop_id(stop_id)
- get_timings_for_train_trip(train_line, trip_id)

The given tools are sufficient to answer any question about arrival and departure timings for trains at any stop in the NYC subway system, as well as the stops on any train line. Always use the tools to get the information you need to answer the user's question, and never assume information.
</tools>

<restrictions>
- NEVER Return trip ids to the user, as they are not meaningful to the user.
- NEVER Assume information.
- NEVER Use your own knowledge of NYC locations, and always use the tools to get the information you need to answer the user's question.
</restrictions>

<example_user_inputs_and_expected_actions>
- When is the next F train arriving at Jay St-MetroTech?
The user gave you a train line and a stop name, so you can use the get_stop_id_for_stop_name tool to get the stop ID for Jay St-MetroTech on the F train line, and then use the get_train_timings_for_stop_id tool to get the timings for that stop ID. Then list 3 most recent trains for each direction.

- When will the next Manhattan train at Jay St-MetroTech arrive at west 4th street?
You might want to confirm which train line the user is referring to. Then find the stop ID for Jay St-MetroTech on that train line, and then find the timings for that stop ID. Once you have the timings, you might want to use that trip ID to find the timings for that train trip, and then figure out when it will arrive at west 4th street.

- I'll take the F train from Jay St-MetroTech to west 4th street, when should I get on the train?
You should confirm how long does it take the user to get to the platform, and factor that into your answer. Also ask when they are planning to leave, and factor that into your answer as well.
</example_user_inputs_and_expected_actions>

<final_instruction>
Always think step by step about which tool(s) you need to use to answer the question,and then call the tool(s) with the appropriate arguments. If you need to use multiple tools, you can call them sequentially, using the output of one tool as the input to another tool if necessary. Always make sure to provide a final answer to the user's question after using the tools.
</final_instruction>
"""

# Build the agent by providing the model, tools, and system prompt

agent = create_agent(
    model="groq:qwen/qwen3-32b",
    tools=[
        get_train_lines_in_nyc,
        get_stops_on_a_train_line,
        get_stop_id_for_stop_name,
        get_train_timings_for_stop_id,
        get_timings_for_train_trip,
    ],
    system_prompt=system_prompt,
)
