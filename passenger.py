import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector
from mysql.connector import Error

from config import HOST, USER, PASSWORD, DATABASE, PORT


class Passenger:
    def __init__(self, root):
        self.root = root

        self.root.title("Passenger Management")
        self.root.geometry("1200x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#e5e7eb")

        self.selected_id = None

        self.name_var = tk.StringVar()
        self.father_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.mobile_var = tk.StringVar()
        self.address_var = tk.StringVar()

        self.create_header()
        self.create_form()
        self.create_table()

        self.load_passengers()

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================
    def get_connection(self):
        try:
            return mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                port=PORT
            )

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Database connection failed:\n{error}"
            )
            return None

    # ==================================================
    # HEADER
    # ==================================================
    def create_header(self):
        header = tk.Frame(
            self.root,
            bg="#071725",
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        heading = tk.Label(
            header,
            text="PASSENGER MANAGEMENT",
            font=("Segoe UI", 25, "bold"),
            bg="#071725",
            fg="#fbbf24"
        )
        heading.pack(
            side="left",
            padx=30,
            pady=20
        )

        close_button = tk.Button(
            header,
            text="CLOSE",
            command=self.root.destroy,
            font=("Segoe UI", 11, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            bd=0,
            cursor="hand2"
        )
        close_button.pack(
            side="right",
            padx=30,
            ipadx=20,
            ipady=8
        )

    # ==================================================
    # PASSENGER FORM
    # ==================================================
    def create_form(self):
        form_frame = tk.LabelFrame(
            self.root,
            text="Passenger Details",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#0f172a",
            bd=1,
            relief="solid"
        )
        form_frame.place(
            x=25,
            y=100,
            width=430,
            height=570
        )

        self.create_label_entry(
            form_frame,
            "Passenger Name",
            self.name_var,
            35
        )

        self.create_label_entry(
            form_frame,
            "Father Name",
            self.father_var,
            105
        )

        gender_label = tk.Label(
            form_frame,
            text="Gender",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#111827"
        )
        gender_label.place(x=25, y=180)

        gender_combo = ttk.Combobox(
            form_frame,
            textvariable=self.gender_var,
            values=["Male", "Female", "Other"],
            state="readonly",
            font=("Segoe UI", 11)
        )
        gender_combo.place(
            x=25,
            y=207,
            width=175,
            height=35
        )

        age_label = tk.Label(
            form_frame,
            text="Age",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#111827"
        )
        age_label.place(x=225, y=180)

        age_entry = tk.Entry(
            form_frame,
            textvariable=self.age_var,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )
        age_entry.place(
            x=225,
            y=207,
            width=175,
            height=35
        )

        self.create_label_entry(
            form_frame,
            "Mobile Number",
            self.mobile_var,
            255
        )

        self.create_label_entry(
            form_frame,
            "Address",
            self.address_var,
            325
        )

        button_frame = tk.Frame(
            form_frame,
            bg="white"
        )
        button_frame.place(
            x=20,
            y=395,
            width=390,
            height=120
        )

        self.create_button(
            button_frame,
            "SAVE",
            self.save_passenger,
            "#15803d",
            0,
            0
        )

        self.create_button(
            button_frame,
            "UPDATE",
            self.update_passenger,
            "#0369a1",
            0,
            1
        )

        self.create_button(
            button_frame,
            "DELETE",
            self.delete_passenger,
            "#dc2626",
            1,
            0
        )

        self.create_button(
            button_frame,
            "RESET",
            self.reset_form,
            "#d97706",
            1,
            1
        )

    def create_label_entry(
        self,
        parent,
        label_text,
        variable,
        y_position
    ):
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#111827"
        )
        label.place(
            x=25,
            y=y_position
        )

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )
        entry.place(
            x=25,
            y=y_position + 27,
            width=375,
            height=35
        )

    def create_button(
        self,
        parent,
        text,
        command,
        color,
        row,
        column
    ):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="white",
            activeforeground="white",
            bd=0,
            cursor="hand2"
        )

        button.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            ipadx=35,
            ipady=10,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

    # ==================================================
    # TABLE
    # ==================================================
    def create_table(self):
        table_frame = tk.LabelFrame(
            self.root,
            text="Passenger Records",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#0f172a",
            bd=1,
            relief="solid"
        )
        table_frame.place(
            x=475,
            y=100,
            width=700,
            height=570
        )

        search_label = tk.Label(
            table_frame,
            text="Search:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#111827"
        )
        search_label.place(
            x=15,
            y=15
        )

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            table_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )
        search_entry.place(
            x=80,
            y=12,
            width=300,
            height=32
        )

        search_button = tk.Button(
            table_frame,
            text="SEARCH",
            command=self.search_passenger,
            font=("Segoe UI", 10, "bold"),
            bg="#0369a1",
            fg="white",
            bd=0,
            cursor="hand2"
        )
        search_button.place(
            x=395,
            y=12,
            width=100,
            height=32
        )

        show_all_button = tk.Button(
            table_frame,
            text="SHOW ALL",
            command=self.load_passengers,
            font=("Segoe UI", 10, "bold"),
            bg="#475569",
            fg="white",
            bd=0,
            cursor="hand2"
        )
        show_all_button.place(
            x=510,
            y=12,
            width=105,
            height=32
        )

        columns = (
            "id",
            "name",
            "father",
            "gender",
            "age",
            "mobile",
            "address"
        )

        self.passenger_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.passenger_table.heading(
            "id",
            text="ID"
        )
        self.passenger_table.heading(
            "name",
            text="Passenger Name"
        )
        self.passenger_table.heading(
            "father",
            text="Father Name"
        )
        self.passenger_table.heading(
            "gender",
            text="Gender"
        )
        self.passenger_table.heading(
            "age",
            text="Age"
        )
        self.passenger_table.heading(
            "mobile",
            text="Mobile"
        )
        self.passenger_table.heading(
            "address",
            text="Address"
        )

        self.passenger_table.column(
            "id",
            width=50,
            anchor="center"
        )
        self.passenger_table.column(
            "name",
            width=150
        )
        self.passenger_table.column(
            "father",
            width=150
        )
        self.passenger_table.column(
            "gender",
            width=80,
            anchor="center"
        )
        self.passenger_table.column(
            "age",
            width=60,
            anchor="center"
        )
        self.passenger_table.column(
            "mobile",
            width=110
        )
        self.passenger_table.column(
            "address",
            width=180
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.passenger_table.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.passenger_table.xview
        )

        self.passenger_table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.passenger_table.place(
            x=15,
            y=60,
            width=650,
            height=520
        )

        vertical_scrollbar.place(
            x=665,
            y=60,
            height=520
        )

        horizontal_scrollbar.place(
            x=15,
            y=520,
            width=650,
            height=20
        )

        self.passenger_table.bind(
            "<<TreeviewSelect>>",
            self.select_passenger
        )

    # ==================================================
    # VALIDATION
    # ==================================================
    def validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showwarning(
                "Required",
                "Passenger name enter करो।"
            )
            return False

        if not self.gender_var.get():
            messagebox.showwarning(
                "Required",
                "Gender select करो।"
            )
            return False

        age = self.age_var.get().strip()

        if not age.isdigit():
            messagebox.showwarning(
                "Invalid Age",
                "Age केवल numbers में डालो।"
            )
            return False

        mobile = self.mobile_var.get().strip()

        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showwarning(
                "Invalid Mobile",
                "Mobile number 10 digits का होना चाहिए।"
            )
            return False

        return True

    # ==================================================
    # SAVE
    # ==================================================
    def save_passenger(self):
        if not self.validate_form():
            return

        connection = self.get_connection()

        if connection is None:
            return

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
            INSERT INTO passengers
            (
                passenger_name,
                father_name,
                gender,
                age,
                mobile,
                address
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                self.name_var.get().strip(),
                self.father_var.get().strip(),
                self.gender_var.get(),
                int(self.age_var.get()),
                self.mobile_var.get().strip(),
                self.address_var.get().strip()
            )

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo(
                "Success",
                "Passenger saved successfully."
            )

            self.reset_form()
            self.load_passengers()

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Passenger save नहीं हुआ:\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # ==================================================
    # LOAD DATA
    # ==================================================
    def load_passengers(self):
        for row in self.passenger_table.get_children():
            self.passenger_table.delete(row)

        connection = self.get_connection()

        if connection is None:
            return

        cursor = None

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    passenger_name,
                    father_name,
                    gender,
                    age,
                    mobile,
                    address
                FROM passengers
                ORDER BY id DESC
                """
            )

            records = cursor.fetchall()

            for record in records:
                self.passenger_table.insert(
                    "",
                    tk.END,
                    values=record
                )

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Records load नहीं हुए:\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # ==================================================
    # SELECT RECORD
    # ==================================================
    def select_passenger(self, event=None):
        selected = self.passenger_table.focus()

        if not selected:
            return

        values = self.passenger_table.item(
            selected,
            "values"
        )

        if not values:
            return

        self.selected_id = values[0]

        self.name_var.set(values[1])
        self.father_var.set(values[2])
        self.gender_var.set(values[3])
        self.age_var.set(values[4])
        self.mobile_var.set(values[5])
        self.address_var.set(values[6])

    # ==================================================
    # UPDATE
    # ==================================================
    def update_passenger(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Record",
                "पहले table से passenger select करो।"
            )
            return

        if not self.validate_form():
            return

        connection = self.get_connection()

        if connection is None:
            return

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
            UPDATE passengers
            SET
                passenger_name = %s,
                father_name = %s,
                gender = %s,
                age = %s,
                mobile = %s,
                address = %s
            WHERE id = %s
            """

            values = (
                self.name_var.get().strip(),
                self.father_var.get().strip(),
                self.gender_var.get(),
                int(self.age_var.get()),
                self.mobile_var.get().strip(),
                self.address_var.get().strip(),
                self.selected_id
            )

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo(
                "Updated",
                "Passenger updated successfully."
            )

            self.reset_form()
            self.load_passengers()

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Passenger update नहीं हुआ:\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # ==================================================
    # DELETE
    # ==================================================
    def delete_passenger(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Record",
                "पहले table से passenger select करो।"
            )
            return

        answer = messagebox.askyesno(
            "Delete",
            "क्या आप selected passenger delete करना चाहते हैं?"
        )

        if not answer:
            return

        connection = self.get_connection()

        if connection is None:
            return

        cursor = None

        try:
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM passengers WHERE id = %s",
                (self.selected_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Passenger deleted successfully."
            )

            self.reset_form()
            self.load_passengers()

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Passenger delete नहीं हुआ:\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # ==================================================
    # SEARCH
    # ==================================================
    def search_passenger(self):
        search_text = self.search_var.get().strip()

        if not search_text:
            self.load_passengers()
            return

        for row in self.passenger_table.get_children():
            self.passenger_table.delete(row)

        connection = self.get_connection()

        if connection is None:
            return

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
            SELECT
                id,
                passenger_name,
                father_name,
                gender,
                age,
                mobile,
                address
            FROM passengers
            WHERE passenger_name LIKE %s
               OR mobile LIKE %s
            ORDER BY id DESC
            """

            search_value = f"%{search_text}%"

            cursor.execute(
                query,
                (search_value, search_value)
            )

            records = cursor.fetchall()

            for record in records:
                self.passenger_table.insert(
                    "",
                    tk.END,
                    values=record
                )

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Search failed:\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # ==================================================
    # RESET
    # ==================================================
    def reset_form(self):
        self.selected_id = None

        self.name_var.set("")
        self.father_var.set("")
        self.gender_var.set("")
        self.age_var.set("")
        self.mobile_var.set("")
        self.address_var.set("")

        for selected in self.passenger_table.selection():
            self.passenger_table.selection_remove(selected)


if __name__ == "__main__":
    root = tk.Tk()
    Passenger(root)
    root.mainloop()