import os
import csv
import re
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.PROGRESS_BAR_LENGTH = 500
        self.csv_file_path = None
        # Automatically set the folder file path to the current directory
        self.folder_file_path = os.getcwd()

        # Window Properties
        self.title(".csv to .txt Converter")

        # Application Heading
        title_font = ('Helvetica', 16, 'bold')
        self.title_label = ttk.Label(
            self, text='CSV to TXT Converter', font=title_font, foreground='#336699')
        self.title_label.pack(pady=10)

        # Description
        description_font = ('Helvetica', 12, 'italic')
        self.description_label = ttk.Label(
            self, text="This application converts all lines in a .csv file into individual .txt files.", font=description_font)
        self.description_label.pack(pady=10)

        # File Explorer
        file_select_button_font = ('Helvetica', 12, 'bold')

        self.csv_file = ttk.Label(
            self, text="Location of the .csv File:", font=file_select_button_font)
        self.csv_file.pack(pady=5)

        self.csv_button = ttk.Button(
            self, text="Browse CSV", command=lambda: self.find_file('csv'))
        self.csv_button.pack(pady=5)

        self.txt_files = ttk.Label(
            self, text=f"Location of .txt Folder: {os.getcwd()}", font=file_select_button_font)
        self.txt_files.pack(pady=5)

        self.txt_button = ttk.Button(
            self, text="Browse TXT", command=lambda: self.find_file('txt'))
        self.txt_button.pack(pady=5)

        # Convert Button
        self.convert_button = ttk.Button(
            self, text="Convert", command=lambda: self.convert(), state='disabled')
        self.convert_button.pack(pady=10, ipadx=20, ipady=15)

        # Progress Details
        self.progress_bar = ttk.Progressbar(
            self, orient='horizontal', length=self.PROGRESS_BAR_LENGTH, mode='determinate')
        self.progress_bar.pack(pady=5)

        progress_font = ('Helvetica', 10, 'italic')
        self.progress_label = ttk.Label(self, text="", font=progress_font)
        self.progress_label.pack(pady=5)

    def find_file(self, file_type):
        if file_type == 'csv':
            file_path = filedialog.askopenfilename(
                filetypes=[(f".{file_type.upper()} files", f"*.{file_type}")])
        elif file_type == 'txt':
            file_path = filedialog.askdirectory()

        if file_path:  # Update labels in app
            if file_type == 'csv':
                self.csv_file.config(
                    text=f"Location of the .csv File: {file_path}")
                self.csv_file_path = file_path
            elif file_type == 'txt':
                self.txt_files.config(
                    text=f"Location of .txt Folder: {file_path}")
                self.folder_file_path = file_path

        self.check_conditions()

    def check_conditions(self):
        conditions_met = self.csv_file_path and self.folder_file_path
        if conditions_met:
            # Allow users to click on text once both csv and folder file paths are initialised
            self.convert_button['state'] = 'normal'
        else:
            self.convert_button['state'] = 'disabled'

    def convert(self):
        try:
            with open(self.csv_file_path, 'r') as file:
                reader = csv.reader(file, delimiter="\t")

                # Get file path of the new directory to be added
                new_folder_path = self.get_full_file_path()
                os.makedirs(new_folder_path)

                total_lines = len(list(reader))
                self.progress_bar["maximum"] = total_lines

                file.seek(0)

                headers = []
                for line_index, line in enumerate(reader):
                    if line_index == 0:
                        # Get all headers of the csv file
                        headers = line[0].split(",")
                        continue  # Do not convert the header line to a .txt file

                    if line:
                        new_file_name = f"{new_folder_path}/line_{line_index + 1}.txt"

                        with open(new_file_name, "w") as new_file:
                            # Split line based on commas, but not if a space follows comma, e.g. "abc,def" would be split, but "abc, def" would not
                            cells = re.split(r',(?!\s)', line[0])
                            for header_index, cell in enumerate(cells):
                                new_file.write(
                                    f"{headers[header_index]}: {cell}\n")

                        # Updated progress bar and labels
                        self.progress_bar["value"] = line_index + 1
                        self.progress_label.config(
                            text=f"Line {line_index + 1}")
                        self.update_idletasks()

                self.progress_label.config(text=f"Completed")

        except Exception as e:
            self.progress_label.config(
                text=f"An Error Occured. Please corretly format your selected .csv file and try again.")

    def get_full_file_path(self):
        file_name = self.csv_file_path.split('/')[-1][:-4]
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{self.folder_file_path}/{file_name}_{current_time}"


if __name__ == "__main__":
    app = App()
    app.mainloop()
