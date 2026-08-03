from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date
# ======================================================
# DATABASE SETTINGS
# ======================================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Swet@2709"          # Apna MySQL password yahan likho
DB_NAME = "railway_system"
class TicketPage:

    def __init__(self, root):
        self.root = root
        self.root.title("Indian Railway Ticket Booking")
        self.root.geometry("1350x750+0+0")
        self.root.resizable(True, True)
        self.root.configure(bg="#e7e7e7")

        self.selected_booking_ref = None
        self.passenger_records = {}

        # ---------------- Variables ----------------

        self.train_name = StringVar()
        self.booking_ref = StringVar()
        self.coach_type = StringVar()
        self.seat_number = StringVar()
        self.platform_name = StringVar()
        self.departure_date = StringVar()
        self.arrival_date = StringVar()
        self.travel_time = StringVar()
        self.route_no = StringVar()

        self.ticket_fare = StringVar()
        self.passenger_choice = StringVar()
        self.passenger_id = StringVar()
        self.contact_number = StringVar()
        self.passenger_name = StringVar()
        self.journey_from = StringVar()
        self.journey_to = StringVar()

        # ---------------- Dropdown Data ----------------

        self.train_values = [
            "Choose",
            "Rajdhani Express",
            "Shatabdi Express",
            "Vande Bharat Express",
            "Duronto Express",
            "Gatimaan Express",
            "Garib Rath Express",
            "Humsafar Express"
        ]

        self.coach_values = [
            "Choose",
            "First AC",
            "AC 2 Tier",
            "AC 3 Tier",
            "Sleeper",
            "Chair Car",
            "General"
        ]

        self.seat_values = ["Choose"] + [
            str(number) for number in range(1, 73)
        ]

        self.platform_values = [
            "Choose",
            "Platform 1",
            "Platform 2",
            "Platform 3",
            "Platform 4",
            "Platform 5",
            "Platform 6",
            "Platform 7",
            "Platform 8"
        ]

        self.route_values = [
            "Choose",
            "RT-101",
            "RT-102",
            "RT-103",
            "RT-104",
            "RT-105",
            "RT-106",
            "RT-107",
            "RT-108"
        ]

        self.fare_values = [
            "Choose",
            "₹250",
            "₹450",
            "₹650",
            "₹750",
            "₹950",
            "₹1,200",
            "₹1,500",
            "₹1,800",
            "₹2,100"
        ]

        self.station_values = [
            "Choose",
            "New Delhi",
            "Mumbai Central",
            "Lucknow",
            "Kanpur Central",
            "Varanasi",
            "Prayagraj",
            "Kolkata",
            "Jaipur",
            "Patna",
            "Bhopal",
            "Agra",
            "Chennai",
            "Bengaluru",
            "Hyderabad"
        ]

        self.create_database()
        self.create_ui()
        self.load_passengers()
        self.show_records()
        self.clear_fields()

    # ======================================================
    # DATABASE CONNECTION
    # ======================================================

    def connect_db(self, use_database=True):

        config = {
            "host": DB_HOST,
            "user": DB_USER,
            "password": DB_PASSWORD
        }

        if use_database:
            config["database"] = DB_NAME

        return mysql.connector.connect(**config)

    def create_database(self):

        try:
            connection = self.connect_db(False)
            cursor = connection.cursor()

            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
            )

            connection.commit()
            connection.close()

            connection = self.connect_db()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickets(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    train_name VARCHAR(100),
                    booking_ref VARCHAR(30) UNIQUE,
                    coach_type VARCHAR(40),
                    seat_number VARCHAR(20),
                    platform_name VARCHAR(40),
                    departure_date VARCHAR(30),
                    arrival_date VARCHAR(30),
                    travel_time VARCHAR(30),
                    route_no VARCHAR(30),
                    ticket_fare VARCHAR(30),
                    passenger_id VARCHAR(30),
                    contact_number VARCHAR(20),
                    passenger_name VARCHAR(100),
                    journey_from VARCHAR(60),
                    journey_to VARCHAR(60)
                )
            """)

            connection.commit()
            connection.close()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                f"MySQL connection nahi hua.\n\n{error}",
                parent=self.root
            )

    # ======================================================
    # USER INTERFACE
    # ======================================================

    def create_ui(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except TclError:
            pass

        style.configure(
            "Ticket.Treeview",
            font=("Arial", 9),
            rowheight=25
        )

        style.configure(
            "Ticket.Treeview.Heading",
            font=("Arial", 9, "bold")
        )

        # ---------------- Header ----------------

        header_frame = Frame(
            self.root,
            bg="#10232f",
            bd=4,
            relief=RIDGE
        )
        header_frame.pack(fill=X)

        Label(
            header_frame,
            text="INDIAN RAILWAY TICKET MANAGEMENT",
            font=("Times New Roman", 27, "bold"),
            bg="#10232f",
            fg="#f5c84c",
            pady=11
        ).pack()

        # ---------------- Main Frame ----------------

        main_frame = Frame(
            self.root,
            bg="#e5e5e5",
            bd=4,
            relief=RIDGE
        )
        main_frame.place(
            x=10,
            y=75,
            width=1330,
            height=365
        )

        booking_frame = LabelFrame(
            main_frame,
            text="Passenger Journey Information",
            font=("Arial", 11, "bold"),
            bg="#e5e5e5",
            fg="#10232f",
            bd=3,
            relief=RIDGE
        )
        booking_frame.place(
            x=8,
            y=7,
            width=930,
            height=342
        )

        ticket_summary_frame = LabelFrame(
            main_frame,
            text="Ticket Summary",
            font=("Arial", 11, "bold"),
            bg="#e5e5e5",
            fg="#10232f",
            bd=3,
            relief=RIDGE
        )
        ticket_summary_frame.place(
            x=947,
            y=7,
            width=370,
            height=342
        )

        # ---------------- Left Booking Fields ----------------

        left_fields = [
            ("Train Name", self.train_name, "train"),
            ("Booking Ref", self.booking_ref, "readonly"),
            ("Coach Type", self.coach_type, "coach"),
            ("Seat Number", self.seat_number, "seat"),
            ("Platform Name", self.platform_name, "platform"),
            ("Departure Date", self.departure_date, "normal"),
            ("Arrival Date", self.arrival_date, "normal"),
            ("Travel Time", self.travel_time, "normal"),
            ("Route No.", self.route_no, "route")
        ]

        for row, (text, variable, field_type) in enumerate(left_fields):

            Label(
                booking_frame,
                text=text,
                font=("Arial", 9, "bold"),
                bg="#e5e5e5",
                fg="#111111"
            ).grid(
                row=row,
                column=0,
                padx=(12, 8),
                pady=5,
                sticky=W
            )

            if field_type == "train":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.train_values
                )

            elif field_type == "coach":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.coach_values
                )

            elif field_type == "seat":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.seat_values
                )

            elif field_type == "platform":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.platform_values
                )

            elif field_type == "route":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.route_values
                )

            else:
                field = Entry(
                    booking_frame,
                    textvariable=variable,
                    font=("Arial", 9),
                    width=26,
                    bd=2,
                    relief=GROOVE,
                    state=field_type
                )

            field.grid(
                row=row,
                column=1,
                padx=8,
                pady=5
            )

        # ---------------- Right Booking Fields ----------------

        right_fields = [
            ("Ticket Fare", self.ticket_fare, "fare"),
            ("Select Passenger", self.passenger_choice, "passenger"),
            ("Passenger ID", self.passenger_id, "readonly"),
            ("Contact Number", self.contact_number, "normal"),
            ("Passenger Name", self.passenger_name, "normal"),
            ("Journey From", self.journey_from, "station"),
            ("Journey To", self.journey_to, "station")
        ]

        for row, (text, variable, field_type) in enumerate(right_fields):

            Label(
                booking_frame,
                text=text,
                font=("Arial", 9, "bold"),
                bg="#e5e5e5",
                fg="#111111"
            ).grid(
                row=row,
                column=2,
                padx=(35, 8),
                pady=7,
                sticky=W
            )

            if field_type == "fare":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.fare_values
                )

            elif field_type == "station":
                field = self.make_combo(
                    booking_frame,
                    variable,
                    self.station_values
                )

            elif field_type == "passenger":

                self.passenger_box = ttk.Combobox(
                    booking_frame,
                    textvariable=variable,
                    values=["Choose"],
                    state="readonly",
                    font=("Arial", 9),
                    width=25
                )

                self.passenger_box.bind(
                    "<<ComboboxSelected>>",
                    self.fill_passenger_details
                )

                field = self.passenger_box

            else:
                field = Entry(
                    booking_frame,
                    textvariable=variable,
                    font=("Arial", 9),
                    width=26,
                    bd=2,
                    relief=GROOVE,
                    state=field_type
                )

            field.grid(
                row=row,
                column=3,
                padx=8,
                pady=7
            )

        # Passenger Refresh Button

        Button(
            booking_frame,
            text="Refresh Passenger",
            command=self.load_passengers,
            font=("Arial", 9, "bold"),
            bg="#1f6f78",
            fg="white",
            activebackground="#278994",
            activeforeground="white",
            cursor="hand2",
            bd=1
        ).grid(
            row=7,
            column=2,
            columnspan=2,
            pady=5
        )

        # ---------------- Ticket Summary ----------------

        self.ticket_text = Text(
            ticket_summary_frame,
            font=("Courier New", 9, "bold"),
            bg="white",
            fg="#10232f",
            bd=2,
            relief=SUNKEN,
            padx=8,
            pady=8,
            wrap=WORD
        )

        self.ticket_text.pack(
            fill=BOTH,
            expand=True,
            padx=7,
            pady=7
        )

        # ---------------- Buttons ----------------

        button_frame = Frame(
            self.root,
            bg="#10232f",
            bd=3,
            relief=RIDGE
        )

        button_frame.place(
            x=10,
            y=445,
            width=1330,
            height=62
        )

        buttons = [
            ("Generate Ticket", self.generate_ticket),
            ("Save Record", self.save_record),
            ("Update", self.update_record),
            ("Delete", self.delete_record),
            ("Clear", self.clear_fields),
            ("Exit", self.root.destroy)
        ]

        for text, command in buttons:

            Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                bg="#087f5b",
                fg="white",
                activebackground="#0ca678",
                activeforeground="white",
                cursor="hand2",
                bd=2,
                width=18
            ).pack(
                side=LEFT,
                expand=True,
                fill=X,
                padx=5,
                pady=9
            )

        # ---------------- Compact Table ----------------

        table_frame = Frame(
            self.root,
            bg="white",
            bd=4,
            relief=RIDGE
        )

        table_frame.place(
            x=10,
            y=512,
            width=1330,
            height=228
        )

        scroll_x = Scrollbar(
            table_frame,
            orient=HORIZONTAL
        )

        scroll_y = Scrollbar(
            table_frame,
            orient=VERTICAL
        )

        self.table_columns = (
            "train_name",
            "booking_ref",
            "coach_type",
            "seat_number",
            "platform_name",
            "departure_date",
            "arrival_date",
            "travel_time",
            "route_no",
            "ticket_fare",
            "passenger_id",
            "contact_number",
            "passenger_name",
            "journey_from",
            "journey_to"
        )

        self.ticket_table = ttk.Treeview(
            table_frame,
            columns=self.table_columns,
            show="headings",
            style="Ticket.Treeview",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            height=6
        )

        headings = {
            "train_name": "Train Name",
            "booking_ref": "Booking Ref",
            "coach_type": "Coach Type",
            "seat_number": "Seat Number",
            "platform_name": "Platform Name",
            "departure_date": "Departure Date",
            "arrival_date": "Arrival Date",
            "travel_time": "Travel Time",
            "route_no": "Route No.",
            "ticket_fare": "Ticket Fare",
            "passenger_id": "Passenger ID",
            "contact_number": "Contact Number",
            "passenger_name": "Passenger Name",
            "journey_from": "Journey From",
            "journey_to": "Journey To"
        }

        column_widths = {
            "train_name": 125,
            "booking_ref": 95,
            "coach_type": 90,
            "seat_number": 80,
            "platform_name": 95,
            "departure_date": 100,
            "arrival_date": 90,
            "travel_time": 85,
            "route_no": 75,
            "ticket_fare": 80,
            "passenger_id": 90,
            "contact_number": 105,
            "passenger_name": 115,
            "journey_from": 105,
            "journey_to": 105
        }

        for column in self.table_columns:

            self.ticket_table.heading(
                column,
                text=headings[column]
            )

            self.ticket_table.column(
                column,
                width=column_widths[column],
                minwidth=70,
                anchor=CENTER,
                stretch=False
            )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.ticket_table.xview)
        scroll_y.config(command=self.ticket_table.yview)

        self.ticket_table.pack(
            fill=BOTH,
            expand=True
        )

        self.ticket_table.bind(
            "<ButtonRelease-1>",
            self.get_selected_record
        )

    def make_combo(self, parent, variable, values):

        return ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            font=("Arial", 9),
            width=25
        )

    # ======================================================
    # AUTO GENERATE IDS
    # ======================================================

    def generate_booking_ref(self):

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT MAX(id) FROM tickets"
            )

            result = cursor.fetchone()
            connection.close()

            last_id = result[0] if result and result[0] else 0

            return f"BK{100001 + last_id}"

        except mysql.connector.Error:
            return "BK100001"

    def generate_passenger_id(self):

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT MAX(id) FROM tickets"
            )

            result = cursor.fetchone()
            connection.close()

            last_id = result[0] if result and result[0] else 0

            return f"P{1001 + last_id}"

        except mysql.connector.Error:
            return "P1001"

    # ======================================================
    # PASSENGER DATABASE
    # ======================================================

    def find_passenger_table(self, cursor):

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema=%s
        """, (DB_NAME,))

        available_tables = [
            row[0].lower() for row in cursor.fetchall()
        ]

        candidates = [
            "passengers",
            "passenger",
            "passenger_details",
            "passenger_records"
        ]

        for table in candidates:
            if table in available_tables:
                return table

        return None

    def find_column(self, columns, candidates):

        lowercase_columns = {
            column.lower(): column for column in columns
        }

        for candidate in candidates:

            if candidate.lower() in lowercase_columns:
                return lowercase_columns[candidate.lower()]

        return None

    def load_passengers(self):

     self.passenger_records.clear()
     passenger_list = ["Choose"]

     try:
            connection = self.connect_db()
            cursor = connection.cursor()

            table_name = self.find_passenger_table(cursor)

            if not table_name:
                self.passenger_box["values"] = passenger_list
                self.passenger_choice.set("Choose")
                connection.close()
                return

            cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")

            columns = [
                row[0] for row in cursor.fetchall()
            ]

            id_column = self.find_column(
                columns,
                [
                    "passenger_id",
                    "passengerid",
                    "p_id",
                    "id"
                ]
            )

            name_column = self.find_column(
                columns,
                [
                    "passenger_name",
                    "name",
                    "full_name",
                    "p_name"
                ]
            )

            contact_column = self.find_column(
                columns,
                [
                    "contact_number",
                    "contact",
                    "phone",
                    "mobile",
                    "phone_number"
                ]
            )

            if not id_column or not name_column:

                self.passenger_box["values"] = passenger_list
                self.passenger_choice.set("Choose")
                connection.close()
                return

            if contact_column:

                query = f"""
                    SELECT
                        `{id_column}`,
                        `{name_column}`,
                        `{contact_column}`
                    FROM `{table_name}`
                    ORDER BY `{name_column}`
                """

            else:

                query = f"""
                    SELECT
                        `{id_column}`,
                        `{name_column}`,
                        ''
                    FROM `{table_name}`
                    ORDER BY `{name_column}`
                """

            cursor.execute(query)

            rows = cursor.fetchall()
            connection.close()

            for passenger_id, name, contact in rows:

                display_text = f"{passenger_id} - {name}"

                passenger_list.append(display_text)

                self.passenger_records[display_text] = {
                    "passenger_id": passenger_id,
                    "name": name,
                    "contact": contact or ""
                }

            self.passenger_box["values"] = passenger_list
            self.passenger_choice.set("Choose")

     except mysql.connector.Error:

            self.passenger_box["values"] = passenger_list
            self.passenger_choice.set("Choose")

    def fill_passenger_details(self, event=None):

        selected_passenger = self.passenger_choice.get()

        if selected_passenger not in self.passenger_records:
            return

        data = self.passenger_records[selected_passenger]

        self.passenger_id.set(data["passenger_id"])
        self.passenger_name.set(data["name"])
        self.contact_number.set(data["contact"])

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate_fields(self):

        required_fields = {
            "Train Name": self.train_name.get(),
            "Booking Reference": self.booking_ref.get(),
            "Coach Type": self.coach_type.get(),
            "Seat Number": self.seat_number.get(),
            "Platform Name": self.platform_name.get(),
            "Departure Date": self.departure_date.get(),
            "Route Number": self.route_no.get(),
            "Ticket Fare": self.ticket_fare.get(),
            "Passenger ID": self.passenger_id.get(),
            "Contact Number": self.contact_number.get(),
            "Passenger Name": self.passenger_name.get(),
            "Journey From": self.journey_from.get(),
            "Journey To": self.journey_to.get()
        }

        for field_name, value in required_fields.items():

            if not value.strip() or value == "Choose":

                messagebox.showwarning(
                    "Required Field",
                    f"Please {field_name} fill ya choose karo.",
                    parent=self.root
                )

                return False

        if self.journey_from.get() == self.journey_to.get():

            messagebox.showwarning(
                "Invalid Journey",
                "Journey From aur Journey To same nahi ho sakte.",
                parent=self.root
            )

            return False

        if not self.contact_number.get().isdigit():

            messagebox.showwarning(
                "Invalid Contact",
                "Contact Number me sirf numbers enter karo.",
                parent=self.root
            )

            return False

        if len(self.contact_number.get()) != 10:

            messagebox.showwarning(
                "Invalid Contact",
                "Contact Number 10 digits ka hona chahiye.",
                parent=self.root
            )

            return False

        return True

    # ======================================================
    # GENERATE TICKET
    # ======================================================

    def generate_ticket(self):

        if not self.validate_fields():
            return

        ticket = f"""
================================
       INDIAN RAILWAY TICKET
================================

Booking Ref : {self.booking_ref.get()}
Train Name  : {self.train_name.get()}
Coach Type  : {self.coach_type.get()}
Seat Number : {self.seat_number.get()}

Passenger ID: {self.passenger_id.get()}
Passenger   : {self.passenger_name.get()}
Contact No. : {self.contact_number.get()}

Journey From: {self.journey_from.get()}
Journey To  : {self.journey_to.get()}

Platform    : {self.platform_name.get()}
Route No.   : {self.route_no.get()}
Departure   : {self.departure_date.get()}
Arrival     : {self.arrival_date.get()}
Travel Time : {self.travel_time.get()}

Ticket Fare : {self.ticket_fare.get()}

================================
          HAPPY JOURNEY
================================
"""

        self.ticket_text.delete("1.0", END)
        self.ticket_text.insert(END, ticket)

    # ======================================================
    # DATABASE VALUES
    # ======================================================

    def get_all_values(self):

        return (
            self.train_name.get(),
            self.booking_ref.get(),
            self.coach_type.get(),
            self.seat_number.get(),
            self.platform_name.get(),
            self.departure_date.get(),
            self.arrival_date.get(),
            self.travel_time.get(),
            self.route_no.get(),
            self.ticket_fare.get(),
            self.passenger_id.get(),
            self.contact_number.get(),
            self.passenger_name.get(),
            self.journey_from.get(),
            self.journey_to.get()
        )

    # ======================================================
    # SAVE
    # ======================================================

    
    def save_record(self):

        if not self.validate_fields():
            return 

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

        # ===== CHECK AVAILABLE SEATS =====

            cursor.execute("""
               SELECT available_seats
               FROM trains
               WHERE train_name=%s
               """, (self.train_name.get(),))

            result = cursor.fetchone()       
            if not result:
              messagebox.showerror(
              "Error",
              "Train not found.",
                parent=self.root
            )
            connection.close()
            return

            if result[0] <= 0:
              messagebox.showerror(
              "No Seats",
              "No seat available for booking.",
               parent=self.root
            )
            connection.close()
            return

