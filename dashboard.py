from tkinter import *
from tkinter import messagebox
import importlib
import os
import sys
from ticket import TicketPage


class RailwayDashboard:
    def __init__(self, root, username="admin"):
        self.root = root
        self.username = username
        self.root.title("Railway Management System - Dashboard")
        self.root.geometry("1350x720+0+0")
        self.root.minsize(1100, 650)
        self.root.configure(bg="#071c2c")

        # ==================== COLORS ====================
        self.dark_blue = "#071c2c"
        self.sidebar_color = "#0b2a40"
        self.header_color = "#061722"
        self.card_color = "#123b55"
        self.button_color = "#164f70"
        self.button_hover = "#1c6b93"
        self.white = "#ffffff"
        self.light_text = "#dceaf2"
        self.accent = "#19a7ce"
        self.logout_color = "#b3261e"

        # File location of dashboard.py
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Opened child windows
        self.opened_windows = {}

        self.create_header()
        self.create_sidebar()
        self.create_main_content()

    # =====================================================
    # HEADER
    # =====================================================
    def create_header(self):
        self.header_frame = Frame(
            self.root,
            bg=self.header_color,
            height=80
        )
        self.header_frame.pack(
            side=TOP,
            fill=X
        )
        self.header_frame.pack_propagate(False)

        logo_label = Label(
            self.header_frame,
            text="🚆",
            font=("Arial", 34),
            bg=self.header_color,
            fg=self.white
        )
        logo_label.pack(
            side=LEFT,
            padx=(25, 10)
        )

        title_frame = Frame(
            self.header_frame,
            bg=self.header_color
        )
        title_frame.pack(
            side=LEFT,
            pady=10
        )

        title_label = Label(
            title_frame,
            text="RAILWAY MANAGEMENT SYSTEM",
            font=("Arial", 22, "bold"),
            bg=self.header_color,
            fg=self.white
        )
        title_label.pack(
            anchor="w"
        )

        subtitle_label = Label(
            title_frame,
            text="Admin Dashboard",
            font=("Arial", 11),
            bg=self.header_color,
            fg=self.accent
        )
        subtitle_label.pack(
            anchor="w"
        )

        admin_label = Label(
            self.header_frame,
            text="Welcome, Admin",
            font=("Arial", 12, "bold"),
            bg=self.header_color,
            fg=self.light_text
        )
        admin_label.pack(
            side=RIGHT,
            padx=30
        )

    # =====================================================
    # SIDEBAR
    # =====================================================
    def create_sidebar(self):
        self.sidebar_frame = Frame(
            self.root,
            bg=self.sidebar_color,
            width=260
        )
        self.sidebar_frame.pack(
            side=LEFT,
            fill=Y
        )
        self.sidebar_frame.pack_propagate(False)

        menu_heading = Label(
            self.sidebar_frame,
            text="MAIN MENU",
            font=("Arial", 12, "bold"),
            bg=self.sidebar_color,
            fg=self.accent
        )
        menu_heading.pack(
            anchor="w",
            padx=25,
            pady=(30, 15)
        )

        self.create_menu_button(
            text="🏠   Dashboard",
            command=self.show_dashboard
        )

        self.create_menu_button(
            text="👤   Passenger",
            command=lambda: self.open_page(
                file_name="passenger",
                class_name="Passenger",
                page_title="Passenger Management"
            )
        )

        self.create_menu_button(
            text="🚆   Train",
            command=lambda: self.open_page(
                file_name="train",
                class_name="Train",
                page_title="Train Management"
            )
        )

        self.create_menu_button(
            text="🎫   Ticket Booking",
            command=lambda: self.open_page(
                file_name="ticket",
                class_name="TicketPage",
                page_title="Ticket Booking"
            )
        )

        self.create_menu_button(
            text="📅   Train Schedule",
            command=lambda: self.open_page(
                file_name="schedule",
                class_name="Schedule",
                page_title="Train Schedule"
            )
        )

        self.create_menu_button(
            text="💳   Payment",
            command=lambda: self.open_page(
                file_name="payment",
                class_name="Payment",
                page_title="Payment"
            )
        )

        self.create_menu_button(
            text="📊   Reports",
            command=lambda: self.open_page(
                file_name="report",
                class_name="Report",
                page_title="Reports"
            )
        )

        logout_button = Button(
            self.sidebar_frame,
            text="🚪   Logout",
            font=("Arial", 12, "bold"),
            bg=self.logout_color,
            fg=self.white,
            activebackground="#8c1d18",
            activeforeground=self.white,
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=25,
            command=self.logout
        )
        logout_button.pack(
            side=BOTTOM,
            fill=X,
            padx=15,
            pady=25,
            ipady=12
        )

    # =====================================================
    # SIDEBAR BUTTON
    # =====================================================
    def create_menu_button(self, text, command):
        button = Button(
            self.sidebar_frame,
            text=text,
            font=("Arial", 12, "bold"),
            bg=self.sidebar_color,
            fg=self.light_text,
            activebackground=self.button_hover,
            activeforeground=self.white,
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=25,
            command=command
        )
        button.pack(
            fill=X,
            padx=10,
            pady=3,
            ipady=12
        )

        button.bind(
            "<Enter>",
            lambda event, btn=button: btn.config(
                bg=self.button_hover
            )
        )

        button.bind(
            "<Leave>",
            lambda event, btn=button: btn.config(
                bg=self.sidebar_color
            )
        )

    # =====================================================
    # MAIN CONTENT
    # =====================================================
    def create_main_content(self):
        self.main_frame = Frame(
            self.root,
            bg=self.dark_blue
        )
        self.main_frame.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        self.show_dashboard()

    # =====================================================
    # DASHBOARD HOME
    # =====================================================
    def show_dashboard(self):
        self.clear_main_frame()

        heading_label = Label(
            self.main_frame,
            text="Dashboard Overview",
            font=("Arial", 26, "bold"),
            bg=self.dark_blue,
            fg=self.white
        )
        heading_label.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        description_label = Label(
            self.main_frame,
            text="Manage passengers, trains, bookings and railway records.",
            font=("Arial", 12),
            bg=self.dark_blue,
            fg=self.light_text
        )
        description_label.pack(
            anchor="w",
            padx=37,
            pady=(0, 25)
        )

        cards_frame = Frame(
            self.main_frame,
            bg=self.dark_blue
        )
        cards_frame.pack(
            fill=X,
            padx=25
        )

        for column in range(3):
            cards_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="cards",
                minsize=320
            )

        self.create_dashboard_card(
            parent=cards_frame,
            row=0,
            column=0,
            icon="👤",
            title="Passengers",
            value="Manage",
            command=lambda: self.open_page(
                "passenger",
                "Passenger",
                "Passenger Management"
            )
        )

        self.create_dashboard_card(
            parent=cards_frame,
            row=0,
            column=1,
            icon="🚆",
            title="Trains",
            value="Manage",
            command=lambda: self.open_page(
                "train",
                "Train",
                "Train Management"
            )
        )

        self.create_dashboard_card(
            parent=cards_frame,
            row=0,
            column=2,
            icon="📄",
            title="Tickets",
            value="View",
            command=lambda: self.open_page(
                "ticket",
                "Ticket",
                "Ticket Details"
            )
        )

        quick_frame = Frame(
            self.main_frame,
            bg=self.card_color,
            bd=0,
            highlightthickness=1,
            highlightbackground="#24536b"
        )
        quick_frame.pack(
            fill=BOTH,
            expand=TRUE,
            padx=35,
            pady=30
        )

        quick_title = Label(
            quick_frame,
            text="Quick Actions",
            font=("Arial", 18, "bold"),
            bg=self.card_color,
            fg=self.white
        )
        quick_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        quick_buttons_frame = Frame(
            quick_frame,
            bg=self.card_color
        )
        quick_buttons_frame.pack(
            fill=X,
            padx=20,
            pady=(0, 20)
        )

        for column in range(3):
            quick_buttons_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.create_quick_button(
            quick_buttons_frame,
            "Add Passenger",
            0,
            0,
            lambda: self.open_page(
                "passenger",
                "Passenger",
                "Passenger Management"
            )
        )

        self.create_quick_button(
            quick_buttons_frame,
            "Add Train",
            0,
            1,
            lambda: self.open_page(
                "train",
                "Train",
                "Train Management"
            )
        )

        self.create_quick_button(
            quick_buttons_frame,
            "View Tickets",
            0,
            2,
            lambda: self.open_page(
                "ticket",
                "Ticket",
                "Ticket Details"
            )
        )

        self.create_quick_button(
            quick_buttons_frame,
            "Train Schedule",
            1,
            0,
            lambda: self.open_page(
                "schedule",
                "Schedule",
                "Train Schedule"
            )
        )

        self.create_quick_button(
            quick_buttons_frame,
            "View Reports",
            1,
            1,
            lambda: self.open_page(
                "report",
                "Report",
                "Reports"
            )
        )

    # =====================================================
    # DASHBOARD CARD
    # =====================================================
    def create_dashboard_card(
        self,
        parent,
        row,
        column,
        icon,
        title,
        value,
        command
    ):
        card = Frame(
            parent,
            bg=self.card_color,
            height=145,
            width=280,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground="#24536b"
        )
        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=10,
            pady=10
        )
        card.grid_propagate(False)

        icon_label = Label(
            card,
            text=icon,
            font=("Arial", 28),
            bg=self.card_color,
            fg=self.white
        )
        icon_label.pack(
            pady=(18, 2)
        )

        title_label = Label(
            card,
            text=title,
            font=("Arial", 13, "bold"),
            bg=self.card_color,
            fg=self.white
        )
        title_label.pack()

        value_label = Label(
            card,
            text=value,
            font=("Arial", 10),
            bg=self.card_color,
            fg=self.accent
        )
        value_label.pack(
            pady=3
        )

        widgets = [
            card,
            icon_label,
            title_label,
            value_label
        ]

        for widget in widgets:
            widget.bind(
                "<Button-1>",
                lambda event, cmd=command: cmd()
            )

            widget.bind(
                "<Enter>",
                lambda event, frame=card: frame.config(
                    bg=self.button_color
                )
            )

            widget.bind(
                "<Leave>",
                lambda event, frame=card: frame.config(
                    bg=self.card_color
                )
            )

    # =====================================================
    # QUICK ACTION BUTTON
    # =====================================================
    def create_quick_button(
        self,
        parent,
        text,
        row,
        column,
        command
    ):
        button = Button(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg=self.button_color,
            fg=self.white,
            activebackground=self.button_hover,
            activeforeground=self.white,
            bd=0,
            cursor="hand2",
            command=command
        )
        button.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=10,
            pady=10,
            ipady=13
        )

    # =====================================================
    # DYNAMIC PAGE LOADER
    # =====================================================
    def open_page(
        self,
        file_name,
        class_name,
        page_title
    ):
        try:
            file_path = os.path.join(
                self.base_path,
                file_name + ".py"
            )

            # File not created yet
            if not os.path.exists(file_path):
                messagebox.showinfo(
                    "Page Not Available",
                    f"{page_title} page abhi create nahi hua hai.\n\n"
                    f"Baad me '{file_name}.py' file create karne par "
                    f"ye button automatically connect ho jayega."
                )
                return

            # Ensure project folder is in Python path
            if self.base_path not in sys.path:
                sys.path.insert(
                    0,
                    self.base_path
                )

            # Import module dynamically
            if file_name in sys.modules:
                module = importlib.reload(
                    sys.modules[file_name]
                )
            else:
                module = importlib.import_module(
                    file_name
                )

            # Check class exists
            if not hasattr(module, class_name):
                messagebox.showerror(
                    "Class Not Found",
                    f"'{file_name}.py' file mil gayi hai,\n"
                    f"lekin uske andar '{class_name}' class nahi mili.\n\n"
                    f"Class ka naam exact '{class_name}' rakho."
                )
                return

            page_class = getattr(
                module,
                class_name
            )

            # Close old window of same page
            if file_name in self.opened_windows:
                old_window = self.opened_windows[file_name]

                if old_window.winfo_exists():
                    old_window.lift()
                    old_window.focus_force()
                    return

            new_window = Toplevel(
                self.root
            )

            self.opened_windows[file_name] = new_window

            new_window.protocol(
                "WM_DELETE_WINDOW",
                lambda: self.close_child_window(
                    file_name,
                    new_window
                )
            )

            # Open target page
            page_class(new_window)

        except ModuleNotFoundError as error:
            messagebox.showerror(
                "Import Error",
                f"{page_title} open nahi hua.\n\n"
                f"Required module nahi mila:\n{error}"
            )

        except TypeError as error:
            messagebox.showerror(
                "Class Error",
                f"{page_title} ki class ka structure sahi nahi hai.\n\n"
                f"Class me constructor aisa hona chahiye:\n"
                f"def __init__(self, root):\n\n"
                f"Error: {error}"
            )

        except Exception as error:
            messagebox.showerror(
                "Page Error",
                f"{page_title} page open nahi ho raha.\n\n"
                f"Error: {error}"
            )

    # =====================================================
    # CLOSE CHILD WINDOW
    # =====================================================
    def close_child_window(
        self,
        file_name,
        window
    ):
        try:
            if window.winfo_exists():
                window.destroy()
        except Exception:
            pass

        self.opened_windows.pop(
            file_name,
            None
        )

    # =====================================================
    # CLEAR MAIN FRAME
    # =====================================================
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =====================================================
    # LOGOUT
    # =====================================================
    def logout(self):
        answer = messagebox.askyesno(
            "Logout",
            "Kya aap logout karna chahte hain?"
        )

        if answer:
            self.root.destroy()

            try:
                if self.base_path not in sys.path:
                    sys.path.insert(
                        0,
                        self.base_path
                    )

                if os.path.exists(
                    os.path.join(
                        self.base_path,
                        "login.py"
                    )
                ):
                    login_module = importlib.import_module(
                        "login"
                    )
                    importlib.reload(
                        login_module
                    )

            except Exception:
                pass


# =========================================================
# RUN DASHBOARD
# =========================================================
if __name__ == "__main__":
    root = Tk()
    app = RailwayDashboard(root)
    root.mainloop()
    DashboardWindow = RailwayDashboard