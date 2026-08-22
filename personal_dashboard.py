from BASE_MAP import BASE_MAP
import json



def print_personal_dashboard():

    personal_map = BASE_MAP.copy()

    with open("user_config.json", "r") as json_file:
        selected_stations = json.load(json_file)

    for station in selected_stations:

        row = station["row"]
        col = station["col"]
        num = station["symbol"]
        personal_map[row] = personal_map[row][:col] + num + personal_map[row][col+1:]


    for row in personal_map:
        print(row)


if __name__  == "__main__":
    print_personal_dashboard()
