import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from Combinatronics import combine_shapefiles, find_shapefiles


class CombinatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Shapefile Combinator")

        self.input_dir = tk.StringVar()
        self.output_file = tk.StringVar()

        # Input Directory
        tk.Label(master, text="Input Directory:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5)
        self.input_entry = tk.Entry(
            master, textvariable=self.input_dir, width=50)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_input).grid(
            row=0, column=2, padx=5, pady=5)

        # Output GeoPackage
        tk.Label(master, text="Output GeoPackage:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5)
        self.output_entry = tk.Entry(
            master, textvariable=self.output_file, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_output).grid(
            row=1, column=2, padx=5, pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(master, length=300, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=3,
                           pady=10, padx=5, sticky="ew")

        # Combine Button
        self.combine_button = tk.Button(master, text="Combine Shapefiles",
                                        command=self.run_combinator)
        self.combine_button.grid(row=3, column=1, pady=10)

    def browse_input(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir.set(directory)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gpkg", filetypes=[("GeoPackage", "*.gpkg")])
        if file_path:
            self.output_file.set(file_path)

    def run_combinator(self):
        input_dir = self.input_dir.get()
        output_file = self.output_file.get()
        if not input_dir or not output_file:
            messagebox.showerror(
                "Error", "Please provide both input directory and output file.")
            return

        self.combine_button.config(state='disabled')
        self.progress['value'] = 0

        # Start processing in a separate thread
        thread = threading.Thread(
            target=self.process_files, args=(input_dir, output_file))
        thread.start()

    def process_files(self, input_dir, output_file):
        try:
            shp_files = find_shapefiles(input_dir)
            total_files = len(shp_files)

            def update_progress(current, total):
                progress_value = int((current / total) * 100)
                self.progress['value'] = progress_value
                self.master.update_idletasks()

            combine_shapefiles(input_dir, output_file,
                               progress_callback=update_progress)

            self.master.after(0, self.show_completion, output_file)
        except Exception as e:
            self.master.after(0, self.show_error, str(e))

    def show_completion(self, output_file):
        messagebox.showinfo(
            "Success", f"Combined shapefiles saved to {output_file}")
        self.combine_button.config(state='normal')
        self.open_output_folder(output_file)

    def show_error(self, error_message):
        messagebox.showerror("Error", f"An error occurred: {error_message}")
        self.combine_button.config(state='normal')

    def open_output_folder(self, output_file):
        output_dir = os.path.dirname(output_file)
        try:
            os.startfile(output_dir)
        except AttributeError:
            # For non-Windows systems
            import subprocess
            subprocess.Popen(['xdg-open', output_dir])


def main():
    root = tk.Tk()
    gui = CombinatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
