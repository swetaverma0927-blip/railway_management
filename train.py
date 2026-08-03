from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import re

# ============================================================
# DATABASE SETTINGS
# ============================================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Swet@2709"          # Apna MySQL password yahan likho
DB_NAME = "railway_system"
# ============================================================
# TRAIN MANAGEMENT CLASS
# Dashboard ke liye class ka naam exact Train rakha gaya hai
# ============================================================
class Train:

    def __init__(self, root):
        self.root = root
        self.root.title("Train Management")
        self.root.geometry("1450x760+30+20")
        self.root.configure(bg="#f4f6f8")

        try:
            self.root.state("zoomed")
        except:
            pass

        # Selected database ID
        self.selected_train_id = None

        # Variables
        self.var_train_number = StringVar()
        self.var_train_name = StringVar()
        self.var_source = StringVar()
        self.var_destination = StringVar()
        self.var_departure = StringVar()
        self.var_arrival = StringVar()
        self.var_total_seats = StringVar()
        self.var_available_seats = StringVar()
        self.var_train_type = StringVar(value="Choose")

        self.var_search_by = StringVar(value="Train Number")
        self.var_search_text = StringVar()

        # Database table create/check
        self.create_database_table()

        # UI
        self.create_header()
        self.create_main_content()

        # Load records
        self.fetch_trains()
    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    def connect_database(self):
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )


    def create_database_table(self):
        """Train table agar nahi hai to automatically create karega."""

        connection = None
        cursor = None

        try:
            # First database create karne ke liye connection
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )

            cursor = connection.cursor()

            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
            )

            cursor.close()
            connection.close()

            # Database select karke table create
            connection = self.connect_database()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trains (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    train_number VARCHAR(30) NOT NULL UNIQUE,
                    train_name VARCHAR(100) NOT NULL,
                    source_station VARCHAR(100) NOT NULL,
                    destination_station VARCHAR(100) NOT NULL,
                    departure_time VARCHAR(20) NOT NULL,
                    arrival_time VARCHAR(20) NOT NULL,
                    total_seats INT NOT NULL,
                    available_seats INT NOT NULL,
                    train_type VARCHAR(50) NOT NULL
                )
            """)

            connection.commit()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Database setup nahi ho paya.\n\n{error}",
                parent=self.root
            )

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = Frame(
            self.root,
            bg="#111827",
            height=105
        )
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(
            header,
            text="TRAIN MANAGEMENT",
            font=("Arial", 28, "bold"),
            bg="#111827",
            fg="#ef4444"
        ).pack(side=LEFT, padx=45, pady=28)

        Button(
            header,
            text="CLOSE",
            font=("Arial", 11, "bold"),
            bg="#7f1d1d",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            width=12,
            command=self.root.destroy
        ).pack(side=RIGHT, padx=45, pady=28)


    # ========================================================
    # MAIN CONTENT
    # ========================================================

    def create_main_content(self):

        main_frame = Frame(
            self.root,
            bg="#f4f6f8"
        )
        main_frame.pack(
            fill=BOTH,
            expand=True,
            padx=25,
            pady=20
        )

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

        self.create_train_details_frame(main_frame)
        self.create_train_records_frame(main_frame)


    # ========================================================
    # TRAIN DETAILS FORM
    # ========================================================

    def create_train_details_frame(self, parent):

        details_frame = LabelFrame(
            parent,
            text=" Train Details ",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#111827",
            bd=2,
            relief=GROOVE,
            padx=22,
            pady=15
        )

        details_frame.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(0, 15)
        )

        details_frame.configure(width=580)
        details_frame.grid_propagate(False)

        # Column configuration
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)

        # Row 0 - Train Number / Train Name
        self.create_label(
            details_frame,
            "Train Number",
            0,
            0
        )

        self.train_number_entry = self.create_entry(
            details_frame,
            self.var_train_number,
            1,
            0
        )

        self.create_label(
            details_frame,
            "Train Name",
            0,
            1
        )

        self.train_name_combo = ttk.Combobox(
            details_frame,
            textvariable=self.var_train_name,
            font=("Arial", 12),
            state="normal",
            width=25,
            values=[
                "Rajdhani Express",
                "Shatabdi Express",
                "Vande Bharat Express",
                "Duronto Express",
                "Garib Rath Express",
                "Jan Shatabdi Express",
                "Humsafar Express",
                "Tejas Express",
                "Superfast Express",
                "Intercity Express",
                "Passenger Train"
            ]
        )

        self.train_name_combo.grid(
            row=1,
            column=1,
            padx=12,
            pady=(3, 16),
            sticky="ew",
            ipady=7
        )

        # Row 2 - Source / Destination
        self.create_label(
            details_frame,
            "Source Station",
            2,
            0
        )

        self.source_combo = ttk.Combobox(
            details_frame,
            textvariable=self.var_source,
            font=("Arial", 12),
            state="normal",
            width=25,
            values=self.station_list()
        )

        self.source_combo.grid(
            row=3,
            column=0,
            padx=12,
            pady=(3, 16),
            sticky="ew",
            ipady=7
        )

        self.create_label(
            details_frame,
            "Destination Station",
            2,
            1
        )

        self.destination_combo = ttk.Combobox(
            details_frame,
            textvariable=self.var_destination,
            font=("Arial", 12),
            state="normal",
            width=25,
            values=self.station_list()
        )

        self.destination_combo.grid(
            row=3,
            column=1,
            padx=12,
            pady=(3, 16),
            sticky="ew",
            ipady=7
        )

        # Row 4 - Departure / Arrival
        self.create_label(
            details_frame,
            "Departure Time",
            4,
            0
        )

        self.departure_entry = self.create_entry(
            details_frame,
            self.var_departure,
            5,
            0
        )

        self.create_label(
            details_frame,
            "Arrival Time",
            4,
            1
        )

        self.arrival_entry = self.create_entry(
            details_frame,
            self.var_arrival,
            5,
            1
        )

        # Hint
        Label(
            details_frame,
            text="Time format: HH:MM, jaise 09:30 ya 18:45",
            font=("Arial", 9),
            bg="white",
            fg="#6b7280"
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            padx=12,
            pady=(0, 10)
        )

        # Row 7 - Total / Available Seats
        self.create_label(
            details_frame,
            "Total Seats",
            7,
            0
        )

        self.total_seats_entry = self.create_entry(
            details_frame,
            self.var_total_seats,
            8,
            0
        )

        self.total_seats_entry.bind(
            "<KeyRelease>",
            self.update_available_seats
        )

        self.create_label(
            details_frame,
            "Available Seats",
            7,
            1
        )

        self.available_seats_entry = Entry(
            details_frame,
            textvariable=self.var_available_seats,
            font=("Arial", 12),
            bg="#e5e7eb",
            fg="#374151",
            relief=SOLID,
            bd=1,
            state="readonly",
            readonlybackground="#e5e7eb"
        )

        self.available_seats_entry.grid(
            row=8,
            column=1,
            padx=12,
            pady=(3, 16),
            sticky="ew",
            ipady=9
        )

        # Train Type
        self.create_label(
            details_frame,
            "Train Type",
            9,
            0,
            columnspan=2
        )

        self.train_type_combo = ttk.Combobox(
            details_frame,
            textvariable=self.var_train_type,
            font=("Arial", 12),
            state="readonly",
            values=[
                "Choose",
                "Rajdhani",
                "Shatabdi",
                "Vande Bharat",
                "Duronto",
                "Superfast",
                "Express",
                "Passenger",
                "Intercity",
                "MEMU",
                "DEMU"
            ]
        )

        self.train_type_combo.grid(
            row=10,
            column=0,
            columnspan=2,
            padx=12,
            pady=(3, 20),
            sticky="ew",
            ipady=7
        )

        self.train_type_combo.current(0)

        # Buttons frame
        button_frame = Frame(
            details_frame,
            bg="white"
        )

        button_frame.grid(
            row=11,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=12,
            pady=(5, 8)
        )

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.create_action_button(
            button_frame,
            "SAVE",
            "#16a34a",
            0,
            0,
            self.save_train
        )

        self.create_action_button(
            button_frame,
            "UPDATE",
            "#0284c7",
            0,
            1,
            self.update_train
        )

        self.create_action_button(
            button_frame,
            "DELETE",
            "#db2777",
            1,
            0,
            self.delete_train
        )

        self.create_action_button(
            button_frame,
            "RESET",
            "#eab308",
            1,
            1,
            self.reset_fields
        )


    # ========================================================
    # TRAIN RECORDS TABLE
    # ========================================================

    def create_train_records_frame(self, parent):

        records_frame = LabelFrame(
            parent,
            text=" Train Records ",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#111827",
            bd=2,
            relief=GROOVE,
            padx=15,
            pady=15
        )

        records_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        records_frame.grid_rowconfigure(1, weight=1)
        records_frame.grid_columnconfigure(0, weight=1)

        # Search section
        search_frame = Frame(
            records_frame,
            bg="white"
        )

        search_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=(0, 14)
        )

        search_frame.grid_columnconfigure(2, weight=1)

        Label(
            search_frame,
            text="Search By:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#111827"
        ).grid(
            row=0,
            column=0,
            padx=(0, 8)
        )

        self.search_by_combo = ttk.Combobox(
            search_frame,
            textvariable=self.var_search_by,
            font=("Arial", 11),
            state="readonly",
            width=18,
            values=[
                "Train Number",
                "Train Name",
                "Source",
                "Destination",
                "Train Type"
            ]
        )

        self.search_by_combo.grid(
            row=0,
            column=1,
            padx=(0, 10),
            ipady=5
        )

        self.search_by_combo.current(0)

        self.search_entry = Entry(
            search_frame,
            textvariable=self.var_search_text,
            font=("Arial", 12),
            bg="white",
            fg="#111827",
            relief=SOLID,
            bd=1
        )

        self.search_entry.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(0, 10),
            ipady=8
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_train()
        )

        Button(
            search_frame,
            text="SEARCH",
            font=("Arial", 10, "bold"),
            bg="#1d4ed8",
            fg="white",
            activebackground="#1e40af",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            width=12,
            command=self.search_train
        ).grid(
            row=0,
            column=3,
            padx=5,
            ipady=8
        )

        Button(
            search_frame,
            text="SHOW ALL",
            font=("Arial", 10, "bold"),
            bg="#111827",
            fg="white",
            activebackground="#1f2937",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            width=12,
            command=self.show_all
        ).grid(
            row=0,
            column=4,
            padx=5,
            ipady=8
        )

        # Table frame
        table_frame = Frame(
            records_frame,
            bg="white"
        )

        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient=HORIZONTAL
        )

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL
        )

        columns = (
            "id",
            "train_number",
            "train_name",
            "source",
            "destination",
            "departure",
            "arrival",
            "total_seats",
            "available_seats",
            "train_type"
        )

        self.train_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(
            command=self.train_table.xview
        )

        scroll_y.config(
            command=self.train_table.yview
        )

        scroll_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        scroll_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.train_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Table headings
        headings = {
            "id": "ID",
            "train_number": "Train No.",
            "train_name": "Train Name",
            "source": "Source",
            "destination": "Destination",
            "departure": "Departure",
            "arrival": "Arrival",
            "total_seats": "Total Seats",
            "available_seats": "Available Seats",
            "train_type": "Train Type"
        }

        widths = {
            "id": 60,
            "train_number": 100,
            "train_name": 180,
            "source": 130,
            "destination": 130,
            "departure": 100,
            "arrival": 100,
            "total_seats": 100,
            "available_seats": 120,
            "train_type": 120
        }

        for column in columns:
            self.train_table.heading(
                column,
                text=headings[column]
            )

            self.train_table.column(
                column,
                width=widths[column],
                minwidth=widths[column],
                anchor=CENTER
            )

        # Table style
        style = ttk.Style()

        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=30,
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        self.train_table.bind(
            "<ButtonRelease-1>",
            self.get_selected_row
        )


    # ========================================================
    # HELPER UI METHODS
    # ========================================================

    def create_label(
        self,
        parent,
        text,
        row,
        column,
        columnspan=1
    ):
        Label(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#111827",
            anchor="w"
        ).grid(
            row=row,
            column=column,
            columnspan=columnspan,
            padx=12,
            pady=(5, 0),
            sticky="w"
        )


    def create_entry(
        self,
        parent,
        variable,
        row,
        column
    ):
        entry = Entry(
            parent,
            textvariable=variable,
            font=("Arial", 12),
            bg="white",
            fg="#111827",
            relief=SOLID,
            bd=1
        )

        entry.grid(
            row=row,
            column=column,
            padx=12,
            pady=(3, 16),
            sticky="ew",
            ipady=9
        )

        return entry


    def create_action_button(
        self,
        parent,
        text,
        color,
        row,
        column,
        command
    ):
        Button(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=command
        ).grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="ew",
            ipady=11
        )


    def station_list(self):
        return [
            "New Delhi",
            "Mumbai Central",
            "Varanasi Junction",
            "Lucknow Junction",
            "Kanpur Central",
            "Prayagraj Junction",
            "Patna Junction",
            "Howrah Junction",
            "Kolkata",
            "Chennai Central",
            "Bengaluru City",
            "Hyderabad Deccan",
            "Ahmedabad Junction",
            "Jaipur Junction",
            "Bhopal Junction",
            "Agra Cantt",
            "Gorakhpur Junction",
            "Ayodhya Cantt",
            "Dehradun",
            "Chandigarh"
        ]


    # ========================================================
    # AVAILABLE SEATS
    # ========================================================

    def update_available_seats(self, event=None):
        """
        New train save karte waqt Available Seats,
        Total Seats ke equal automatically ho jayegi.
        """

        if self.selected_train_id is None:
            total = self.var_total_seats.get().strip()

            if total.isdigit():
                self.var_available_seats.set(total)
            else:
                self.var_available_seats.set("")


    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_fields(self):

        train_number = self.var_train_number.get().strip()
        train_name = self.var_train_name.get().strip()
        source = self.var_source.get().strip()
        destination = self.var_destination.get().strip()
        departure = self.var_departure.get().strip()
        arrival = self.var_arrival.get().strip()
        total_seats = self.var_total_seats.get().strip()
        train_type = self.var_train_type.get().strip()

        if not train_number:
            messagebox.showwarning(
                "Required Field",
                "Train Number enter karo.",
                parent=self.root
            )
            self.train_number_entry.focus()
            return False

        if not train_name:
            messagebox.showwarning(
                "Required Field",
                "Train Name enter ya select karo.",
                parent=self.root
            )
            self.train_name_combo.focus()
            return False

        if not source:
            messagebox.showwarning(
                "Required Field",
                "Source Station select karo.",
                parent=self.root
            )
            self.source_combo.focus()
            return False

        if not destination:
            messagebox.showwarning(
                "Required Field",
                "Destination Station select karo.",
                parent=self.root
            )
            self.destination_combo.focus()
            return False

        if source.lower() == destination.lower():
            messagebox.showwarning(
                "Invalid Journey",
                "Source aur Destination same nahi ho sakte.",
                parent=self.root
            )
            return False

        if not departure:
            messagebox.showwarning(
                "Required Field",
                "Departure Time enter karo.",
                parent=self.root
            )
            self.departure_entry.focus()
            return False

        if not arrival:
            messagebox.showwarning(
                "Required Field",
                "Arrival Time enter karo.",
                parent=self.root
            )
            self.arrival_entry.focus()
            return False

        if not self.valid_time(departure):
            messagebox.showwarning(
                "Invalid Time",
                "Departure Time HH:MM format me enter karo.\nExample: 09:30",
                parent=self.root
            )
            self.departure_entry.focus()
            return False

        if not self.valid_time(arrival):
            messagebox.showwarning(
                "Invalid Time",
                "Arrival Time HH:MM format me enter karo.\nExample: 18:45",
                parent=self.root
            )
            self.arrival_entry.focus()
            return False

        if not total_seats:
            messagebox.showwarning(
                "Required Field",
                "Total Seats enter karo.",
                parent=self.root
            )
            self.total_seats_entry.focus()
            return False

        if not total_seats.isdigit():
            messagebox.showwarning(
                "Invalid Seats",
                "Total Seats me sirf number enter karo.",
                parent=self.root
            )
            self.total_seats_entry.focus()
            return False

        if int(total_seats) <= 0:
            messagebox.showwarning(
                "Invalid Seats",
                "Total Seats zero se zyada honi chahiye.",
                parent=self.root
            )
            return False

        if train_type == "Choose" or not train_type:
            messagebox.showwarning(
                "Required Field",
                "Train Type select karo.",
                parent=self.root
            )
            self.train_type_combo.focus()
            return False

        return True


    def valid_time(self, value):
        """
        24-hour HH:MM format validate karega.
        Example: 09:30, 18:45
        """

        pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"
        return bool(re.match(pattern, value))

    # ========================================================
    # SAVE TRAIN
    # ========================================================

    def save_train(self):

        if not self.validate_fields():
            return

        connection = None
        cursor = None

        try:
            connection = self.connect_database()
            cursor = connection.cursor()

            train_number = self.var_train_number.get().strip()

            # Duplicate check
            cursor.execute(
                """
                SELECT id
                FROM trains
                WHERE train_number = %s
                """,
                (train_number,)
            )

            duplicate = cursor.fetchone()

            if duplicate:
                messagebox.showwarning(
                    "Duplicate Train",
                    "Ye Train Number database me already maujood hai.",
                    parent=self.root
                )
                return

            total_seats = int(
                self.var_total_seats.get().strip()
            )

            # New train me available seats = total seats
            available_seats = total_seats

            cursor.execute(
                """
                INSERT INTO trains (
                    train_number,
                    train_name,
                    source_station,
                    destination_station,
                    departure_time,
                    arrival_time,
                    total_seats,
                    available_seats,
                    train_type
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    train_number,
                    self.var_train_name.get().strip(),
                    self.var_source.get().strip(),
                    self.var_destination.get().strip(),
                    self.var_departure.get().strip(),
                    self.var_arrival.get().strip(),
                    total_seats,
                    available_seats,
                    self.var_train_type.get().strip()
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Train successfully save ho gayi.",
                parent=self.root
            )

            self.fetch_trains()
            self.reset_fields()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Train save nahi ho payi.\n\n{error}",
                parent=self.root
            )

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # ========================================================
    # FETCH ALL TRAINS
    # ========================================================

    def fetch_trains(self):

        connection = None
        cursor = None

        try:
            connection = self.connect_database()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    train_number,
                    train_name,
                    source_station,
                    destination_station,
                    departure_time,
                    arrival_time,
                    total_seats,
                    available_seats,
                    train_type
                FROM trains
                ORDER BY id DESC
            """)

            rows = cursor.fetchall()

            self.clear_table()

            for row in rows:
                self.train_table.insert(
                    "",
                    END,
                    values=row
                )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Train records load nahi hue.\n\n{error}",
                parent=self.root
            )

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # ========================================================
    # SELECT TABLE ROW
    # ========================================================

    def get_selected_row(self, event=None):

        selected = self.train_table.selection()

        if not selected:
            return

        values = self.train_table.item(
            selected[0],
            "values"
        )

        if not values:
            return

        self.selected_train_id = values[0]

        self.var_train_number.set(values[1])
        self.var_train_name.set(values[2])
        self.var_source.set(values[3])
        self.var_destination.set(values[4])
        self.var_departure.set(values[5])
        self.var_arrival.set(values[6])
        self.var_total_seats.set(values[7])
        self.var_available_seats.set(values[8])
        self.var_train_type.set(values[9])

        # ========================================================
    # UPDATE TRAIN
    # ========================================================

    def update_train(self):

        if self.selected_train_id is None:
            messagebox.showwarning(
                "Select Train",
                "Update karne ke liye table se train select karo.",
                parent=self.root
            )
            return

        if not self.validate_fields():
            return

        connection = None
        cursor = None

        try:
            connection = self.connect_database()
            cursor = connection.cursor()

            train_number = self.var_train_number.get().strip()

            # Duplicate Train Number check excluding selected row
            cursor.execute(
                """
                SELECT id
                FROM trains
                WHERE train_number = %s
                AND id != %s
                """,
                (
                    train_number,
                    self.selected_train_id
                )
            )

            duplicate = cursor.fetchone()

            if duplicate:
                messagebox.showwarning(
                    "Duplicate Train",
                    "Is Train Number ki doosri train already maujood hai.",
                    parent=self.root
                )
                return

            new_total_seats = int(
                self.var_total_seats.get().strip()
            )

            current_available = self.var_available_seats.get().strip()

            if current_available.isdigit():
                current_available = int(current_available)
            else:
                current_available = new_total_seats

            # Available seats total se zyada nahi ho sakti
            if current_available > new_total_seats:
                current_available = new_total_seats

            cursor.execute(
                """
                UPDATE trains
                SET
                    train_number = %s,
                    train_name = %s,
                    source_station = %s,
                    destination_station = %s,
                    departure_time = %s,
                    arrival_time = %s,
                    total_seats = %s,
                    available_seats = %s,
                    train_type = %s
                WHERE id = %s
                """,
                (
                    train_number,
                    self.var_train_name.get().strip(),
                    self.var_source.get().strip(),
                    self.var_destination.get().strip(),
                    self.var_departure.get().strip(),
                    self.var_arrival.get().strip(),
                    new_total_seats,
                    current_available,
                    self.var_train_type.get().strip(),
                    self.selected_train_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Train record successfully update ho gaya.",
                parent=self.root
            )

            self.fetch_trains()
            self.reset_fields()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Train update nahi ho payi.\n\n{error}",
                parent=self.root
            )

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # ========================================================
    # DELETE TRAIN
    # ========================================================

    def delete_train(self):

        if self.selected_train_id is None:
            messagebox.showwarning(
                "Select Train",
                "Delete karne ke liye table se train select karo.",
                parent=self.root
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            "Kya aap selected train ko delete karna chahte hain?",
            parent=self.root
        )

        if not confirmation:
            return

        connection = None
        cursor = None

        try:
            connection = self.connect_database()
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM trains
                WHERE id = %s
                """,
                (self.selected_train_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Train record successfully delete ho gaya.",
                parent=self.root
            )

            self.fetch_trains()
            self.reset_fields()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Train delete nahi ho payi.\n\n{error}",
                parent=self.root
            )

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # ========================================================
    # SEARCH TRAIN
    # ========================================================

    def search_train(self):

        search_by = self.var_search_by.get().strip()
        search_text = self.var_search_text.get().strip()

        if not search_text:
            messagebox.showwarning(
                "Search",
                "Search karne ke liye value enter karo.",
                parent=self.root
            )
            self.search_entry.focus()
            return

        column_mapping = {
            "Train Number": "train_number",
            "Train Name": "train_name",
            "Source": "source_station",
            "Destination": "destination_station",
            "Train Type": "train_type"
        }

        database_column = column_mapping.get(
            search_by,
            "train_number"
        )

        connection = None
        cursor = None

        try:
            connection = self.connect_database()
            cursor = connection.cursor()

            query = f"""
                SELECT
                    id,
                    train_number,
                    train_name,
                    source_station,
                    destination_station,
                    departure_time,
                    arrival_time,
                    total_seats,
                    available_seats,
                    train_type
                FROM trains
                WHERE {database_column} LIKE %s
                ORDER BY id DESC
            """

            cursor.execute(
                query,
                (f"%{search_text}%",)
            )

            rows = cursor.fetchall()

            self.clear_table()

            for row in rows:
                self.train_table.insert(
                    "",
                    END,
                    values=row
                )

            if not rows:
                messagebox.showinfo(
                    "No Record",
                    "Koi matching train record nahi mila.",
                    parent=self.root
                )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Search perform nahi ho payi.\n\n{error}",
                parent=self.root
            )

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()


    # ========================================================
    # SHOW ALL
    # ========================================================

    def show_all(self):
        self.var_search_text.set("")
        self.var_search_by.set("Train Number")
        self.fetch_trains()


    # ========================================================
    # RESET
    # ========================================================

    def reset_fields(self):

        self.selected_train_id = None

        self.var_train_number.set("")
        self.var_train_name.set("")
        self.var_source.set("")
        self.var_destination.set("")
        self.var_departure.set("")
        self.var_arrival.set("")
        self.var_total_seats.set("")
        self.var_available_seats.set("")
        self.var_train_type.set("Choose")

        # Table selection remove
        selected_items = self.train_table.selection()

        for item in selected_items:
            self.train_table.selection_remove(item)

        self.train_number_entry.focus()


    # ========================================================
    # CLEAR TABLE
    # ========================================================

    def clear_table(self):
        for item in self.train_table.get_children():
            self.train_table.delete(item)


# ============================================================
# DIRECT RUN
# ============================================================

if __name__ == "__main__":
    root = Tk()
    app = Train(root)
    root.mainloop()