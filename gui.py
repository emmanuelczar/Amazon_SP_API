import tkinter as tk
from tkinter import ttk
from data.report_dict import report_dictionary
from data.marketplace_dict import marketplace_dictionary

report_list = [key for key in report_dictionary]
markets = [key for key in marketplace_dictionary]


def download_batch():
    selected_items = []
    for i, var in enumerate(report_list_vars):
        if var.get() == 1:
            selected_items.append(report_list[i])
    print("Batch download:", selected_items)

def download_individual():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    print("Individual download - Start Date:", start_date)
    print("Individual download - End Date:", end_date)



root = tk.Tk()
root.title("Amazon SP-API Downloader")

# Left Half Section (Batch Download)
left_frame = ttk.Frame(root, width=400, padding=10)
left_frame.grid(row=0, column=0, sticky="nsew")

report_label = ttk.Label(left_frame, text="Select Reports:")
report_label.pack()

report_list_vars = []
for report in report_list:
    var = tk.IntVar()
    report_list_vars.append(var)
    radio_button = ttk.Radiobutton(left_frame, text=report, variable=var, value=1)
    radio_button.pack(anchor="w")

market_label = ttk.Label(left_frame, text="Select Markets:")
market_label.pack()

market_vars = []
for market in markets:
    var = tk.IntVar()
    market_vars.append(var)
    radio_button = ttk.Radiobutton(left_frame, text=market, variable=var, value=1)
    radio_button.pack(anchor="w")

days_offset_label = ttk.Label(left_frame, text="# of Days Offset")
days_offset_label.pack()

days_offset_entry = ttk.Entry(left_frame, width=10)
days_offset_entry.pack()

batch_download_button = ttk.Button(left_frame, text="Download", command=download_batch)
batch_download_button.pack()

cancel_batch_button = ttk.Button(left_frame, text="Cancel")
cancel_batch_button.pack()

# Right Half Section (Individual Download)
right_frame = ttk.Frame(root, width=400, padding=10)
right_frame.grid(row=0, column=1, sticky="nsew")

dropdown_label = ttk.Label(right_frame, text="Select Item:")
dropdown_label.pack()

dropdown_values = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
dropdown = ttk.Combobox(right_frame, values=dropdown_values, state="readonly")
dropdown.current(0)
dropdown.pack()

start_date_label = ttk.Label(right_frame, text="Start Date:")
start_date_label.pack()

start_date_entry = ttk.Entry(right_frame, width=12)
start_date_entry.insert(0, "2023-01-01")
start_date_entry.pack()

end_date_label = ttk.Label(right_frame, text="End Date:")
end_date_label.pack()

end_date_entry = ttk.Entry(right_frame, width=12)
end_date_entry.insert(0, "2023-01-01")
end_date_entry.pack()

individual_download_button = ttk.Button(right_frame, text="Download", command=download_individual)
individual_download_button.pack()

cancel_individual_button = ttk.Button(right_frame, text="Cancel")
cancel_individual_button.pack()

root.mainloop()

