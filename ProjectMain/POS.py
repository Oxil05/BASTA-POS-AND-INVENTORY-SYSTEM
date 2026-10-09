import os
import sys
from datetime import datetime
from PIL import Image
import customtkinter

# Robust path handling so both root execution and ProjectMain execution work
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
for path in [script_dir, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Configure global CustomTkinter appearance
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Base directory paths for assets
logo_path = os.path.join(project_root, "Designs", "basta_LOGO.png")

# Safely load the brand logo with fallback
try:
    raw_logo_pil = Image.open(logo_path)
except Exception:
    raw_logo_pil = None


def get_logo_image(size=(60, 60)):
    """Return a CTkImage for basta_LOGO.png or None if unavailable."""
    if raw_logo_pil:
        return customtkinter.CTkImage(light_image=raw_logo_pil, dark_image=raw_logo_pil, size=size)
    return None


# Import unified views
try:
    from product_management import ProductManagementView
    from inventory_overview import InventoryOverviewView
    from reports import ReportsView
    from account_settings import AccountSettingsView
except ImportError:
    from ProjectMain.product_management import ProductManagementView
    from ProjectMain.inventory_overview import InventoryOverviewView
    from ProjectMain.reports import ReportsView
    from ProjectMain.account_settings import AccountSettingsView



class PaymentCompleteWindow(customtkinter.CTkToplevel):
    """Secondary window representing the Payment Complete screen & Digital Tablet Receipt."""

    def __init__(self, parent_window, order_data=None):
        super().__init__(parent_window)

        self.parent_window = parent_window
        self.order_data = order_data or {
            "items": [
                {"name": "Basta Smash Burger", "qty": 2, "price": 285.0},
                {"name": "Truffle Parm Fries", "qty": 1, "price": 145.0},
                {"name": "Ube Milkshake", "qty": 1, "price": 165.0}
            ],
            "subtotal": 880.0,
            "vat": 94.29,
            "service_charge": 88.0,
            "total": 968.0,
            "payment_method": "Cash"
        }

        self.title("BASTA POS - Payment Complete")
        self.geometry("1180x760")
        self.minsize(980, 650)

        # Configure root grid weights for responsiveness (2 columns: left confirmation, right tablet receipt)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)  # Left confirmation panel
        self.grid_columnconfigure(1, weight=2)  # Right tablet receipt panel

        self._build_confirmation_panel()
        self._build_tablet_receipt_panel()

    def _build_confirmation_panel(self):
        center_scroll = customtkinter.CTkScrollableFrame(
            self,
            fg_color="#f8fafc",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        center_scroll.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        center_scroll.grid_columnconfigure(0, weight=1)

        # Header Titles with generous rounded spacing
        main_title = customtkinter.CTkLabel(
            center_scroll,
            text="Payment complete",
            font=customtkinter.CTkFont(size=30, weight="bold"),
            text_color="#09090b"
        )
        main_title.grid(row=0, column=0, sticky="w", pady=(12, 2), padx=6)

        sub_title = customtkinter.CTkLabel(
            center_scroll,
            text="Order #B-1048 · Table 12 · 9:48 AM",
            font=customtkinter.CTkFont(size=13),
            text_color="#64748b"
        )
        sub_title.grid(row=1, column=0, sticky="w", pady=(0, 20), padx=6)

        # Big Success Checkmark Icon Badge
        checkmark_badge = customtkinter.CTkButton(
            center_scroll,
            text="✓",
            font=customtkinter.CTkFont(size=32, weight="bold"),
            width=72,
            height=72,
            corner_radius=36,
            fg_color="#10b981",
            text_color="#ffffff",
            hover=False
        )
        checkmark_badge.grid(row=2, column=0, sticky="w", pady=(0, 12), padx=6)

        # Status text
        success_label = customtkinter.CTkLabel(
            center_scroll,
            text="PAYMENT SUCCESSFUL",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text_color="#10b981"
        )
        success_label.grid(row=3, column=0, sticky="w", padx=6)

        # Dynamic Paid Amount
        total_amount = self.order_data.get("total", 968.0)
        amount_label = customtkinter.CTkLabel(
            center_scroll,
            text=f"₱{total_amount:,.2f}",
            font=customtkinter.CTkFont(size=44, weight="bold"),
            text_color="#09090b"
        )
        amount_label.grid(row=4, column=0, sticky="w", pady=(4, 10), padx=6)

        # Description
        desc_label = customtkinter.CTkLabel(
            center_scroll,
            text="Payment received. The kitchen ticket has been sent and Table 12 is marked as paid.",
            font=customtkinter.CTkFont(size=13),
            text_color="#475569",
            wraplength=480,
            justify="left"
        )
        desc_label.grid(row=5, column=0, sticky="w", pady=(0, 20), padx=6)

        # Transaction details card
        card_frame = customtkinter.CTkFrame(
            center_scroll,
            fg_color="#ffffff",
            corner_radius=16,
            border_width=1,
            border_color="#e2e8f0"
        )
        card_frame.grid(row=6, column=0, sticky="ew", pady=(0, 20), padx=4)
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=1)

        pay_method = self.order_data.get("payment_method", "Cash")
        cash_received = self.order_data.get("cash_received", (1000.0 if pay_method == "Cash" else total_amount))
        change_due = self.order_data.get("change_due", max(0.0, cash_received - total_amount))

        detail_items = [
            ("Payment method", pay_method),
            ("Cash received", f"₱{cash_received:,.2f}"),
            ("Change due", f"₱{change_due:,.2f}"),
            ("Transaction ID", "TXN-0928-001048")
        ]

        for idx, (label_txt, value_txt) in enumerate(detail_items):
            lbl = customtkinter.CTkLabel(
                card_frame,
                text=label_txt,
                font=customtkinter.CTkFont(size=13),
                text_color="#64748b"
            )
            lbl.grid(row=idx, column=0, padx=18, pady=9, sticky="w")

            val = customtkinter.CTkLabel(
                card_frame,
                text=value_txt,
                font=customtkinter.CTkFont(size=13, weight="bold"),
                text_color="#09090b"
            )
            val.grid(row=idx, column=1, padx=18, pady=9, sticky="e")

        # Action Buttons row 1 (Responsive)
        actions_row_1 = customtkinter.CTkFrame(center_scroll, fg_color="transparent")
        actions_row_1.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        actions_row_1.grid_columnconfigure(0, weight=1)
        actions_row_1.grid_columnconfigure(1, weight=1)

        new_order_btn = customtkinter.CTkButton(
            actions_row_1,
            text="+ New order",
            height=46,
            corner_radius=12,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            text_color="#ffffff",
            hover_color="#059669",
            command=self.start_new_order
        )
        new_order_btn.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        print_receipt_btn = customtkinter.CTkButton(
            actions_row_1,
            text="⎙ Print receipt",
            height=46,
            corner_radius=12,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#18181b",
            text_color="#ffffff",
            hover_color="#27272a"
        )
        print_receipt_btn.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        # Action Buttons row 2 (Sub-actions)
        actions_row_2 = customtkinter.CTkFrame(center_scroll, fg_color="transparent")
        actions_row_2.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        actions_row_2.grid_columnconfigure(0, weight=1)
        actions_row_2.grid_columnconfigure(1, weight=1)
        actions_row_2.grid_columnconfigure(2, weight=1)

        email_btn = customtkinter.CTkButton(
            actions_row_2,
            text="✉ Email receipt",
            height=38,
            corner_radius=10,
            font=customtkinter.CTkFont(size=12),
            fg_color="#ffffff",
            text_color="#334155",
            border_width=1,
            border_color="#cbd5e1",
            hover_color="#f1f5f9"
        )
        email_btn.grid(row=0, column=0, padx=4, sticky="ew")

        sms_btn = customtkinter.CTkButton(
            actions_row_2,
            text="💬 Send via SMS",
            height=38,
            corner_radius=10,
            font=customtkinter.CTkFont(size=12),
            fg_color="#ffffff",
            text_color="#334155",
            border_width=1,
            border_color="#cbd5e1",
            hover_color="#f1f5f9"
        )
        sms_btn.grid(row=0, column=1, padx=4, sticky="ew")

        reopen_btn = customtkinter.CTkButton(
            actions_row_2,
            text="Reopen order",
            height=38,
            corner_radius=10,
            font=customtkinter.CTkFont(size=12),
            fg_color="transparent",
            text_color="#64748b",
            hover_color="#e2e8f0",
            command=self.destroy
        )
        reopen_btn.grid(row=0, column=2, padx=4, sticky="ew")

    def _build_tablet_receipt_panel(self):
        tablet_container = customtkinter.CTkFrame(
            self,
            fg_color="#f1f5f9",
            corner_radius=0
        )
        tablet_container.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        tablet_container.grid_rowconfigure(0, weight=1)
        tablet_container.grid_columnconfigure(0, weight=1)

        # Black outer tablet frame
        tablet_bezel = customtkinter.CTkFrame(
            tablet_container,
            fg_color="#18181b",
            corner_radius=28
        )
        tablet_bezel.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        tablet_bezel.grid_rowconfigure(0, weight=1)
        tablet_bezel.grid_columnconfigure(0, weight=1)

        # White inner receipt paper
        receipt_paper = customtkinter.CTkScrollableFrame(
            tablet_bezel,
            fg_color="#ffffff",
            corner_radius=18
        )
        receipt_paper.grid(row=0, column=0, padx=14, pady=14, sticky="nsew")
        receipt_paper.grid_columnconfigure(0, weight=1)
        receipt_paper.grid_columnconfigure(1, weight=1)

        # Store Header with basta_LOGO.png
        current_row = 0
        receipt_logo_img = get_logo_image(size=(46, 46))
        if receipt_logo_img:
            receipt_logo_label = customtkinter.CTkLabel(
                receipt_paper,
                image=receipt_logo_img,
                text=""
            )
            receipt_logo_label.grid(row=current_row, column=0, columnspan=2, pady=(14, 2))
            current_row += 1

        store_title = customtkinter.CTkLabel(
            receipt_paper,
            text="BASTA POS",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="#09090b"
        )
        store_title.grid(row=current_row, column=0, columnspan=2, pady=(0, 2))
        current_row += 1

        store_addr = customtkinter.CTkLabel(
            receipt_paper,
            text="#11 Purok 2, Ibayo Marilao Bulacan\nVAT Reg. TIN 009-482-176-000",
            font=customtkinter.CTkFont(size=11),
            text_color="#64748b"
        )
        store_addr.grid(row=current_row, column=0, columnspan=2, pady=(0, 10))
        current_row += 1

        # Receipt Meta
        meta_items = [
            ("Receipt", "OR-2026-01048"),
            ("Order", "#B-1048 · Table 12"),
            ("Cashier", "Bea M."),
            ("Date", "28 Sep 2026 - 9:48 AM")
        ]
        for lbl_txt, val_txt in meta_items:
            m_lbl = customtkinter.CTkLabel(
                receipt_paper,
                text=lbl_txt,
                font=customtkinter.CTkFont(size=11),
                text_color="#64748b"
            )
            m_lbl.grid(row=current_row, column=0, sticky="w", padx=14, pady=2)

            m_val = customtkinter.CTkLabel(
                receipt_paper,
                text=val_txt,
                font=customtkinter.CTkFont(size=11, weight="bold"),
                text_color="#09090b"
            )
            m_val.grid(row=current_row, column=1, sticky="e", padx=14, pady=2)
            current_row += 1

        # Divider
        divider_1 = customtkinter.CTkLabel(
            receipt_paper,
            text="--------------------------------------------------",
            text_color="#cbd5e1"
        )
        divider_1.grid(row=current_row, column=0, columnspan=2, pady=5)
        current_row += 1

        # Dynamic Item list from order data
        items = self.order_data.get("items", [])
        for item in items:
            item_name = item.get("name", "Item")
            qty = item.get("qty", 1)
            price = item.get("price", 0.0)
            item_line_total = price * qty if price < 1000 else price

            i_lbl = customtkinter.CTkLabel(
                receipt_paper,
                text=f"{qty}×  {item_name}",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#0f172a"
            )
            i_lbl.grid(row=current_row, column=0, sticky="w", padx=14, pady=3)

            i_val = customtkinter.CTkLabel(
                receipt_paper,
                text=f"₱{item_line_total:,.2f}",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#0f172a"
            )
            i_val.grid(row=current_row, column=1, sticky="e", padx=14, pady=3)
            current_row += 1

        # Divider
        divider_2 = customtkinter.CTkLabel(
            receipt_paper,
            text="--------------------------------------------------",
            text_color="#cbd5e1"
        )
        divider_2.grid(row=current_row, column=0, columnspan=2, pady=5)
        current_row += 1

        # Financial Breakdown
        subtotal = self.order_data.get("subtotal", 880.0)
        vat_sales = subtotal / 1.12
        vat_val = self.order_data.get("vat", 94.29)
        svc_val = self.order_data.get("service_charge", 88.0)
        total_val = self.order_data.get("total", 968.0)

        breakdown_items = [
            ("Subtotal", f"₱{subtotal:,.2f}"),
            ("VATable sales", f"₱{vat_sales:,.2f}"),
            ("VAT (12%)", f"₱{vat_val:,.2f}"),
            ("Service charge", f"₱{svc_val:,.2f}")
        ]
        for b_lbl, b_val in breakdown_items:
            f_lbl = customtkinter.CTkLabel(
                receipt_paper,
                text=b_lbl,
                font=customtkinter.CTkFont(size=11),
                text_color="#64748b"
            )
            f_lbl.grid(row=current_row, column=0, sticky="w", padx=14, pady=2)

            f_val = customtkinter.CTkLabel(
                receipt_paper,
                text=b_val,
                font=customtkinter.CTkFont(size=11),
                text_color="#09090b"
            )
            f_val.grid(row=current_row, column=1, sticky="e", padx=14, pady=2)
            current_row += 1

        # Total
        tot_lbl = customtkinter.CTkLabel(
            receipt_paper,
            text="TOTAL",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color="#09090b"
        )
        tot_lbl.grid(row=current_row, column=0, sticky="w", padx=14, pady=(8, 4))

        tot_val = customtkinter.CTkLabel(
            receipt_paper,
            text=f"₱{total_val:,.2f}",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            text_color="#09090b"
        )
        tot_val.grid(row=current_row, column=1, sticky="e", padx=14, pady=(8, 4))
        current_row += 1

        # Payment Badge
        badge_frame = customtkinter.CTkFrame(
            receipt_paper,
            fg_color="#ecfdf5",
            corner_radius=10
        )
        badge_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", padx=14, pady=10)
        badge_frame.grid_columnconfigure(0, weight=1)
        badge_frame.grid_columnconfigure(1, weight=1)

        pay_method = self.order_data.get("payment_method", "Cash")
        cash_received = self.order_data.get("cash_received", (1000.0 if pay_method == "Cash" else total_val))
        change_due = self.order_data.get("change_due", max(0.0, cash_received - total_val))

        b_cash = customtkinter.CTkLabel(
            badge_frame,
            text=f"💵 {pay_method}",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color="#047857"
        )
        b_cash.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        b_change = customtkinter.CTkLabel(
            badge_frame,
            text=f"Change ₱{change_due:,.2f}",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color="#047857"
        )
        b_change.grid(row=0, column=1, padx=10, pady=8, sticky="e")
        current_row += 1

        # Thank you note
        thanks_label = customtkinter.CTkLabel(
            receipt_paper,
            text="Salamat! See you again.",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text_color="#09090b"
        )
        thanks_label.grid(row=current_row, column=0, columnspan=2, pady=(10, 18))

    def start_new_order(self):
        """Reset the cart in POS and close this window."""
        if hasattr(self.parent_window, "reset_cart"):
            self.parent_window.reset_cart()
        self.destroy()

    def open_products_screen(self):
        self.destroy()
        if hasattr(self.parent_window, "switch_view"):
            self.parent_window.switch_view("products")

    def open_inventory_screen(self):
        self.destroy()
        if hasattr(self.parent_window, "switch_view"):
            self.parent_window.switch_view("inventory")

    def open_reports_screen(self):
        self.destroy()
        if hasattr(self.parent_window, "switch_view"):
            self.parent_window.switch_view("reports")

    def open_accounts_screen(self):
        self.destroy()
        if hasattr(self.parent_window, "switch_view"):
            self.parent_window.switch_view("settings")


class BastaPOSApp(customtkinter.CTk):
    """Main POS Application window recreation with full interactivity and responsiveness."""

    def __init__(self, initial_view="pos", current_user="Chef Marco S.", current_role="Administrator"):
        super().__init__()

        self.initial_view = initial_view
        self.current_user = current_user
        self.current_role = current_role
        self.is_admin = (str(self.current_role).strip().lower() in ["admin", "administrator"])
        self.order_counter = 1048
        self.title("BASTA POS")
        self.geometry("1440x880")
        self.minsize(1080, 680)

        # Set background
        self.configure(fg_color="#f1f5f9")

        # Preload reusable CTkImages for fast rendering
        self.sidebar_logo_img = get_logo_image(size=(52, 52))
        self.product_placeholder_img = get_logo_image(size=(105, 75))
        self.cached_product_images = {}

        # Products catalog data (dynamically populated from ProductManagementView)
        self.catalog_products = []

        # Active cart state dictionary
        self.cart_items = {}

        # Filter state
        self.active_category = "🔥 All Items"
        self.search_query = ""
        self.active_payment_method = "Cash"
        self.category_buttons = {}
        self.payment_buttons = {}
        self.current_grid_columns = 4

        # Configure root layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Left sidebar (width 110)
        self.grid_columnconfigure(1, weight=1)  # Unified content container

        self._build_sidebar()

        # Build Unified Content Container
        self.content_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # 1. POS Register View Frame
        self.pos_view = customtkinter.CTkFrame(self.content_container, fg_color="transparent")
        self.pos_view.grid_rowconfigure(0, weight=1)
        self.pos_view.grid_columnconfigure(0, weight=4)  # Main order catalog
        self.pos_view.grid_columnconfigure(1, weight=2)  # Right checkout panel

        # 2. Reusable Modular Views embedded inside one system (instantiated before catalog to allow sync)
        self.products_view = ProductManagementView(self.content_container, app_controller=self)
        self.inventory_view = InventoryOverviewView(self.content_container, app_controller=self)
        self.reports_view = ReportsView(self.content_container, app_controller=self)
        self.accounts_view = AccountSettingsView(self.content_container, app_controller=self)

        self._build_main_catalog()
        self._build_checkout_panel()

        # Initial calculation & rendering
        self.recalculate_totals()
        self.refresh_cart_display()

        # Switch to requested initial view
        self.switch_view(self.initial_view)

        # Bind configure for responsive grid scaling
        self.bind("<Configure>", self.on_window_resize)

    def _build_sidebar(self):
        sidebar_frame = customtkinter.CTkFrame(
            self,
            width=110,
            corner_radius=0,
            fg_color="#09090b"
        )
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_propagate(False)
        sidebar_frame.grid_rowconfigure(7, weight=1)

        # Brand / Logo Header using basta_LOGO.png
        if self.sidebar_logo_img:
            logo_label = customtkinter.CTkLabel(
                sidebar_frame,
                image=self.sidebar_logo_img,
                text=""
            )
            logo_label.grid(row=0, column=0, padx=10, pady=(20, 2))

            brand_label = customtkinter.CTkLabel(
                sidebar_frame,
                text="BASTA POS",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#f8fafc"
            )
            brand_label.grid(row=1, column=0, padx=10, pady=(0, 20))
        else:
            brand_label = customtkinter.CTkLabel(
                sidebar_frame,
                text="🍔\nBASTA\nPOS",
                font=customtkinter.CTkFont(size=14, weight="bold"),
                text_color="#f8fafc"
            )
            brand_label.grid(row=0, column=0, padx=10, pady=(25, 30))

        # Navigation Buttons (All connected seamlessly inside one window)
        self.pos_nav_btn = customtkinter.CTkButton(
            sidebar_frame,
            text="⊞\nPOS",
            width=70,
            height=60,
            corner_radius=14,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="#10b981",
            text_color="#ffffff",
            hover_color="#059669",
            command=lambda: self.switch_view("pos")
        )
        self.pos_nav_btn.grid(row=2, column=0, padx=15, pady=6)

        self.products_nav_btn = customtkinter.CTkButton(
            sidebar_frame,
            text="📦\nProducts",
            width=70,
            height=50,
            corner_radius=10,
            font=customtkinter.CTkFont(size=11),
            fg_color="transparent",
            text_color="#9ca3af",
            hover_color="#1f2937",
            command=lambda: self.switch_view("products")
        )
        self.stock_nav_btn = customtkinter.CTkButton(
            sidebar_frame,
            text="📋\nStock",
            width=70,
            height=50,
            corner_radius=10,
            font=customtkinter.CTkFont(size=11),
            fg_color="transparent",
            text_color="#9ca3af",
            hover_color="#1f2937",
            command=lambda: self.switch_view("stock")
        )

        self.reports_nav_btn = customtkinter.CTkButton(
            sidebar_frame,
            text="📊\nReports",
            width=70,
            height=50,
            corner_radius=10,
            font=customtkinter.CTkFont(size=11),
            fg_color="transparent",
            text_color="#9ca3af",
            hover_color="#1f2937",
            command=lambda: self.switch_view("reports")
        )

        self.settings_nav_btn = customtkinter.CTkButton(
            sidebar_frame,
            text="⚙\nSettings",
            width=70,
            height=50,
            corner_radius=10,
            font=customtkinter.CTkFont(size=11),
            fg_color="transparent",
            text_color="#9ca3af",
            hover_color="#1f2937",
            command=lambda: self.switch_view("settings")
        )

        if self.is_admin:
            self.products_nav_btn.grid(row=3, column=0, padx=15, pady=6)
            self.stock_nav_btn.grid(row=4, column=0, padx=15, pady=6)
            self.reports_nav_btn.grid(row=5, column=0, padx=15, pady=6)
            self.settings_nav_btn.grid(row=6, column=0, padx=15, pady=6)

        # Logout at bottom
        logout_btn = customtkinter.CTkButton(
            sidebar_frame,
            text="➔\nLogout",
            width=70,
            height=50,
            corner_radius=10,
            font=customtkinter.CTkFont(size=11),
            fg_color="transparent",
            text_color="#9ca3af",
            hover_color="#1f2937",
            command=self.handle_logout
        )
        logout_btn.grid(row=8, column=0, padx=15, pady=(10, 25))

    def switch_view(self, view_name):
        """Switches the active view inside the main window seamlessly."""
        if not self.is_admin and view_name != "pos":
            from tkinter import messagebox
            messagebox.showwarning("Access Restricted", "Access Denied: Cashiers are authorized to access the POS only.")
            return

        self.current_view_name = view_name

        # Hide all views
        self.pos_view.grid_forget()
        self.products_view.grid_forget()
        self.inventory_view.grid_forget()
        self.reports_view.grid_forget()
        self.accounts_view.grid_forget()

        # Reset all navigation buttons styling
        nav_buttons = [
            self.pos_nav_btn,
            self.products_nav_btn,
            self.stock_nav_btn,
            self.reports_nav_btn,
            self.settings_nav_btn
        ]
        for btn in nav_buttons:
            btn.configure(
                height=50,
                corner_radius=10,
                fg_color="transparent",
                text_color="#9ca3af",
                hover_color="#1f2937",
                font=customtkinter.CTkFont(size=11)
            )

        # Display target view and highlight matching button
        if view_name == "pos":
            self.sync_products_from_management()
            self.pos_view.grid(row=0, column=0, sticky="nsew")
            self.pos_nav_btn.configure(
                height=60, corner_radius=14,
                fg_color="#10b981", text_color="#ffffff", hover_color="#059669",
                font=customtkinter.CTkFont(size=12, weight="bold")
            )
            self.title("BASTA POS - Point of Sale")
        elif view_name == "products":
            self.products_view.grid(row=0, column=0, sticky="nsew")
            self.products_nav_btn.configure(
                height=60, corner_radius=14,
                fg_color="#10b981", text_color="#ffffff", hover_color="#059669",
                font=customtkinter.CTkFont(size=12, weight="bold")
            )
            self.title("BASTA POS - Product Management")
        elif view_name == "stock":
            if hasattr(self.inventory_view, "render_inventory_table"):
                self.inventory_view.render_inventory_table()
            self.inventory_view.grid(row=0, column=0, sticky="nsew")
            self.stock_nav_btn.configure(
                height=60, corner_radius=14,
                fg_color="#10b981", text_color="#ffffff", hover_color="#059669",
                font=customtkinter.CTkFont(size=12, weight="bold")
            )
            self.title("BASTA POS - Inventory Overview")
        elif view_name == "reports":
            if hasattr(self.reports_view, "render_metric_cards"):
                self.reports_view.render_metric_cards()
            if hasattr(self.reports_view, "render_transactions_table"):
                self.reports_view.render_transactions_table()
            self.reports_view.grid(row=0, column=0, sticky="nsew")
            self.reports_nav_btn.configure(
                height=60, corner_radius=14,
                fg_color="#10b981", text_color="#ffffff", hover_color="#059669",
                font=customtkinter.CTkFont(size=12, weight="bold")
            )
            self.title("BASTA POS - Sales & Inventory Reports")
        elif view_name == "settings":
            if hasattr(self.accounts_view, "render_accounts_table"):
                self.accounts_view.render_accounts_table()
            self.accounts_view.grid(row=0, column=0, sticky="nsew")
            self.settings_nav_btn.configure(
                height=60, corner_radius=14,
                fg_color="#10b981", text_color="#ffffff", hover_color="#059669",
                font=customtkinter.CTkFont(size=12, weight="bold")
            )
            self.title("BASTA POS - Account Settings")

    def get_cached_product_image(self, image_filename, size=(160, 95)):
        """Retrieve or cache CTkImage for a product photo from Designs folder."""
        if not image_filename:
            return self.product_placeholder_img

        cache_key = (image_filename, size)
        if cache_key in self.cached_product_images:
            return self.cached_product_images[cache_key]

        # Determine path
        img_path = os.path.join(project_root, "Designs", image_filename)
        if not os.path.exists(img_path) and os.path.isabs(image_filename) and os.path.exists(image_filename):
            img_path = image_filename

        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                ctk_img = customtkinter.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
                self.cached_product_images[cache_key] = ctk_img
                return ctk_img
            except Exception as e:
                print(f"[BASTA POS] Warning loading product image {image_filename}: {e}")

        return self.product_placeholder_img

    def sync_products_from_management(self):
        """Dynamically synchronize POS catalog with products from Product Management."""
        category_icons = {
            "Burgers": "🍔",
            "Beverages": "🥤",
            "Drinks": "🥤",
            "Sides": "🍟",
            "Desserts": "🍪",
            "Meals": "🍗",
            "Silog": "🍳",
            "Sandwiches": "🥪",
            "Pasta": "🍝"
        }

        if hasattr(self, "products_view") and hasattr(self.products_view, "products_data"):
            synced_catalog = []
            for prod in self.products_view.products_data:
                # Include products that are active and designated for in-store
                if prod.get("status", "Active") == "Active" and prod.get("in_store", True):
                    cat = prod.get("category", "Burgers")
                    icon = category_icons.get(cat, "🍔")
                    stock_qty = prod.get("stock", 0)
                    synced_catalog.append({
                        "id": prod.get("id"),
                        "sku": prod.get("sku", ""),
                        "name": prod.get("name", "Item"),
                        "category": cat,
                        "sub": f"{cat} · {stock_qty} left",
                        "price": float(prod.get("price", 0.0)),
                        "icon": icon,
                        "stock": stock_qty,
                        "image_filename": prod.get("image_filename", "basta_LOGO.png")
                    })
            if synced_catalog:
                self.catalog_products = synced_catalog

        if hasattr(self, "categories_bar"):
            self.refresh_category_pills()
        if hasattr(self, "products_scroll"):
            self.render_product_cards()

    def refresh_category_pills(self):
        """Dynamically rebuild category pill buttons from current catalog."""
        if not hasattr(self, "categories_bar"):
            return
        for widget in self.categories_bar.winfo_children():
            widget.destroy()
        self.category_buttons.clear()

        unique_cats = sorted(list(set(p["category"] for p in self.catalog_products if p.get("category"))))
        categories = ["🔥 All Items"] + unique_cats

        if self.active_category not in categories:
            self.active_category = "🔥 All Items"

        for cat_name in categories:
            is_active = (cat_name == self.active_category)
            cat_btn = customtkinter.CTkButton(
                self.categories_bar,
                text=cat_name,
                height=36,
                corner_radius=18,
                font=customtkinter.CTkFont(size=13, weight="bold" if is_active else "normal"),
                fg_color="#18181b" if is_active else "#ffffff",
                text_color="#ffffff" if is_active else "#334155",
                border_width=1 if not is_active else 0,
                border_color="#cbd5e1",
                hover_color="#27272a" if is_active else "#f1f5f9",
                command=lambda c=cat_name: self.select_category(c)
            )
            cat_btn.pack(side="left", padx=5)
            self.category_buttons[cat_name] = cat_btn

    def _build_main_catalog(self):
        # Catalog container inside pos_view with smooth rounded corners and proper padding
        self.catalog_container = customtkinter.CTkFrame(
            self.pos_view,
            fg_color="#f8fafc",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.catalog_container.grid(row=0, column=0, sticky="nsew", padx=(16, 12), pady=18)
        self.catalog_container.grid_rowconfigure(3, weight=1)
        self.catalog_container.grid_columnconfigure(0, weight=1)

        # Top Header (Greeting & Date) with generous padding
        header_frame = customtkinter.CTkFrame(self.catalog_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 14))

        greeting_label = customtkinter.CTkLabel(
            header_frame,
            text=f"Good morning, {self.current_user}!",
            font=customtkinter.CTkFont(size=28, weight="bold"),
            text_color="#09090b"
        )
        greeting_label.grid(row=0, column=0, sticky="w")

        role_tag = f"Role: {self.current_role} · " if hasattr(self, "current_role") and self.current_role else ""
        date_label = customtkinter.CTkLabel(
            header_frame,
            text=f"{role_tag}{datetime.now().strftime('%A, %B %d, %Y')}",
            font=customtkinter.CTkFont(size=13),
            text_color="#64748b"
        )
        date_label.grid(row=1, column=0, sticky="w", pady=(3, 0))

        # Sub-header: Build an order + Search bar (responsive)
        sub_bar = customtkinter.CTkFrame(self.catalog_container, fg_color="transparent")
        sub_bar.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 14))
        sub_bar.grid_columnconfigure(0, weight=1)
        sub_bar.grid_columnconfigure(1, weight=0)

        build_info_frame = customtkinter.CTkFrame(sub_bar, fg_color="transparent")
        build_info_frame.grid(row=0, column=0, sticky="w")

        build_label = customtkinter.CTkLabel(
            build_info_frame,
            text="Build an order",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="#09090b"
        )
        build_label.grid(row=0, column=0, sticky="w")

        self.available_items_label = customtkinter.CTkLabel(
            build_info_frame,
            text="0 items available today",
            font=customtkinter.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.available_items_label.grid(row=1, column=0, sticky="w")

        # Search Entry with live filtering
        self.search_entry = customtkinter.CTkEntry(
            sub_bar,
            placeholder_text="🔍 Search menu",
            width=260,
            height=40,
            corner_radius=14,
            fg_color="#ffffff",
            border_color="#cbd5e1"
        )
        self.search_entry.grid(row=0, column=1, sticky="e")
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Category Filter Pills (Horizontal scrollable, rounded pills)
        self.categories_bar = customtkinter.CTkScrollableFrame(
            self.catalog_container,
            height=52,
            orientation="horizontal",
            fg_color="transparent"
        )
        self.categories_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))

        # Responsive Product Cards Grid
        self.products_scroll = customtkinter.CTkScrollableFrame(
            self.catalog_container,
            fg_color="transparent"
        )
        self.products_scroll.grid(row=3, column=0, sticky="nsew", padx=16, pady=(0, 16))

        # Initial synchronization with Product Management
        self.sync_products_from_management()
        self.render_product_cards()

    def render_product_cards(self):
        """Render product cards based on active category and search filter."""
        # Clear existing cards
        for widget in self.products_scroll.winfo_children():
            widget.destroy()

        # Filter items
        filtered_products = []
        for p in self.catalog_products:
            matches_cat = (self.active_category == "🔥 All Items" or p["category"] == self.active_category)
            matches_search = (self.search_query.lower() in p["name"].lower() or self.search_query.lower() in p["category"].lower())
            if matches_cat and matches_search:
                filtered_products.append(p)

        # Update available label
        self.available_items_label.configure(text=f"{len(filtered_products)} items available today")

        # Configure columns with weights
        cols = self.current_grid_columns
        for c in range(cols):
            self.products_scroll.grid_columnconfigure(c, weight=1)

        for p_idx, product in enumerate(filtered_products):
            row_pos = p_idx // cols
            col_pos = p_idx % cols

            card = customtkinter.CTkFrame(
                self.products_scroll,
                fg_color="#ffffff",
                corner_radius=16,
                border_width=1,
                border_color="#e2e8f0"
            )
            card.grid(row=row_pos, column=col_pos, padx=6, pady=6, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            # Product Image Container with rounded borders
            img_box = customtkinter.CTkFrame(
                card,
                height=110,
                corner_radius=12,
                fg_color="#f8fafc"
            )
            img_box.grid(row=0, column=0, padx=8, pady=(8, 6), sticky="nsew")
            img_box.grid_propagate(False)

            prod_img = self.get_cached_product_image(product.get("image_filename"), size=(160, 95))
            if prod_img:
                img_label = customtkinter.CTkLabel(
                    img_box,
                    image=prod_img,
                    text=""
                )
                img_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                img_icon = customtkinter.CTkLabel(
                    img_box,
                    text=product.get("icon", "🍔"),
                    font=customtkinter.CTkFont(size=38)
                )
                img_icon.place(relx=0.5, rely=0.5, anchor="center")

            # Small food category badge in corner
            cat_badge = customtkinter.CTkLabel(
                img_box,
                text=product["icon"],
                font=customtkinter.CTkFont(size=14)
            )
            cat_badge.place(relx=0.88, rely=0.18, anchor="center")

            # Title
            title_lbl = customtkinter.CTkLabel(
                card,
                text=product["name"],
                font=customtkinter.CTkFont(size=13, weight="bold"),
                text_color="#09090b",
                anchor="w"
            )
            title_lbl.grid(row=1, column=0, padx=10, pady=(2, 0), sticky="w")

            # Subtitle (Category & Stock)
            sub_lbl = customtkinter.CTkLabel(
                card,
                text=product["sub"],
                font=customtkinter.CTkFont(size=11),
                text_color="#94a3b8",
                anchor="w"
            )
            sub_lbl.grid(row=2, column=0, padx=10, pady=(0, 6), sticky="w")

            # Bottom row (Price + Green Add Button)
            price_row = customtkinter.CTkFrame(card, fg_color="transparent")
            price_row.grid(row=3, column=0, padx=10, pady=(0, 8), sticky="ew")
            price_row.grid_columnconfigure(0, weight=1)

            price_lbl = customtkinter.CTkLabel(
                price_row,
                text=f"₱{product['price']:,.0f}",
                font=customtkinter.CTkFont(size=14, weight="bold"),
                text_color="#09090b"
            )
            price_lbl.grid(row=0, column=0, sticky="w")

            add_btn = customtkinter.CTkButton(
                price_row,
                text="+",
                width=32,
                height=32,
                corner_radius=8,
                font=customtkinter.CTkFont(size=16, weight="bold"),
                fg_color="#10b981",
                text_color="#ffffff",
                hover_color="#059669",
                command=lambda p=product: self.add_to_cart(p)
            )
            add_btn.grid(row=0, column=1, sticky="e")

    def _build_checkout_panel(self):
        self.checkout_frame = customtkinter.CTkFrame(
            self.pos_view,
            fg_color="#ffffff",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.checkout_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 18), pady=18)
        self.checkout_frame.grid_rowconfigure(1, weight=1)
        self.checkout_frame.grid_columnconfigure(0, weight=1)

        # Checkout Title
        title_box = customtkinter.CTkFrame(self.checkout_frame, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=18, pady=(18, 8), sticky="ew")

        checkout_title = customtkinter.CTkLabel(
            title_box,
            text="Checkout",
            font=customtkinter.CTkFont(size=22, weight="bold"),
            text_color="#09090b"
        )
        checkout_title.pack(anchor="center")

        # Scrollable items list
        self.order_scroll = customtkinter.CTkScrollableFrame(self.checkout_frame, fg_color="transparent")
        self.order_scroll.grid(row=1, column=0, padx=14, pady=4, sticky="nsew")
        self.order_scroll.grid_columnconfigure(1, weight=1)

        # Add order note input
        self.note_entry = customtkinter.CTkEntry(
            self.checkout_frame,
            placeholder_text="📝 Add order note",
            height=36,
            corner_radius=10,
            fg_color="#f8fafc",
            border_color="#e2e8f0"
        )
        self.note_entry.grid(row=2, column=0, padx=18, pady=8, sticky="ew")

        # Financial Breakdown
        breakdown_box = customtkinter.CTkFrame(self.checkout_frame, fg_color="transparent")
        breakdown_box.grid(row=3, column=0, padx=18, pady=(4, 8), sticky="ew")
        breakdown_box.grid_columnconfigure(0, weight=1)

        # Subtotal
        sub_l = customtkinter.CTkLabel(breakdown_box, text="Subtotal", font=customtkinter.CTkFont(size=12), text_color="#64748b")
        sub_l.grid(row=0, column=0, sticky="w", pady=1)
        self.subtotal_label = customtkinter.CTkLabel(breakdown_box, text="₱0.00", font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#09090b")
        self.subtotal_label.grid(row=0, column=1, sticky="e", pady=1)

        # VAT included
        vat_l = customtkinter.CTkLabel(breakdown_box, text="VAT included", font=customtkinter.CTkFont(size=12), text_color="#64748b")
        vat_l.grid(row=1, column=0, sticky="w", pady=1)
        self.vat_label = customtkinter.CTkLabel(breakdown_box, text="₱0.00", font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#09090b")
        self.vat_label.grid(row=1, column=1, sticky="e", pady=1)

        # Service charge
        svc_l = customtkinter.CTkLabel(breakdown_box, text="Service charge", font=customtkinter.CTkFont(size=12), text_color="#64748b")
        svc_l.grid(row=2, column=0, sticky="w", pady=1)
        self.service_charge_label = customtkinter.CTkLabel(breakdown_box, text="₱0.00", font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#09090b")
        self.service_charge_label.grid(row=2, column=1, sticky="e", pady=1)

        # Total Line
        total_box = customtkinter.CTkFrame(self.checkout_frame, fg_color="transparent")
        total_box.grid(row=4, column=0, padx=18, pady=(6, 12), sticky="ew")
        total_box.grid_columnconfigure(0, weight=1)

        tot_label = customtkinter.CTkLabel(
            total_box,
            text="Total",
            font=customtkinter.CTkFont(size=15, weight="bold"),
            text_color="#09090b"
        )
        tot_label.grid(row=0, column=0, sticky="w")

        self.tot_price_label = customtkinter.CTkLabel(
            total_box,
            text="₱0.00",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color="#09090b"
        )
        self.tot_price_label.grid(row=0, column=1, sticky="e")

        # Payment Method Pills (Responsive)
        payment_methods_box = customtkinter.CTkFrame(self.checkout_frame, fg_color="transparent")
        payment_methods_box.grid(row=5, column=0, padx=18, pady=(0, 14), sticky="ew")
        payment_methods_box.grid_columnconfigure(0, weight=1)
        payment_methods_box.grid_columnconfigure(1, weight=1)
        payment_methods_box.grid_columnconfigure(2, weight=1)

        methods = ["Cash", "GCash", "Card"]
        for m_idx, m_name in enumerate(methods):
            is_m_active = (m_name == self.active_payment_method)
            m_btn = customtkinter.CTkButton(
                payment_methods_box,
                text=f"{'💵' if m_name=='Cash' else ('📱' if m_name=='GCash' else '💳')} {m_name}",
                height=36,
                corner_radius=10,
                font=customtkinter.CTkFont(size=12, weight="bold" if is_m_active else "normal"),
                fg_color="#18181b" if is_m_active else "#ffffff",
                text_color="#ffffff" if is_m_active else "#334155",
                border_width=1 if not is_m_active else 0,
                border_color="#cbd5e1",
                hover_color="#27272a" if is_m_active else "#f1f5f9",
                command=lambda m=m_name: self.select_payment_method(m)
            )
            m_btn.grid(row=0, column=m_idx, padx=3, sticky="ew")
            self.payment_buttons[m_name] = m_btn

        # Row 6: Cash Tendered & Change Section (Responsive)
        self.cash_tender_frame = customtkinter.CTkFrame(
            self.checkout_frame,
            fg_color="#f8fafc",
            corner_radius=12,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.cash_tender_frame.grid(row=6, column=0, padx=18, pady=(0, 12), sticky="ew")

        # Header: Title & Change Due Badge
        tender_header = customtkinter.CTkFrame(self.cash_tender_frame, fg_color="transparent")
        tender_header.pack(fill="x", padx=12, pady=(10, 4))
        tender_header.grid_columnconfigure(0, weight=1)

        self.cash_tender_title = customtkinter.CTkLabel(
            tender_header,
            text="💵 Cash Given by Customer:",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color="#334155"
        )
        self.cash_tender_title.grid(row=0, column=0, sticky="w")

        self.change_due_label = customtkinter.CTkLabel(
            tender_header,
            text="Change: ₱0.00",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color="#059669"
        )
        self.change_due_label.grid(row=0, column=1, sticky="e")

        # Cash Input Box & Exact Button Row
        self.cash_input_row = customtkinter.CTkFrame(self.cash_tender_frame, fg_color="transparent")
        self.cash_input_row.pack(fill="x", padx=12, pady=(0, 6))
        self.cash_input_row.grid_columnconfigure(0, weight=1)

        self.cash_tendered_entry = customtkinter.CTkEntry(
            self.cash_input_row,
            placeholder_text="Enter cash (e.g. 1000)",
            height=36,
            corner_radius=8,
            fg_color="#ffffff",
            border_color="#cbd5e1",
            font=customtkinter.CTkFont(size=13, weight="bold")
        )
        self.cash_tendered_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.cash_tendered_entry.bind("<KeyRelease>", self.on_cash_tendered_change)
        self.cash_tendered_entry.bind("<Return>", lambda e: self.open_payment_complete_window())

        self.exact_cash_btn = customtkinter.CTkButton(
            self.cash_input_row,
            text="Exact",
            width=54,
            height=36,
            corner_radius=8,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="#e2e8f0",
            text_color="#0f172a",
            hover_color="#cbd5e1",
            command=self.set_exact_cash
        )
        self.exact_cash_btn.grid(row=0, column=1, sticky="e")

        # Quick Denomination Presets Row
        self.presets_row = customtkinter.CTkFrame(self.cash_tender_frame, fg_color="transparent")
        self.presets_row.pack(fill="x", padx=12, pady=(0, 10))
        for p_idx in range(4):
            self.presets_row.grid_columnconfigure(p_idx, weight=1)

        preset_denominations = [100, 200, 500, 1000]
        for p_idx, p_val in enumerate(preset_denominations):
            p_btn = customtkinter.CTkButton(
                self.presets_row,
                text=f"₱{p_val:,}",
                height=26,
                corner_radius=6,
                font=customtkinter.CTkFont(size=11, weight="bold"),
                fg_color="#ffffff",
                border_width=1,
                border_color="#e2e8f0",
                text_color="#475569",
                hover_color="#f1f5f9",
                command=lambda val=p_val: self.set_preset_cash(val)
            )
            p_btn.grid(row=0, column=p_idx, padx=2, sticky="ew")

        # Digital Payment Info Label (shown when GCash or Card is active)
        self.digital_pay_info_lbl = customtkinter.CTkLabel(
            self.cash_tender_frame,
            text="📱 Digital Payment: Exact charge will be billed.",
            font=customtkinter.CTkFont(size=12),
            text_color="#64748b"
        )

        # Row 7: Action Buttons: Receipt Preview & Charge Button (Responsive)
        action_btns_frame = customtkinter.CTkFrame(self.checkout_frame, fg_color="transparent")
        action_btns_frame.grid(row=7, column=0, padx=18, pady=(0, 18), sticky="ew")
        action_btns_frame.grid_columnconfigure(0, weight=1)
        action_btns_frame.grid_columnconfigure(1, weight=2)

        self.receipt_btn = customtkinter.CTkButton(
            action_btns_frame,
            text="🧾 Receipt",
            height=48,
            corner_radius=12,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            fg_color="#18181b",
            text_color="#ffffff",
            hover_color="#27272a",
            command=self.open_payment_complete_window
        )
        self.receipt_btn.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.charge_btn = customtkinter.CTkButton(
            action_btns_frame,
            text="➔ Charge ₱0.00",
            height=48,
            corner_radius=12,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            text_color="#ffffff",
            hover_color="#059669",
            command=self.open_payment_complete_window
        )
        self.charge_btn.grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def add_to_cart(self, product):
        """Add product to cart or increment quantity."""
        name = product["name"]
        if name in self.cart_items:
            self.cart_items[name]["qty"] += 1
        else:
            self.cart_items[name] = {
                "qty": 1,
                "price": product["price"],
                "notes": product.get("sub", "")
            }
        self.recalculate_totals()
        self.refresh_cart_display()

    def increment_cart_item(self, item_name):
        """Increment item count."""
        if item_name in self.cart_items:
            self.cart_items[item_name]["qty"] += 1
            self.recalculate_totals()
            self.refresh_cart_display()

    def decrement_cart_item(self, item_name):
        """Decrement item count, removing if 0."""
        if item_name in self.cart_items:
            self.cart_items[item_name]["qty"] -= 1
            if self.cart_items[item_name]["qty"] <= 0:
                del self.cart_items[item_name]
            self.recalculate_totals()
            self.refresh_cart_display()

    def reset_cart(self):
        """Reset the cart to empty and clear cash input."""
        self.cart_items.clear()
        if hasattr(self, "cash_tendered_entry"):
            self.cash_tendered_entry.delete(0, "end")
        if hasattr(self, "change_due_label"):
            self.change_due_label.configure(text="Change: ₱0.00", text_color="#059669")
        self.recalculate_totals()
        self.refresh_cart_display()

    def recalculate_totals(self):
        """Calculate subtotal, VAT, service charge, and total."""
        subtotal = 0.0
        for item in self.cart_items.values():
            subtotal += item["price"] * item["qty"]

        # VAT included is roughly 12% of VATable
        vat = (subtotal / 1.12) * 0.12 if subtotal > 0 else 0.0
        service_charge = subtotal * 0.10 if subtotal > 0 else 0.0
        total = subtotal + service_charge

        self.calculated_subtotal = subtotal
        self.calculated_vat = vat
        self.calculated_service_charge = service_charge
        self.calculated_total = total

        self.subtotal_label.configure(text=f"₱{subtotal:,.2f}")
        self.vat_label.configure(text=f"₱{vat:,.2f}")
        self.service_charge_label.configure(text=f"₱{service_charge:,.2f}")
        self.tot_price_label.configure(text=f"₱{total:,.2f}")
        self.charge_btn.configure(text=f"➔ Charge ₱{total:,.2f}")

        if hasattr(self, "cash_tendered_entry"):
            self.on_cash_tendered_change()

    def refresh_cart_display(self):
        """Re-render the items in checkout order_scroll."""
        for widget in self.order_scroll.winfo_children():
            widget.destroy()

        if not self.cart_items:
            empty_lbl = customtkinter.CTkLabel(
                self.order_scroll,
                text="No items in order yet.\nClick + on any product to add.",
                font=customtkinter.CTkFont(size=12),
                text_color="#94a3b8"
            )
            empty_lbl.grid(row=0, column=0, columnspan=2, pady=30)
            return

        for idx, (item_name, item_info) in enumerate(self.cart_items.items()):
            item_row = customtkinter.CTkFrame(self.order_scroll, fg_color="transparent")
            item_row.grid(row=idx, column=0, columnspan=2, sticky="ew", pady=5)
            item_row.grid_columnconfigure(1, weight=1)

            # Qty badge (rounded)
            qty_badge = customtkinter.CTkButton(
                item_row,
                text=str(item_info["qty"]),
                width=28,
                height=28,
                corner_radius=8,
                font=customtkinter.CTkFont(size=12, weight="bold"),
                fg_color="#18181b",
                text_color="#ffffff",
                hover=False
            )
            qty_badge.grid(row=0, column=0, rowspan=2, padx=(0, 8), sticky="n")

            # Name
            name_lbl = customtkinter.CTkLabel(
                item_row,
                text=item_name,
                font=customtkinter.CTkFont(size=13, weight="bold"),
                text_color="#09090b"
            )
            name_lbl.grid(row=0, column=1, sticky="w")

            # Price
            line_total = item_info["price"] * item_info["qty"]
            price_lbl = customtkinter.CTkLabel(
                item_row,
                text=f"₱{line_total:,.0f}",
                font=customtkinter.CTkFont(size=13, weight="bold"),
                text_color="#09090b"
            )
            price_lbl.grid(row=0, column=2, sticky="e")

            # Sub-row for notes + steppers
            sub_row = customtkinter.CTkFrame(item_row, fg_color="transparent")
            sub_row.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(2, 0))
            sub_row.grid_columnconfigure(0, weight=1)

            notes_lbl = customtkinter.CTkLabel(
                sub_row,
                text=item_info.get("notes", ""),
                font=customtkinter.CTkFont(size=11),
                text_color="#94a3b8"
            )
            notes_lbl.grid(row=0, column=0, sticky="w")

            # Stepper pill
            stepper_frame = customtkinter.CTkFrame(sub_row, fg_color="#f1f5f9", corner_radius=14)
            stepper_frame.grid(row=0, column=1, sticky="e")

            minus_btn = customtkinter.CTkButton(
                stepper_frame, text="−", width=22, height=22, corner_radius=11,
                fg_color="transparent", text_color="#64748b", hover_color="#e2e8f0",
                command=lambda n=item_name: self.decrement_cart_item(n)
            )
            minus_btn.pack(side="left", padx=2)

            qty_val = customtkinter.CTkLabel(
                stepper_frame, text=str(item_info["qty"]), font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#09090b"
            )
            qty_val.pack(side="left", padx=4)

            plus_btn = customtkinter.CTkButton(
                stepper_frame, text="+", width=22, height=22, corner_radius=11,
                fg_color="transparent", text_color="#10b981", hover_color="#e2e8f0",
                command=lambda n=item_name: self.increment_cart_item(n)
            )
            plus_btn.pack(side="left", padx=2)

    def select_category(self, cat_name):
        """Update active category pill style and filter catalog."""
        self.active_category = cat_name
        for name, btn in self.category_buttons.items():
            is_act = (name == cat_name)
            btn.configure(
                fg_color="#18181b" if is_act else "#ffffff",
                text_color="#ffffff" if is_act else "#334155",
                font=customtkinter.CTkFont(size=13, weight="bold" if is_act else "normal"),
                border_width=0 if is_act else 1
            )
        self.render_product_cards()

    def select_payment_method(self, method_name):
        """Highlight chosen payment method and adapt cash/digital payment view."""
        self.active_payment_method = method_name
        for name, btn in self.payment_buttons.items():
            is_act = (name == method_name)
            btn.configure(
                fg_color="#18181b" if is_act else "#ffffff",
                text_color="#ffffff" if is_act else "#334155",
                font=customtkinter.CTkFont(size=12, weight="bold" if is_act else "normal"),
                border_width=0 if is_act else 1
            )

        if hasattr(self, "cash_tender_frame"):
            if method_name == "Cash":
                self.digital_pay_info_lbl.pack_forget()
                self.cash_input_row.pack(fill="x", padx=12, pady=(0, 6))
                self.presets_row.pack(fill="x", padx=12, pady=(0, 10))
                self.cash_tender_title.configure(text="💵 Cash Given by Customer:")
                self.on_cash_tendered_change()
            else:
                self.cash_input_row.pack_forget()
                self.presets_row.pack_forget()
                self.digital_pay_info_lbl.pack(fill="x", padx=12, pady=(4, 10))
                icon = "📱" if method_name == "GCash" else "💳"
                self.cash_tender_title.configure(text=f"{icon} {method_name} Selected:")
                self.digital_pay_info_lbl.configure(text=f"Exact amount of ₱{self.calculated_total:,.2f} will be billed.")
                self.change_due_label.configure(text="Exact Amount", text_color="#059669")

    def on_cash_tendered_change(self, event=None):
        """Calculates real-time change due as the cashier enters customer cash."""
        if not hasattr(self, "cash_tendered_entry") or not hasattr(self, "change_due_label"):
            return

        if self.active_payment_method != "Cash":
            self.change_due_label.configure(text="Exact Amount", text_color="#059669")
            return

        raw_val = self.cash_tendered_entry.get().strip().replace("₱", "").replace(",", "")
        if not raw_val:
            self.change_due_label.configure(text="Change: ₱0.00", text_color="#64748b")
            return

        try:
            tendered = float(raw_val)
        except ValueError:
            self.change_due_label.configure(text="Invalid Amount", text_color="#dc2626")
            return

        change = tendered - self.calculated_total
        if change >= 0:
            self.change_due_label.configure(
                text=f"Change: ₱{change:,.2f}",
                text_color="#059669"
            )
        else:
            shortage = abs(change)
            self.change_due_label.configure(
                text=f"Short: ₱{shortage:,.2f}",
                text_color="#dc2626"
            )

    def set_exact_cash(self):
        """Sets customer cash given to exact order total."""
        if self.calculated_total <= 0:
            return
        self.cash_tendered_entry.delete(0, "end")
        self.cash_tendered_entry.insert(0, f"{self.calculated_total:.2f}")
        self.on_cash_tendered_change()

    def set_preset_cash(self, amount):
        """Sets customer cash given to a preset denomination."""
        self.cash_tendered_entry.delete(0, "end")
        self.cash_tendered_entry.insert(0, f"{amount:.0f}")
        self.on_cash_tendered_change()

    def get_cash_received_amount(self) -> float:
        """Parses entered cash amount with safety defaults."""
        if self.active_payment_method != "Cash":
            return self.calculated_total

        if not hasattr(self, "cash_tendered_entry"):
            return 0.0

        raw_val = self.cash_tendered_entry.get().strip().replace("₱", "").replace(",", "")
        if not raw_val:
            return 0.0

        try:
            val = float(raw_val)
            return max(0.0, val)
        except ValueError:
            return 0.0

    def on_search_change(self, event=None):
        """Filter product cards as query changes."""
        self.search_query = self.search_entry.get().strip()
        self.render_product_cards()

    def on_window_resize(self, event):
        """Adjust product card columns dynamically to maintain responsive sizing."""
        if event.widget == self:
            available_width = event.width
            # Determine optimal grid columns
            if available_width < 1180:
                target_cols = 2
            elif available_width < 1380:
                target_cols = 3
            else:
                target_cols = 4

            if target_cols != self.current_grid_columns:
                self.current_grid_columns = target_cols
                self.render_product_cards()

    def open_payment_complete_window(self):
        """Open the pop-up receipt window (BastaReceiptWindow) with active order data and process sale."""
        from tkinter import messagebox

        if not self.cart_items:
            print("[BASTA POS] Cannot checkout: Cart is empty.")
            messagebox.showwarning("Cart Empty", "Cannot checkout: The cart is empty. Please add items to order first.")
            if hasattr(self, "change_due_label"):
                self.change_due_label.configure(text="Cart is empty", text_color="#dc2626")
            return

        # Validate cash amount when customer chooses Cash payment
        if self.active_payment_method == "Cash":
            raw_cash = ""
            if hasattr(self, "cash_tendered_entry"):
                raw_cash = self.cash_tendered_entry.get().strip().replace("₱", "").replace(",", "")

            if not raw_cash:
                print("[BASTA POS] Cannot checkout: Cash amount was not entered.")
                messagebox.showwarning(
                    "Cash Amount Required",
                    "Please enter the cash amount given by the customer before checking out.\n\n"
                    "You can type the amount or click 'Exact' / preset bills (₱200, ₱500, ₱1,000, etc.)."
                )
                if hasattr(self, "change_due_label"):
                    self.change_due_label.configure(
                        text="Enter cash amount!",
                        text_color="#dc2626"
                    )
                if hasattr(self, "cash_tendered_entry"):
                    self.cash_tendered_entry.focus()
                return

            try:
                cash_rec = float(raw_cash)
                if cash_rec <= 0:
                    raise ValueError("Amount must be greater than zero.")
            except ValueError:
                print("[BASTA POS] Cannot checkout: Invalid cash amount.")
                messagebox.showwarning(
                    "Invalid Cash Amount",
                    "Please enter a valid numeric cash amount greater than zero."
                )
                if hasattr(self, "change_due_label"):
                    self.change_due_label.configure(
                        text="Invalid amount",
                        text_color="#dc2626"
                    )
                if hasattr(self, "cash_tendered_entry"):
                    self.cash_tendered_entry.focus()
                return

            if cash_rec < self.calculated_total:
                shortage = self.calculated_total - cash_rec
                print(f"[BASTA POS] Cannot checkout: Cash received (PHP {cash_rec:,.2f}) is short by PHP {shortage:,.2f}.")
                messagebox.showwarning(
                    "Insufficient Cash",
                    f"Cash received (₱{cash_rec:,.2f}) is short by ₱{shortage:,.2f}.\n\n"
                    f"Order Total: ₱{self.calculated_total:,.2f}\n"
                    f"Cash Given:  ₱{cash_rec:,.2f}"
                )
                if hasattr(self, "change_due_label"):
                    self.change_due_label.configure(
                        text=f"Short: ₱{shortage:,.2f}",
                        text_color="#dc2626"
                    )
                if hasattr(self, "cash_tendered_entry"):
                    self.cash_tendered_entry.focus()
                return
        else:
            cash_rec = self.calculated_total

        chg_due = max(0.0, cash_rec - self.calculated_total)

        items_list = []
        for name, info in self.cart_items.items():
            items_list.append({
                "name": name,
                "qty": info["qty"],
                "price": info["price"]
            })

        self.order_counter += 1
        now_dt = datetime.now()
        timestamp_str = now_dt.strftime("%m%d%H%M%S")
        order_id = f"#B-{self.order_counter}"
        txn_id = f"TXN-{timestamp_str}-{self.order_counter}"
        receipt_num = f"OR-{now_dt.year}-{self.order_counter:05d}"
        date_str = now_dt.strftime("%d %b %Y - %I:%M %p")
        time_str = now_dt.strftime("%I:%M %p")

        # 1. Deduct stock in Product Management memory & MySQL database
        try:
            from database import deduct_product_stock
        except Exception:
            try:
                from ProjectMain.database import deduct_product_stock
            except Exception:
                deduct_product_stock = None

        if hasattr(self, "products_view") and hasattr(self.products_view, "products_data"):
            for item in items_list:
                item_name = item["name"]
                item_qty = item["qty"]
                for p in self.products_view.products_data:
                    if p.get("name") == item_name:
                        current_stk = p.get("stock", 0)
                        p["stock"] = max(0, current_stk - item_qty)
                        break
                if deduct_product_stock:
                    try:
                        deduct_product_stock(item_name, item_qty)
                    except Exception as err:
                        print(f"[BASTA POS] Deduct stock notice: {err}")

            # Refresh product management drawer and list if currently viewed
            if hasattr(self.products_view, "populate_drawer") and self.products_view.selected_product:
                self.products_view.populate_drawer(self.products_view.selected_product)
            if hasattr(self.products_view, "render_product_list"):
                self.products_view.render_product_list()

        # 2. Record Completed Transaction in Reports
        items_summary = ", ".join(f"{it['qty']}× {it['name']}" for it in items_list)
        if hasattr(self, "reports_view") and hasattr(self.reports_view, "add_completed_transaction"):
            try:
                self.reports_view.add_completed_transaction(
                    t_id=txn_id,
                    ord_id=order_id,
                    t_time=time_str,
                    itm=items_summary,
                    pay=self.active_payment_method,
                    cash=self.current_user,
                    tot_val=self.calculated_total
                )
            except Exception as err:
                print(f"[BASTA POS] Reports transaction log notice: {err}")

        # 3. Record transaction in MySQL database
        try:
            from database import record_sale_transaction
        except Exception:
            try:
                from ProjectMain.database import record_sale_transaction
            except Exception:
                record_sale_transaction = None

        if record_sale_transaction:
            try:
                record_sale_transaction(
                    transaction_id=txn_id,
                    order_id=order_id,
                    table_num="Table 12",
                    cashier_name=self.current_user,
                    payment_method=self.active_payment_method,
                    subtotal=self.calculated_subtotal,
                    vat=self.calculated_vat,
                    service_charge=self.calculated_service_charge,
                    total=self.calculated_total,
                    cash_received=cash_rec,
                    change_due=chg_due,
                    items=items_list
                )
            except Exception as err:
                print(f"[BASTA POS] Sale recording notice: {err}")

        # Synchronize POS product stock immediately
        self.sync_products_from_management()

        order_data = {
            "order_id": order_id,
            "table_num": "Table 12",
            "receipt_num": receipt_num,
            "cashier_name": self.current_user,
            "transaction_id": txn_id,
            "date_str": date_str,
            "items": items_list,
            "subtotal": self.calculated_subtotal,
            "vat": self.calculated_vat,
            "service_charge": self.calculated_service_charge,
            "total": self.calculated_total,
            "payment_method": self.active_payment_method,
            "cash_received": cash_rec,
            "change_due": chg_due
        }

        try:
            from receipt import BastaReceiptWindow
            receipt_window = BastaReceiptWindow(self, order_data=order_data)
        except Exception:
            try:
                from ProjectMain.receipt import BastaReceiptWindow
                receipt_window = BastaReceiptWindow(self, order_data=order_data)
            except Exception:
                receipt_window = PaymentCompleteWindow(self, order_data=order_data)
        receipt_window.grab_set()

    def open_products_screen(self):
        """Navigate to the Product Management view."""
        self.switch_view("products")

    def open_inventory_screen(self):
        """Navigate to the Inventory Overview view."""
        self.switch_view("stock")

    def open_reports_screen(self):
        """Navigate to the Sales and Inventory Reports view."""
        self.switch_view("reports")

    def open_accounts_screen(self):
        """Navigate to the Account Settings view."""
        self.switch_view("settings")

    def destroy(self):
        """Safely cancels all pending Tcl after callbacks before destruction to prevent Tcl script errors."""
        try:
            for after_id in self.tk.call("after", "info"):
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
        except Exception:
            pass
        try:
            super().destroy()
        except Exception:
            pass

    def handle_logout(self):
        """Transition back to the login page."""
        self.destroy()
        try:
            from login import BastaLoginApp
            login_app = BastaLoginApp()
            login_app.mainloop()
        except Exception:
            try:
                from ProjectMain.login import BastaLoginApp
                login_app = BastaLoginApp()
                login_app.mainloop()
            except Exception as error:
                print(f"[BASTA POS] Logout redirect error: {error}")


if __name__ == "__main__":
    app = BastaPOSApp()
    app.mainloop()