# ===== DECREASE AVAILABLE SEAT =====

            cursor.execute("""
            UPDATE trains
            SET available_seats = available_seats - 1
            WHERE train_name=%s
            """, (self.train_name.get(),))
              
            
            cursor.execute("""
                INSERT INTO tickets(
                    train_name,
                    booking_ref,
                    coach_type,
                    seat_number,
                    platform_name,
                    departure_date,
                    arrival_date,
                    travel_time,
                    route_no,
                    ticket_fare,
                    passenger_id,
                    contact_number,
                    passenger_name,
                    journey_from,
                    journey_to
                )
                VALUES(
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
            """, self.get_all_values())

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Saved",
                "Ticket record successfully save ho gaya.",
                parent=self.root
            )

            self.show_records()
            self.clear_fields()

        except mysql.connector.IntegrityError:

            messagebox.showerror(
                "Duplicate Booking",
                "Ye Booking Reference already database me hai.",
                parent=self.root
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.root
            )

    # ======================================================
    # SHOW RECORDS
    # ======================================================

    def show_records(self):

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    train_name,
                    booking_ref,
                    coach_type,
                    seat_number,
                    platform_name,
                    departure_date,
                    arrival_date,
                    travel_time,
                    route_no,
                    ticket_fare,
                    passenger_id,
                    contact_number,
                    passenger_name,
                    journey_from,
                    journey_to
                FROM tickets
                ORDER BY id DESC
            """)

            records = cursor.fetchall()
            connection.close()

            self.ticket_table.delete(
                *self.ticket_table.get_children()
            )

            for record in records:

                self.ticket_table.insert(
                    "",
                    END,
                    values=record
                )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Ticket records load nahi hue.\n\n{error}",
                parent=self.root
            )

    # ======================================================
    # SELECT TABLE RECORD
    # ======================================================

    def get_selected_record(self, event=None):

        selected_items = self.ticket_table.selection()

        if not selected_items:
            return

        values = self.ticket_table.item(
            selected_items[0],
            "values"
        )

        if not values or len(values) < 15:
            return

        self.train_name.set(values[0])
        self.booking_ref.set(values[1])
        self.coach_type.set(values[2])
        self.seat_number.set(values[3])
        self.platform_name.set(values[4])
        self.departure_date.set(values[5])
        self.arrival_date.set(values[6])
        self.travel_time.set(values[7])
        self.route_no.set(values[8])
        self.ticket_fare.set(values[9])
        self.passenger_id.set(values[10])
        self.contact_number.set(values[11])
        self.passenger_name.set(values[12])
        self.journey_from.set(values[13])
        self.journey_to.set(values[14])

        self.selected_booking_ref = values[1]

        passenger_display = (
            f"{self.passenger_id.get()} - "
            f"{self.passenger_name.get()}"
        )

        if passenger_display in self.passenger_records:
            self.passenger_choice.set(passenger_display)
        else:
            self.passenger_choice.set("Choose")

        self.generate_ticket()

    # ======================================================
    # UPDATE
    # ======================================================

    def update_record(self):

        if not self.selected_booking_ref:

            messagebox.showwarning(
                "Select Ticket",
                "Update karne ke liye table se ticket select karo.",
                parent=self.root
            )

            return

        if not self.validate_fields():
            return

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            update_values = self.get_all_values() + (
                self.selected_booking_ref,
            )

            cursor.execute("""
                UPDATE tickets SET
                    train_name=%s,
                    booking_ref=%s,
                    coach_type=%s,
                    seat_number=%s,
                    platform_name=%s,
                    departure_date=%s,
                    arrival_date=%s,
                    travel_time=%s,
                    route_no=%s,
                    ticket_fare=%s,
                    passenger_id=%s,
                    contact_number=%s,
                    passenger_name=%s,
                    journey_from=%s,
                    journey_to=%s
                WHERE booking_ref=%s
            """, update_values)

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Updated",
                "Ticket successfully update ho gaya.",
                parent=self.root
            )

            self.show_records()
            self.clear_fields()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.root
            )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_record(self):

        if not self.selected_booking_ref:

            messagebox.showwarning(
                "Select Ticket",
                "Delete karne ke liye table se ticket select karo.",
                parent=self.root
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Kya selected ticket delete karna hai?",
            parent=self.root
        )

        if not confirm:
            return

        try:
            connection = self.connect_db()
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM tickets WHERE booking_ref=%s",
                (self.selected_booking_ref,)
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Deleted",
                "Ticket record delete ho gaya.",
                parent=self.root
            )

            self.show_records()
            self.clear_fields()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.root
            )

    # ======================================================
    # CLEAR
    # ======================================================

    def clear_fields(self):

        self.selected_booking_ref = None

        # Default IDs
        self.booking_ref.set(
            self.generate_booking_ref()
        )

        self.passenger_id.set(
            self.generate_passenger_id()
        )

        # Dropdown defaults
        self.train_name.set("Choose")
        self.coach_type.set("Choose")
        self.seat_number.set("Choose")
        self.platform_name.set("Choose")
        self.route_no.set("Choose")
        self.ticket_fare.set("Choose")
        self.journey_from.set("Choose")
        self.journey_to.set("Choose")
        self.passenger_choice.set("Choose")

        # Normal entries
        self.contact_number.set("")
        self.passenger_name.set("")

        self.departure_date.set(
            date.today().strftime("%d-%m-%Y")
        )

        self.arrival_date.set("")
        self.travel_time.set("")

        self.ticket_text.delete("1.0", END)

        for item in self.ticket_table.selection():
            self.ticket_table.selection_remove(item)


# ======================================================
# DIRECT RUN
# ======================================================
class Ticket(TicketPage):
    pass
if __name__ == "__main__":

    root = Tk()
    app = TicketPage(root)
    root.mainloop()