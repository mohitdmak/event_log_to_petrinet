import pm4py
import pandas as pd 
from pathlib import Path
from pm4py.utils import EventLog


class LogFileToNets:
    def __init__(self) -> None:
        print("Starting Event log to Petri Nets driver . . .")
        logs = self.get_logs_from_log_file()
        net_type = -1
        get_net = None
        generate_net = {0: self.create_process_graph, 1: self.create_dmg, 2: self.create_heuristics_net}
        print("Please denote the type of Petri Net to generate ('0' for Process Graph, '1' for DMG, '2' for Heuristics Net) > > >")
        while net_type not in generate_net:
            try:
                net_type = int(input())
                get_net = generate_net[net_type]
                print(f"< < < Net Type recieved: {generate_net[net_type]}")
            except:
                print("Please enter '0' or '1' or '2' only...")
        print("Generating Petri Net > > >")
        get_net(logs) # pyright: ignore

    def get_logs_from_log_file(self):
        get_logs = None
        file_type = {0: "XES", 1: "CSV"}
        getting_log_wrapper = {0: self.read_xes, 1: self.read_csv}
        file_type_inp = -1
        print("Please denote the Log File extension type ('0' for .xes, '1' for .csv) > > >")
        while file_type_inp not in file_type:
            try:
                file_type_inp = int(input())
                get_logs = getting_log_wrapper[file_type_inp]
                print(f"< < < File Type recieved: {file_type[file_type_inp]}")
            except:
                print("Please enter '0' or '1' only, as only xes/csv file formats are supported...")
        print("Please write absolute location of Log File input > > >")
        file_path = str(input())
        print(f"< < < File Path recieved: {file_path}")
        file = Path(file_path)
        if not file.exists():
            raise FileExistsError(f"Given File: `{file}` does not exist < < <") 
        else:
            print(f"Given File: `{file}` exists...")
            logs = get_logs(file) # pyright: ignore
            return logs

    def create_process_graph(self, log: EventLog | pd.DataFrame):
        print("> > > Creating Process Graph...")
        try:
            # process_tree = pm4py.discover_tree_inductive(log)  # DEPRECIATED
            process_tree = pm4py.discover_process_tree_inductive(log)
            bpmn_model = pm4py.convert_to_bpmn(process_tree)
            pm4py.view_bpmn(bpmn_model)
            print("Process Graph created < < <")
        except:
            print("ERROR: Could not create Process Graph < < <")

    def create_dmg(self, log: EventLog | pd.DataFrame):
        print("> > > Creating DMG...")
        try:
            dfg, start_activities, end_activities = pm4py.discover_dfg(log)
            pm4py.view_dfg(dfg, start_activities, end_activities)
            print("DMG created < < <")
        except:
            print("ERROR: Could not create DMG < < <")

    def create_heuristics_net(self, log: EventLog | pd.DataFrame):
        print("> > > Creating Heuristics Net...")
        try:
            map = pm4py.discover_heuristics_net(log)
            pm4py.view_heuristics_net(map)
            print("Heuristics Net created < < <")
        except:
            print("ERROR: Could not create Heuristics Net < < <")

    def read_xes(self, file: Path):
        print("> > > Parsing XES LOGS...")
        try:
            log = pm4py.read_xes(str(file))
            print("XES logs parsed < < <")
            return log
        except:
            print("ERROR: Could not read XES logs, probably the file is not of XES type < < <")
            return None

    def read_csv(self, file: Path):
        print("> > > Parsing CSV LOGS...")
        try:
            pd_dataframe = pd.read_csv(file)
            #dataframe = pm4py.format_dataframe(pd_dataframe, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
            dataframe = pm4py.format_dataframe(pd_dataframe, case_id='case_id', activity_key='activity', timestamp_key='time:timestamp')
            event_log = pm4py.convert_to_event_log(dataframe)
            print("CSV logs parsed < < <")
            return event_log
        except:
            print("ERROR: Could not read CSV logs, probably the file is not of CSV type < < <")
            return None


if __name__ == "__main__":
    driver = LogFileToNets()
