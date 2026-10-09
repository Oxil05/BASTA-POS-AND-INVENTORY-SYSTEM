"""
BASTA BURGER - POS and Inventory Management System
Account Settings and User Management Module
Faithfully recreates Designs/ADMIN_ACCOUNT SETTINGS.png using CustomTkinter and Pillow.
All variables and functions strictly use snake_case.
"""

import os
import sys
from tkinter import messagebox
from PIL import Image
import customtkinter

# Robust path handling so both root execution and ProjectMain execution work
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
for path in [script_dir, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Brand Logo Helper
logo_path = os.path.join(project_root, "Designs", "basta_LOGO.png")
try:
    raw_logo_pil = Image.open(logo_path)
except Exception:
    raw_logo_pil = None


def get_logo_image(size=(52, 52)):
    """Return CTkImage for brand logo or None."""
    if raw_logo_pil:
        return customtkinter.CTkImage(light_image=raw_logo_pil, dark_image=raw_logo_pil, size=size)
    return None


class AccountSettingsView(customtkinter.CTkFrame):
    """
    Account Settings and Staff Management frame matching Designs/ADMIN_ACCOUNT SETTINGS.png.
    Can be embedded directly into BastaPOSApp or displayed in any window.
    """

    def __init__(self, master, app_controller=None, current_role="Administrator", **kwargs):
        super().__init__(master, fg_color="#f1f5f9", **kwargs)
        self.app_controller = app_controller
        self.current_role = getattr(app_controller, "current_role", current_role)

        # Account dataset: load from database or fallback (Admin and Cashier only)
        default_accounts = [
            {"id": 1, "name": "Chef Marco Santos", "email": "marco.s@bastaburger.ph", "user": "marco_admin", "role": "Administrator", "status": "Active", "last_login": "Today, 08:30 AM"},
            {"id": 2, "name": "Bea Mendoza", "email": "bea.m@bastaburger.ph", "user": "bea_cashier", "role": "Cashier", "status": "Active", "last_login": "Today, 09:12 AM"}
        ]

        self.accounts = default_accounts

        try:
            from database import fetch_all_users
            db_users = fetch_all_users()
            if db_users:
                self.accounts = [
                    {
                        "id": u["id"],
                        "name": u["full_name"],
                        "email": u["email"] or f"{u['username']}@bastaburger.ph",
                        "user": u["username"],
                        "role": u["role"],
                        "status": u["status"],
                        "last_login": str(u.get("last_login") or "Never")
                    }
                    for u in db_users
                ]
        except Exception:
            pass

        self.selected_account = None

        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_main_content()

    def is_admin(self):
        """Check if active user has administrator privileges."""
        role = getattr(self.app_controller, "current_role", getattr(self, "current_role", "Administrator"))
        return str(role).strip().lower() in ["admin", "administrator"]

    def _build_main_content(self):
        main_scroll = customtkinter.CTkScrollableFrame(
            self,
            fg_color="#f8fafc",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        main_scroll.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        main_scroll.grid_columnconfigure(0, weight=1)

        # 1. Header Bar
        top_bar = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 16))
        top_bar.grid_columnconfigure(0, weight=1)

        header_info = customtkinter.CTkFrame(top_bar, fg_color="transparent")
        header_info.grid(row=0, column=0, sticky="w")
        customtkinter.CTkLabel(
            header_info, text="Account Settings & Staff Management", font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#09090b"
        ).pack(anchor="w")
        customtkinter.CTkLabel(
            header_info, text="Manage administrative credentials, employee roles, access permissions, and audit logs",
            font=customtkinter.CTkFont(size=12), text_color="#64748b"
        ).pack(anchor="w")

        add_btn_text = "+ Add New Account" if self.is_admin() else "🔒 Add Account (Admin Only)"
        add_btn_fg = "#10b981" if self.is_admin() else "#94a3b8"
        add_btn_hover = "#059669" if self.is_admin() else "#94a3b8"
        add_user_btn = customtkinter.CTkButton(
            top_bar,
            text=add_btn_text,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color=add_btn_fg,
            hover_color=add_btn_hover,
            height=38,
            corner_radius=10,
            command=self.open_create_account_modal
        )
        add_user_btn.grid(row=0, column=1, sticky="e")

        # 2. Key Metrics Row (4 Dark Cards)
        metrics_frame = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        metrics_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        for col_idx in range(4):
            metrics_frame.grid_columnconfigure(col_idx, weight=1)

        total_users = len(self.accounts)
        admin_count = sum(1 for a in self.accounts if a.get("role") == "Administrator")
        cashier_count = sum(1 for a in self.accounts if a.get("role") == "Cashier")
        metrics = [
            ("TOTAL ACCOUNTS", f"{total_users} users", "System registered", "👥"),
            ("CASHIERS", f"{cashier_count} active", "POS Register only", "🟢"),
            ("ADMINISTRATORS", f"{admin_count} admins", "Full system privileges", "🛡"),
            ("ACCOUNT STATUS", "Healthy", "All accounts active", "🔒")
        ]

        for idx, (m_title, m_val, m_sub, m_badge) in enumerate(metrics):
            card = customtkinter.CTkFrame(metrics_frame, fg_color="#09090b", corner_radius=14)
            card.grid(row=0, column=idx, padx=6, pady=4, sticky="nsew")

            c_head = customtkinter.CTkFrame(card, fg_color="transparent")
            c_head.pack(fill="x", padx=16, pady=(14, 4))
            customtkinter.CTkLabel(c_head, text=m_title, font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#94a3b8").pack(side="left")
            customtkinter.CTkLabel(c_head, text=m_badge, font=customtkinter.CTkFont(size=13)).pack(side="right")

            customtkinter.CTkLabel(card, text=m_val, font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#f8fafc").pack(anchor="w", padx=16, pady=2)
            customtkinter.CTkLabel(card, text=m_sub, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#4ade80").pack(anchor="w", padx=16, pady=(0, 14))

        # 3. Staff Accounts Table Card
        table_card = customtkinter.CTkFrame(main_scroll, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        table_card.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 24))
        table_card.grid_columnconfigure(0, weight=1)

        # Filter Sub-bar
        filter_bar = customtkinter.CTkFrame(table_card, fg_color="transparent")
        filter_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        filter_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = customtkinter.CTkEntry(
            filter_bar, placeholder_text="🔍 Search accounts by name, username or role...",
            height=36, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1"
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.role_filter = customtkinter.CTkComboBox(
            filter_bar, values=["All Roles", "Administrator", "Cashier"],
            height=36, corner_radius=10, command=self.on_filter_role, width=180
        )
        self.role_filter.grid(row=0, column=1, sticky="e")

        # Table rows container
        self.table_container = customtkinter.CTkFrame(table_card, fg_color="transparent")
        self.table_container.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        self.table_container.grid_columnconfigure(0, weight=2)
        for c in range(1, 6):
            self.table_container.grid_columnconfigure(c, weight=1)

        self.render_accounts_table()

    def render_accounts_table(self, query="", role_filter="All Roles"):
        for w in self.table_container.winfo_children():
            w.destroy()

        headers = ["USER", "USERNAME", "ROLE", "STATUS", "LAST LOGIN", "ACTIONS"]
        for c_idx, h in enumerate(headers):
            customtkinter.CTkLabel(
                self.table_container, text=h, font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#64748b"
            ).grid(row=0, column=c_idx, sticky="w", padx=6, pady=8)

        filtered = []
        for acc in self.accounts:
            match_q = query.lower() in acc["name"].lower() or query.lower() in acc["user"].lower() or query.lower() in acc["email"].lower()
            match_r = (role_filter == "All Roles") or (acc["role"] == role_filter)
            if match_q and match_r:
                filtered.append(acc)

        for r_idx, acc in enumerate(filtered, start=1):
            row_bg = "#f8fafc" if r_idx % 2 == 0 else "#ffffff"
            r_frame = customtkinter.CTkFrame(self.table_container, fg_color=row_bg, corner_radius=6)
            r_frame.grid(row=r_idx, column=0, columnspan=6, sticky="ew", pady=2)
            r_frame.grid_columnconfigure(0, weight=2)
            for c in range(1, 6):
                r_frame.grid_columnconfigure(c, weight=1)

            # Name & Email
            user_box = customtkinter.CTkFrame(r_frame, fg_color="transparent")
            user_box.grid(row=0, column=0, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(user_box, text=acc["name"], font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#0f172a").pack(anchor="w")
            customtkinter.CTkLabel(user_box, text=acc["email"], font=customtkinter.CTkFont(size=10), text_color="#94a3b8").pack(anchor="w")

            # Username
            customtkinter.CTkLabel(r_frame, text=f"@{acc['user']}", font=customtkinter.CTkFont(size=11), text_color="#475569").grid(row=0, column=1, sticky="w", padx=6, pady=8)

            # Role pill
            role = acc["role"]
            if role == "Administrator":
                r_bg, r_fg = "#ede9fe", "#6d28d9"
            elif role == "Shift Supervisor":
                r_bg, r_fg = "#e0e7ff", "#4338ca"
            elif role == "Cashier":
                r_bg, r_fg = "#dcfce7", "#15803d"
            else:
                r_bg, r_fg = "#fef3c7", "#b45309"

            role_pill = customtkinter.CTkFrame(r_frame, fg_color=r_bg, corner_radius=6)
            role_pill.grid(row=0, column=2, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(role_pill, text=role, font=customtkinter.CTkFont(size=10, weight="bold"), text_color=r_fg).pack(padx=8, pady=2)

            # Status pill
            status_pill = customtkinter.CTkFrame(r_frame, fg_color="#dcfce7", corner_radius=6)
            status_pill.grid(row=0, column=3, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(status_pill, text="● Active", font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#15803d").pack(padx=8, pady=2)

            # Last login
            customtkinter.CTkLabel(r_frame, text=acc["last_login"], font=customtkinter.CTkFont(size=11), text_color="#64748b").grid(row=0, column=4, sticky="w", padx=6, pady=8)

            # Action buttons
            actions_frame = customtkinter.CTkFrame(r_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=5, sticky="w", padx=6, pady=8)

            edit_btn = customtkinter.CTkButton(
                actions_frame, text="✏ Edit", font=customtkinter.CTkFont(size=10, weight="bold"),
                fg_color="#f1f5f9", text_color="#0f172a", hover_color="#e2e8f0", width=55, height=26, corner_radius=6,
                command=lambda a=acc: self.open_edit_account_modal(a)
            )
            edit_btn.pack(side="left", padx=2)

            del_btn = customtkinter.CTkButton(
                actions_frame, text="🗑", font=customtkinter.CTkFont(size=10),
                fg_color="#fee2e2", text_color="#ef4444", hover_color="#fca5a5", width=30, height=26, corner_radius=6,
                command=lambda a=acc: self.delete_account(a)
            )
            del_btn.pack(side="left", padx=2)

    def on_search(self, event=None):
        self.render_accounts_table(query=self.search_entry.get().strip(), role_filter=self.role_filter.get())

    def on_filter_role(self, role):
        self.render_accounts_table(query=self.search_entry.get().strip(), role_filter=role)

    def open_create_account_modal(self):
        if not self.is_admin():
            messagebox.showwarning("Permission Denied", "Access Denied: Only Administrators are authorized to create user accounts.")
            return

        modal = customtkinter.CTkToplevel(self)
        modal.title("Add New Account")
        modal.geometry("460x520")
        modal.grab_set()

        customtkinter.CTkLabel(modal, text="👤 Create Employee / Admin Account", font=customtkinter.CTkFont(size=16, weight="bold")).pack(pady=(20, 14))

        fields = [
            ("Full Name:", "e.g. Maria Santos"),
            ("Username:", "e.g. maria_cashier"),
            ("Email Address:", "e.g. maria.s@bastaburger.ph"),
            ("Temporary Password:", "Enter password...")
        ]
        entries = {}
        for lbl_txt, p_holder in fields:
            customtkinter.CTkLabel(modal, text=lbl_txt, font=customtkinter.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=30, pady=(4, 0))
            e = customtkinter.CTkEntry(modal, placeholder_text=p_holder, width=400, height=36)
            e.pack(padx=30, pady=(2, 6))
            entries[lbl_txt] = e

        customtkinter.CTkLabel(modal, text="Assigned Role:", font=customtkinter.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=30, pady=(4, 0))
        role_cb = customtkinter.CTkComboBox(modal, values=["Cashier", "Administrator"], width=400, height=36)
        role_cb.pack(padx=30, pady=(2, 16))

        def confirm_create():
            f_name = entries["Full Name:"].get().strip()
            u_name = entries["Username:"].get().strip()
            email = entries["Email Address:"].get().strip()
            pwd = entries["Temporary Password:"].get().strip() or "staff123"
            sel_role = role_cb.get()

            if f_name and u_name:
                new_id = len(self.accounts) + 1
                try:
                    from database import add_user
                    db_id = add_user(u_name, pwd, f_name, email or f"{u_name}@bastaburger.ph", sel_role, "Active")
                    if db_id:
                        new_id = db_id
                except Exception as e:
                    print(f"[BASTA DB] User add notice: {e}")

                self.accounts.append({
                    "id": new_id,
                    "name": f_name,
                    "email": email or f"{u_name}@bastaburger.ph",
                    "user": u_name,
                    "role": sel_role,
                    "status": "Active",
                    "last_login": "Never"
                })
                self.render_accounts_table()
            modal.destroy()

        customtkinter.CTkButton(
            modal, text="✓ Save & Grant Access", fg_color="#10b981", hover_color="#059669", height=40, width=400, command=confirm_create
        ).pack(padx=30, pady=10)

    def open_edit_account_modal(self, acc):
        if not self.is_admin():
            messagebox.showwarning("Permission Denied", "Access Denied: Only Administrators are authorized to edit user accounts.")
            return

        modal = customtkinter.CTkToplevel(self)
        modal.title(f"Edit Account: {acc['name']}")
        modal.geometry("460x420")
        modal.grab_set()

        customtkinter.CTkLabel(modal, text=f"Edit: {acc['name']}", font=customtkinter.CTkFont(size=16, weight="bold")).pack(pady=(20, 14))

        customtkinter.CTkLabel(modal, text="Full Name:", font=customtkinter.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=30)
        name_e = customtkinter.CTkEntry(modal, width=400, height=36)
        name_e.insert(0, acc["name"])
        name_e.pack(padx=30, pady=(2, 8))

        customtkinter.CTkLabel(modal, text="Email Address:", font=customtkinter.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=30)
        email_e = customtkinter.CTkEntry(modal, width=400, height=36)
        email_e.insert(0, acc["email"])
        email_e.pack(padx=30, pady=(2, 8))

        customtkinter.CTkLabel(modal, text="Assigned Role:", font=customtkinter.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=30)
        role_cb = customtkinter.CTkComboBox(modal, values=["Cashier", "Administrator"], width=400, height=36)
        role_cb.set(acc["role"])
        role_cb.pack(padx=30, pady=(2, 18))

        def confirm_save():
            new_name = name_e.get().strip()
            new_email = email_e.get().strip()
            new_role = role_cb.get()

            try:
                from database import update_user
                update_user(acc["id"], new_name, new_email, new_role, acc.get("status", "Active"))
            except Exception as e:
                print(f"[BASTA DB] User update notice: {e}")

            acc["name"] = new_name
            acc["email"] = new_email
            acc["role"] = new_role
            modal.destroy()
            self.render_accounts_table()

        customtkinter.CTkButton(
            modal, text="✓ Save Changes", fg_color="#10b981", hover_color="#059669", height=40, width=400, command=confirm_save
        ).pack(padx=30, pady=10)

    def delete_account(self, acc):
        if not self.is_admin():
            messagebox.showwarning("Permission Denied", "Access Denied: Only Administrators are authorized to delete user accounts.")
            return
        if acc in self.accounts:
            try:
                from database import delete_user
                delete_user(acc["id"])
            except Exception as e:
                print(f"[BASTA DB] User delete notice: {e}")

            self.accounts.remove(acc)
            self.render_accounts_table()


class AccountSettingsApp:
    """Wrapper that launches the unified application on the Settings tab."""

    def __new__(cls, *args, **kwargs):
        try:
            from ProjectMain.POS import BastaPOSApp
        except ImportError:
            from POS import BastaPOSApp
        return BastaPOSApp(initial_view="settings")


if __name__ == "__main__":
    app = AccountSettingsApp()
    app.mainloop()
