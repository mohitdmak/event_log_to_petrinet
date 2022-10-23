import pandas as pd 
import pm4py

XES_FILE = "AutomaticProcessSimulation/running-example.xes"
CSV_FILE = "AutomaticProcessSimulation/simulated-logs.csv"

def create_process_graph(log):
    process_tree = pm4py.discover_tree_inductive(log)
    bpmn_model = pm4py.convert_to_bpmn(process_tree)
    pm4py.view_bpmn(bpmn_model)

def read_xes():
    print("Printing XES LOGS:")
    log = pm4py.read_xes(XES_FILE)
    return log

def read_csv():
    print("Printing CSV LOGS:")
    pd_dataframe = pd.read_csv(CSV_FILE)
    #dataframe = pm4py.format_dataframe(pd_dataframe, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    dataframe = pm4py.format_dataframe(pd_dataframe, case_id='case_id', activity_key='activity', timestamp_key='time:timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    return event_log

if __name__ == "__main__":
    xes_logs = read_xes()
    csv_logs = read_csv()
    create_process_graph(xes_logs)