import os
import tkinter as tk
from tkinter import messagebox

import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk

from config import HOST, USER, PASSWORD, DATABASE, PORT


class LoginWindow:
    def __init__(self, root):
        self.root = root

        # Fixed window
        self.root.title("Railway Management System - Login")
        self.root.geometry("1200x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#071725")

        # Login variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar(value=False)

        self.background_photo = None

        self.load_background()
        self.create_login_card()

        # Enter दबाने पर Login
        self.root.bind("<Return>", lambda event: self.login())

    # =====================================================
    # BACKGROUND IMAGE
    # =====================================================
    def load_background(self):
        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "train.jpg"
        )

        try:
            image = Image.open(image_path)

            # Image को exact window size पर fit करना
            image = image.resize(
                (1200, 680),
                Image.Resampling.LANCZOS
            )

            self.background_photo = ImageTk.PhotoImage(image)

            background_label = tk.Label(
                self.root,
                image=self.background_photo,
                bd=0
            )
            background_label.place(
                x=0,
                y=0,
                width=1200,
                height=680
            )

        except FileNotFoundError:
            messagebox.showerror(
                "Image Error",
                "train.jpg नहीं मिली।\n\n"
                "Image इस location पर रखो:\n"
                "images/train.jpg"
            )
            self.root.destroy()

        except Exception as error:
            messagebox.showerror(
                "Image Error",
                f"Image load नहीं हुई:\n{error}"
            )
            self.root.destroy()

    # =====================================================
    # LOGIN CARD
    # =====================================================
    def create_login_card(self):
        self.login_frame = tk.Frame(
            self.root,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#d6d9dd"
        )

        # Right side fixed position
        self.login_frame.place(
            x=720,
            y=220,
            width=440,
            height=430
        )

        # ---------------- Heading ----------------
        title_label = tk.Label(
            self.login_frame,
            text="Login",
            font=("Segoe UI", 27, "bold"),
            bg="white",
            fg="#040D14"
        )
        title_label.pack(pady=(25, 3))

        subtitle_label = tk.Label(
            self.login_frame,
            text="Use admin / admin123 first time",
            font=("Segoe UI", 10),
            bg="white",
            fg="#22262D"
        )
        subtitle_label.pack(pady=(0, 20))

        # ---------------- Username ----------------
        username_label = tk.Label(
            self.login_frame,
            text="Username",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#111827",
            anchor="w"
        )
        username_label.pack(
            fill="x",
            padx=38,
            pady=(0, 5)
        )

        username_box = tk.Frame(
            self.login_frame,
            bg="white",
            highlightthickness=1,
            highlightbackground="#bfc5ca"
        )
        username_box.pack(
            fill="x",
            padx=38
        )

        username_icon = tk.Label(
            username_box,
            text="👤",
            font=("Segoe UI Emoji", 13),
            bg="white",
            fg="#405366",
            width=3
        )
        username_icon.pack(
            side="left",
            padx=(4, 0)
        )

        self.username_entry = tk.Entry(
            username_box,
            textvariable=self.username_var,
            font=("Segoe UI", 12),
            bg="white",
            fg="#111827",
            insertbackground="#111827",
            bd=0,
            relief="flat"
        )
 
            
        self.username_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(2, 10),
            ipady=10
        )
        
        # ---------------- Password ----------------
        password_label = tk.Label(
            self.login_frame,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#111827",
            anchor="w"
        )
        password_label.pack(
            fill="x",
            padx=38,
            pady=(17, 5)
        )

        password_box = tk.Frame(
            self.login_frame,
            bg="white",
            highlightthickness=1,
            highlightbackground="#bfc5ca"
        )
        password_box.pack(
            fill="x",
            padx=38
        )

        password_icon = tk.Label(
            password_box,
            text="🔒",
            font=("Segoe UI Emoji", 13),
            bg="white",
            fg="#405366",
            width=3
        )
        password_icon.pack(
            side="left",
            padx=(4, 0)
        )

        self.password_entry = tk.Entry(
            password_box,
            textvariable=self.password_var,
            font=("Segoe UI", 12),
            bg="white",
            fg="#111827",
            insertbackground="#111827",
            show="●",
            bd=0,
            relief="flat"
        )
        self.password_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(2, 10),
            ipady=10
        )

        # ---------------- Show Password ----------------
        show_password_check = tk.Checkbutton(
            self.login_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=("Segoe UI", 10),
            bg="white",
            fg="#111827",
            activebackground="white",
            activeforeground="#111827",
            selectcolor="white",
            cursor="hand2",
            bd=0
        )
        show_password_check.pack(
            anchor="w",
            padx=34,
            pady=(12, 16)
        )

        # ---------------- Login Button ----------------
        login_button = tk.Button(
            self.login_frame,
            text="⇥   LOGIN TO SYSTEM",
            command=self.login,
            font=("Segoe UI", 13, "bold"),
            bg="#087f4c",
            fg="white",
            activebackground="#06693e",
            activeforeground="white",
            cursor="hand2",
            bd=0,
            relief="flat"
        )
        login_button.pack(
            fill="x",
            padx=38,
            ipady=12
        )

        self.username_entry.focus_set()

    # =====================================================
    # SHOW / HIDE PASSWORD
    # =====================================================
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")

    # =====================================================
    # DATABASE LOGIN
    # =====================================================
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if username == "":
            messagebox.showwarning(
                "Required",
                "Username enter करो।"
            )
            self.username_entry.focus_set()
            return

        if password == "":
            messagebox.showwarning(
                "Required",
                "Password enter करो।"
            )
            self.password_entry.focus_set()
            return

        connection = None
        cursor = None

        try:
            connection = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                port=PORT
            )

            cursor = connection.cursor()

            query = """
            SELECT id, username
            FROM users
            WHERE username = %s
            AND password = %s
            """

            cursor.execute(
                query,
                (username, password)
            )

            user = cursor.fetchone()

            if user:
             self.open_dashboard(user[1])

            else:
                messagebox.showerror(
                    "Login Failed",
                    "Username या password गलत है।"
                )

                self.password_var.set("")
                self.password_entry.focus_set()

        except Error as error:
            messagebox.showerror(
                "Database Error",
                f"Database connection failed:\n{error}"
            )

        finally:
            if cursor is not None:
                cursor.close()

            if (
                connection is not None
                and connection.is_connected()
            ):
                connection.close()

    # =====================================================
    # OPEN DASHBOARD
    # =====================================================
    def open_dashboard(self, username):
        try:
            from dashboard import RailwayDashboard

            self.root.withdraw()

            dashboard_window = tk.Toplevel(self.root)

            RailwayDashboard(
                dashboard_window,
                username
            )

            dashboard_window.protocol(
                "WM_DELETE_WINDOW",
                lambda: self.close_dashboard(dashboard_window)
            )

        except ImportError as error:
            messagebox.showerror(
                "Dashboard Error",
                f"dashboard.py import नहीं हुआ:\n{error}"
            )
            self.root.deiconify()

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                f"Dashboard open नहीं हुआ:\n{error}"
            )
            self.root.deiconify()

    def close_dashboard(self, dashboard_window):
        dashboard_window.destroy()
        self.root.deiconify()

        self.username_var.set("")
        self.password_var.set("")
        self.username_entry.focus_set()


def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()