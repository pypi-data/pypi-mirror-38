import xml.etree.ElementTree as ET
import os
from tkinter import *
from tkinter import filedialog
from terminaltables import AsciiTable
import datetime
import requests
from pytz import timezone, utc
import csv

start = 0
end = 0
csv_filename = ''


def main():
    config = read_config()

    config["timezone"] = get_station_timezone(config)

    station_timezone = timezone(config["timezone"])

    csv_file = []
    with open(config["csv_filename"]) as file:
        r = csv.reader(file)
        for row in r:
            csv_file.append(row)
    # first row is headers, so initialise index at 1
    index = 1

    start = config['start']
    config["start"] = datetime.datetime(start.year, start.month, start.day, start.hour, start.minute, 0, tzinfo=station_timezone)

    end = config['end']
    config["end"] = datetime.datetime(end.year, end.month, end.day, end.hour, end.minute, 0, tzinfo=station_timezone)

    nr_logs, config['station_id'] = check_database_range_empty(config)
    if nr_logs > 0:
        print("There already are " + str(nr_logs) + " points stored between the requested CSV range")
        exit()

    display_config(config)

    while True:
        table_data = [["Server", "Station"], [config["host"], config["station_id"]]]
        table = AsciiTable(table_data)
        table.title = f_blue(" Station Info ")
        print("======================================================================================\n")

        print(table.table)

        if index >= len(csv_file):
            print('Done')
            return True

        # second column represents the time
        sample_time = datetime.datetime.strptime(csv_file[index][1], "%Y/%m/%d %H:%M:%S")
        local_timestamp = datetime.datetime(sample_time.year, sample_time.month, sample_time.day, sample_time.hour,
                                            sample_time.minute, 0, tzinfo=utc)
        local_timestamp = local_timestamp.astimezone(station_timezone)

        if (local_timestamp - config['start']).total_seconds() + 60 > 0 and (
                config['end'] - local_timestamp).total_seconds() >= 0:
            sample = create_sample_csv(local_timestamp, csv_file[index])
        else:
            sample = None

        index += 1
        print('Current index: ' + str(index))

        if sample:
            display_sample(sample)

            response = post_sample(sample, config)
            print(response)

            response = post_status(config)
            print(response)


def check_database_range_empty(config):
    url = "https://{0}/api/Poll/checkRange?X-API-KEY={1}&serial_number={2}&start={3}&end={4}"\
        .format(config["host"], config['X-API-KEY'], config["serial"],
                config["start"].strftime('%Y/%m/%d %H:%M:%S'), config["end"].strftime('%Y/%m/%d %H:%M:%S'))
    headers = {'content-type': "application/x-www-form-urlencoded", 'Accept': "application/json"}

    response = requests.request("GET", url, headers=headers, verify=False)
    nr_logs = int(response.json()['nr_logs'])
    station_id = response.json()['station_id']

    return nr_logs, station_id


def get_station_timezone(config):
    url = "https://{0}/api/Time/zone?X-API-KEY={1}&serial_number={2}"\
        .format(config["host"], config['X-API-KEY'], config["serial"])
    headers = {'content-type': "application/x-www-form-urlencoded", 'Accept': "application/json"}

    response = requests.request("GET", url, headers=headers, verify=False)
    tz = response.json()['timezone']

    return tz


def post_sample(sample, config):

    url = "https://{0}/api/poll".format(config["host"])
    headers = {'content-type': "application/x-www-form-urlencoded"}

    payload = 	 "X-API-KEY={0}" \
                 "&serial_number={1}" \
                 "&leq={2:.2f}" \
                 "&lmax={3:.2f}" \
                 "&lmin={4:.2f}" \
                 "&le={5:.2f}" \
                 "&ln1={6:.2f}" \
                 "&ln2={7:.2f}" \
                 "&ln3={8:.2f}" \
                 "&ln4={9:.2f}" \
                 "&ln5={10:.2f}" \
                 "&timestamp={11}" \
                 "&sd_card={12}" \
                 "&battery={13}" \
                 "&measuring={14}" \
                 "&charging={15}" \
                 "&system_error={16}" \
                 "&lp={17}" \
                 "&apv=0" \
                 "&lp_sub={18}" \
                 "&overload={19}" \
                 "&underrange={20}".format(config["X-API-KEY"], config["serial"], sample["leq"], sample["lmax"], sample["lmin"], sample["le"],
                                           sample["ln1"], sample["ln2"], sample["ln3"], sample["ln4"], sample["ln5"], sample["timestamp"].strftime('%Y/%m/%d %H:%M:%S'),
                                           sample["sd_card"], sample["battery"], sample["measuring"], sample["charging"], sample["system_error"],
                                           sample["lp"], sample["lp_sub"], sample["overload"], sample["underrange"])

    print(f_blue("\nPost payload:"))
    print(payload)
    print("\n")

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    return response.text


