import tkinter as tk
from tkinter import filedialog, messagebox
import re

class FileOperation:
    def execute(self, file_path):
        pass

class ReadFileOperation(FileOperation):
    def execute(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found."

class WriteFileOperation(FileOperation):
    def execute(self, file_path, data):
        try:
            with open(file_path, 'a') as file:  
                file.write(data + '\n')
            return "Data successfully written to file."
        except Exception as e:
            return f"Error writing to file: {e}"

class FileOperationFactory:
    @staticmethod
    def create_operation(operation_type):
        if operation_type == "read":
            return ReadFileOperation()
        elif operation_type == "write":
            return WriteFileOperation()
        else:
            raise ValueError("Invalid operation type")

def is_valid_date(date_string):
    try:
        year, month, day = map(int, date_string.split('-'))
        if month < 1 or month > 12 or day < 1 or day > 31:
            return False
        return True
    except ValueError:
        return False

def browse_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def open_file():
    file_path = entry.get()
    operation = FileOperationFactory.create_operation("read")
    data = operation.execute(file_path)
    if data != "File not found.":
        root.destroy()
        open_main_window(file_path)
    else:
        print(data)

def open_main_window(file_path):
    def on_closing():
        global __main_window_open
        __main_window_open = False
        new_window.destroy()

    global __main_window_open
    if __main_window_open:
        return

    __main_window_open = True
    new_window = tk.Tk()
    new_window.geometry("350x75")
    new_window.title("File Operations")
    display_button = tk.Button(new_window, text="Display existing books", command=lambda: display_info(file_path))
    display_button.pack(side=tk.LEFT, padx=20)
    write_button = tk.Button(new_window, text="Enter a new book", command=lambda: write_book(file_path))
    write_button.pack(side=tk.RIGHT, padx=20)
    new_window.protocol("WM_DELETE_WINDOW", on_closing)
    new_window.mainloop()

def display_info(file_path):
    global __display_window_open, __write_window_open
    if __display_window_open or __write_window_open:
        return

    __display_window_open = True

    def on_closing():
        global __display_window_open
        __display_window_open = False
        info_window.destroy()

    def delete_selected():
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices):  # Reverse to delete from the end to avoid index shifting
            listbox.delete(index)
            
    def save_changes():
        lines = listbox.get(0, tk.END)
        with open(file_path, 'w') as file:
            file.write('\n'.join(lines))
    
    def change_availability():
        selected_index = listbox.curselection()
        if selected_index:
            index = selected_index[0]
            line = listbox.get(index)
            if line.endswith('+'):
                line = line[:-1] + '-'
            else:
                line = line[:-1] + '+'
            listbox.delete(index)
            listbox.insert(index, line)

    def read_file():
        operation = FileOperationFactory.create_operation("read")
        data = operation.execute(file_path)
        listbox.delete(0, tk.END)  
        for line in data.split('\n'):
            listbox.insert(tk.END, line)
    
    info_window = tk.Toplevel()
    info_window.title("File Contents")
    info_window.protocol("WM_DELETE_WINDOW", on_closing)
    label = tk.Label(info_window, text="File Contents:")
    label.pack(pady=10)
    listbox = tk.Listbox(info_window, selectmode=tk.SINGLE, width=50, height=20)
    listbox.pack(padx=10, pady=5)
    read_file()

    # Mygtukas, kad istrinti eilute
    delete_button = tk.Button(info_window, text="Delete Selected", command=delete_selected)
    delete_button.pack(pady=5)
    
    # Mygtukas pakeisti prieinamuma
    change_button = tk.Button(info_window, text="Change Availability", command=change_availability)
    change_button.pack(pady=5)

    # Mygtukas issaugoti busena
    save_button = tk.Button(info_window, text="Save Changes", command=save_changes)
    save_button.pack(pady=5)

def write_book(file_path):
    global __display_window_open, __write_window_open
    if __display_window_open or __write_window_open:
        return

    __write_window_open = True

    def on_closing():
        global __write_window_open
        __write_window_open = False
        book_window.destroy()

    def save_book_details():
        book_name = name_entry.get()[:30]  # Nustatome maksimallu 30 raidziu limita pavadinimui, bei autoriaus vardui/pavardei
        author_name = author_entry.get()[:30]  
        publication_date = date_entry.get()
        availability = '+' if availability_var.get() else '-'

        # Padarome, jog butu priimamos tik lotyniskos raides
        if not re.match(r'^[a-zA-Z\s.]+$', author_name):
            tk.messagebox.showerror("Error", "Author name can only contain letters, spaces, and dots.")
            return
        if not is_valid_date(publication_date):
            tk.messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        # Issaugome duomenis failo gale
        book_details = f'"{book_name}", "{author_name}", "{publication_date}", Availability status =  {availability}'
        operation = FileOperationFactory.create_operation("write")
        message = operation.execute(file_path, book_details)

        tk.messagebox.showinfo("Success", message)

    book_window = tk.Toplevel()
    book_window.title("Write Book Details")
    book_window.protocol("WM_DELETE_WINDOW", on_closing)

    name_label = tk.Label(book_window, text="Book Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(book_window, width=35)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    author_label = tk.Label(book_window, text="Author:")
    author_label.grid(row=1, column=0, padx=5, pady=5)
    author_entry = tk.Entry(book_window, width=35)
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    date_label = tk.Label(book_window, text="Publication Date (YYYY-MM-DD):")
    date_label.grid(row=2, column=0, padx=5, pady=5)
    date_entry = tk.Entry(book_window, width=35)
    date_entry.grid(row=2, column=1, padx=5, pady=5)

    availability_var = tk.BooleanVar(value=True)
    availability_check = tk.Checkbutton(book_window, text="Available", variable=availability_var)
    availability_check.grid(row=3, columnspan=2, pady=5)

    save_button = tk.Button(book_window, text="Save", command=save_book_details)
    save_button.grid(row=4, columnspan=2, pady=10)

# Su siais globaliais kintamaisias matome ar jau atviras langas, kad veliau galetume isvengti dubliu
__main_window_open = False
__display_window_open = False
__write_window_open = False

# Sukuriame pagrindini langa
root = tk.Tk()
root.title("File Directory Input")
root.geometry("400x150") 

label = tk.Label(root, text="Enter File Directory:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.insert(-1, 'C:/Users/infar/kursinis/demofile.txt')
entry.pack(pady=5)

# Mygtukas failo radimui
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

# Mygtukas failo atidarymui
open_button = tk.Button(root, text="Open", command=open_file)
open_button.pack(pady=5)
root.mainloop()