# import library
import jtextfsm as textfsm
import pandas as pd

# Load the input file to a variable
input_file = open("show_output.txt")
raw_text_data = input_file.read()
input_file.close()

# Run the text through the FSM. 
# The argument 'template' is a file handle and 'raw_text_data' is a 
# string with the content from the show_inventory.txt file
template = open("show_ip_bgp_summary.txt")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(raw_text_data)

df = pd.DataFrame(fsm_results, columns=re_table.header)
print df

# the results are written to a CSV file
df.to_csv ("out_csv/outfile.csv")
df.to_excel ("out_csv/outfile.xlsx")
