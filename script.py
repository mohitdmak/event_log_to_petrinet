import sys
import pm4py
import subprocess
import pandas as pd 
from pathlib import Path
from pm4py.utils import EventLog


class LogFileToNets:
    LIB_SIMULATION_EXC = "AutomaticProcessSimulation/simulation.py"
    DEFAULT_SIMULATION_LOGS = "simulated-logs.csv"

    def __init__(self) -> None:
        print("Starting Event log to Petri Nets driver . . .")

    def run(self):
        print("Do you want to generate simulated CSV file from custom Log File? (y for Yes, else proceed)")
        res = str(input())
        if res == 'y':
            return self.net_generation_custom_log_file()
        else:
            return self.direct_net_generation()

    def net_generation_custom_log_file(self):
        print("Please write relative/absolute location of your Custom Log File > > >")
        file_path = str(input())
        print(f"< < < File Path recieved: {file_path}")
        file = Path(file_path)
        if not file.exists():
            raise FileExistsError(f"Given File: `{file}` does not exist < < <") 
        else:
            print(f"Given File: `{file}` exists...")
            command = f"python {self.LIB_SIMULATION_EXC} {file}"
            # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            process = subprocess.Popen(command.split())
            output, error = process.communicate()
            if not error:
                print(f"Simulated Log file created successfully at: `{self.DEFAULT_SIMULATION_LOGS}` < < <")
                logs = self.read_csv(Path(self.DEFAULT_SIMULATION_LOGS))
                self.direct_net_generation(logs)
                return
            else:
                print(error)
                raise Exception("ERROR: Could not generate simulated csv log file from your custom file < < <")

    def direct_net_generation(self, logs: EventLog | pd.DataFrame | None = None):
        if not logs:
            logs, file_name = self.get_logs_from_log_file()
        net_type = -1
        get_net = None
        generate_net = {0: self.create_process_graph, 1: self.create_dmg, 2: self.create_heuristics_net, 3: self.create_petri_net}
        print("Please denote the type of Petri Net to generate ('0' for Process Graph, '1' for DMG, '2' for Heuristics Net, '3' for Petri Net) > > >")
        while net_type not in generate_net:
            try:
                net_type = int(input())
                get_net = generate_net[net_type]
                if net_type == 3:
                    net, initial_marking, final_marking = self.create_petri_net(logs)
                    pm4py.write_pnml(net, initial_marking, final_marking, f"{file_name}_petri.pnml")
                    print("Petri net PNML format written < < <")
                    return
                print(f"< < < Net Type recieved: {generate_net[net_type]}")
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("Please enter '0' or '1' or '2' only...")
        print("Generating Petri Net > > >")
        return get_net(logs) # pyright: ignore

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
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("Please enter '0' or '1' only, as only xes/csv file formats are supported...")
        print("Please write relative/absolute location of Log File input > > >")
        file_path = str(input())
        print(f"< < < File Path recieved: {file_path}")
        file = Path(file_path)
        if not file.exists():
            raise FileExistsError(f"Given File: `{file}` does not exist < < <") 
        else:
            print(f"Given File: `{file}` exists...")
            logs = get_logs(file) # pyright: ignore
            return logs, file

    def create_petri_net(self, log: EventLog | pd.DataFrame):
        print("> > > Creating Petri Net...")
        try:
            # process_tree = pm4py.discover_tree_inductive(log)  # DEPRECIATED
            process_tree = pm4py.discover_process_tree_inductive(log)
            print(process_tree)
            print("Storing Process Tree > > >")
            pm4py.write_ptml(process_tree, "tree.ptml")
            print("Stored Process Tree < < <")
            net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)
            # pm4py.view_bpmn(bpmn_model)
            print("Petri Net created < < <")
            pm4py.view_process_tree(process_tree)
            return (net, initial_marking, final_marking)
        except:
            print("ERROR: Could not create Process Graph < < <")

    def create_process_graph(self, log: EventLog | pd.DataFrame):
        print("> > > Creating Process Graph...")
        try:
            # process_tree = pm4py.discover_tree_inductive(log)  # DEPRECIATED
            process_tree = pm4py.discover_process_tree_inductive(log)
            print(process_tree)
            bpmn_model = pm4py.convert_to_bpmn(process_tree)
            print("BPMB\n\n")
            print(bpmn_model)
            pm4py.view_bpmn(bpmn_model)
            print("Process Graph created < < <")
            return process_tree
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
    driver.run()