def post_status(config):
    url = "https://{0}/api/status".format(config["host"])
    headers = {'content-type': "application/x-www-form-urlencoded"}

    data = {}

    data["X-API-KEY"] = config["X-API-KEY"]
    data["serial_number"] = config["serial"]
    data["sdcard"] = 27
    data["battery"] = 96.3
    data["measuring"] = 1
    data["mounted"] = 1
    data["charging"] = 13
    data["system_error"] = 0

    response = requests.request("POST", url, data=data, headers=headers, verify=False)
    return response.text


def display_sample(sample):
    data = [["Item", "Value"]]

    for key, value in sample.items():
        data.append([key, value])

    table = AsciiTable(data)
    table.title = f_blue(" Sample ")

    print("\n")
    print(table.table)



def create_sample_csv(timestamp, csv_row):
    if csv_row is None:
        return sys.exit(0)

    sample = {
        "leq": float(csv_row[3]),
        "lmax": float(csv_row[5]),
        "lmin": float(csv_row[6]),
        "le": float(csv_row[4]),
        "ln1": float(csv_row[8]),
        "ln2": float(csv_row[9]),
        "ln3": float(csv_row[10]),
        "ln4": float(csv_row[11]),
        "ln5": float(csv_row[12]),
        "timestamp": timestamp,
        "sd_card": 100,
        "battery": 6,
        "measuring": 1,
        "charging": 13.5,
        "system_error": 0,
        "lp": 0,
        "lp_sub": 0,
        "overload": 0,
        "underrange": 0
    }

    return sample


def read_config():
    config = {}

    if os.path.isfile('config.xml') is False:
        print('No config.xml file found')
        exit()

    tree = ET.parse('config.xml')
    root = tree.getroot()[0]
    for child in root:
        for child2 in child:
            if len(child2.tag) > 1:
                config[child2.tag] = child2.text

    get_range()
    global start, end, csv_filename

    try:
        config['start'] = datetime.datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
        config['end'] = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M:%S")
    except:
        print('Invalid format for start/end date')
        exit()

    if config['start'] is False or config['end'] is False:
        print('Invalid format for start/end date')
        exit()

    if (config['start'] - config['end']).total_seconds() >= 0:
        print('Start date bigger than end date')
        exit()

    if not os.path.isfile(csv_filename):
        print('Invalid rnd/csv file selected')
        exit()

    config['csv_filename'] = csv_filename

    return config


def get_range():
    root = Tk()
    root.geometry("300x150")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = Window(root)
    root.mainloop()


def on_closing():
    exit()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("RND upload")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        quitButton = Button(self, text="Quit", command=self.exit_program)
        submitButton = Button(self, text="Submit", command=self.read_range)

        self.range_start = Text(self, height=1, width=19)
        self.range_end = Text(self, height=1, width=19)

        self.range_start.insert("1.0", (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y/%m/%d %H:%M:%S"))
        self.range_end.insert("1.0", datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

        start_label = Label(self, text='Start')
        end_label = Label(self, text='End')

        browseButton = Button(self, text="Browse", command=self.browse_file)

        # placing stuff on my window
        submitButton.place(x=2, y=2)
        quitButton.place(x=240, y=2)
        start_label.place(x=1, y=50)
        end_label.place(x=160, y=50)
        self.range_start.place(x=1, y=70)
        self.range_end.place(x=160, y=70)
        browseButton.place(x=2, y=120)

    def exit_program(self):
        exit()

    def read_range(self):
        global start, end
        start = self.range_start.get("1.0", END)
        start = start[:19]
        self.range_start.insert("1.0", start)
        end = self.range_end.get("1.0", END)
        end = end[:19]
        self.range_end.insert("1.0", end)
        self.master.destroy()

    def browse_file(self):
        global csv_filename
        csv_filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("rnd files", "*.rnd"), ("csv files", "*.csv")))
        if len(csv_filename.split("/")) > 1:
            file_label = Label(self, text=csv_filename.split("/")[-1])
        else:
            file_label = Label(self, text=csv_filename.split("\\")[-1])
        file_label.place(x=80, y=125)


def display_config(config):
    data = [["Item", "Value"]]

    for key, value in config.items():
        data.append([key, value])

    table = AsciiTable(data)
    table.title = f_blue(" Configuration ")

    print("\n")
    print(table.table)


def f_blue(line):
    return "{0}{1}{2}".format(bcolors.OKBLUE, line, bcolors.ENDC)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    main()
