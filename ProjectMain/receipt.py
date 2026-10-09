"""
BASTA BURGER - POS and Inventory Management System
Receipt Window Module (Popup Window for POS.py)
Faithfully recreates the digital tablet receipt and payment confirmation
from Designs/BASTA_RECEIPT.png using CustomTkinter and Pillow.
All variables and functions strictly use snake_case.
"""

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

# Configure appearance
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Path to basta_LOGO.png
logo_path = os.path.join(project_root, "Designs", "basta_LOGO.png")

try:
    raw_logo_pil = Image.open(logo_path)
except Exception:
    raw_logo_pil = None


def get_logo_image(size=(60, 60)):
    """Return a CTkImage for basta_LOGO.png or None if unavailable."""
    if raw_logo_pil:
        return customtkinter.CTkImage(light_image=raw_logo_pil, dark_image=raw_logo_pil, size=size)
    return None


class BastaReceiptWindow(customtkinter.CTkToplevel):
    """
    Receipt pop-up window for POS.py matching Designs/BASTA_RECEIPT.png.
    Displays payment confirmation on the left and a digital tablet receipt on the right.
    """

    def __init__(self, parent_window=None, order_data=None):
        super().__init__(parent_window)

        self.parent_window = parent_window

        # Default sample data matching BASTA_RECEIPT.png if none provided
        self.order_data = order_data or {
            "order_id": "#B-1048",
            "table_num": "Table 12",
            "receipt_num": "OR-2026-01048",
            "cashier_name": "Bea M.",
            "transaction_id": "TXN-0928-001048",
            "date_str": "28 Sep 2026 - 9:48 AM",
            "items": [
                {"name": "Basta Smash Burger", "qty": 2, "price": 285.0},
                {"name": "Truffle Parm Fries", "qty": 1, "price": 145.0},
                {"name": "Ube Milkshake", "qty": 1, "price": 165.0}
            ],
            "subtotal": 880.0,
            "vat": 94.29,
            "service_charge": 88.0,
            "total": 968.0,
            "payment_method": "Cash",
            "cash_received": 1000.0,
            "change_due": 32.0
        }

        self.title("BASTA POS - Receipt & Payment Complete")
        self.geometry("1180x760")
        self.minsize(980, 650)

        # Center on screen if parent exists
        if parent_window:
            pos_x = max(20, parent_window.winfo_x() + 40)
            pos_y = max(20, parent_window.winfo_y() + 30)
            self.geometry(f"+{pos_x}+{pos_y}")

        # Configure root layout for responsiveness (2 columns: left confirmation, right tablet receipt)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)  # Left confirmation panel
        self.grid_columnconfigure(1, weight=2)  # Right tablet receipt panel

        self._build_confirmation_panel()
        self._build_tablet_receipt()

    def _build_confirmation_panel(self):
        """Constructs the Payment Complete section on the left."""
        center_scroll = customtkinter.CTkScrollableFrame(
            self,
            fg_color="#f8fafc",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        center_scroll.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        center_scroll.grid_columnconfigure(0, weight=1)

        order_id = self.order_data.get("order_id", "#B-1048")
        table_num = self.order_data.get("table_num", "Table 12")
        time_str = datetime.now().strftime("%I:%M %p")

        # Header Titles
        main_title = customtkinter.CTkLabel(
            center_scroll,
            text="Payment complete",
            font=customtkinter.CTkFont(size=30, weight="bold"),
            text_color="#09090b"
        )
        main_title.grid(row=0, column=0, sticky="w", pady=(12, 2), padx=6)

        sub_title = customtkinter.CTkLabel(
            center_scroll,
            text=f"Order {order_id} · {table_num} · {time_str}",
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

        # Huge Paid Amount
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
            text="Cash payment received. The kitchen ticket has been sent and Table 12 is marked as paid.",
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
        change_due = max(0.0, cash_received - total_amount)
        txn_id = self.order_data.get("transaction_id", "TXN-0928-001048")

        detail_items = [
            ("Payment method", pay_method),
            ("Cash received", f"₱{cash_received:,.2f}"),
            ("Change due", f"₱{change_due:,.2f}"),
            ("Transaction ID", txn_id)
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
            command=self.handle_new_order
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
            hover_color="#27272a",
            command=self.handle_print_receipt
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

    def _build_tablet_receipt(self):
        """Constructs the digital tablet containing the white receipt."""
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
            text="#11 Purok 2, Ibayao Marilao Bulacan\nVAT Reg. TIN 009-482-176-000",
            font=customtkinter.CTkFont(size=11),
            text_color="#64748b"
        )
        store_addr.grid(row=current_row, column=0, columnspan=2, pady=(0, 10))
        current_row += 1

        # Receipt Meta
        receipt_num = self.order_data.get("receipt_num", "OR-2026-01048")
        order_id = self.order_data.get("order_id", "#B-1048")
        table_num = self.order_data.get("table_num", "Table 12")
        cashier_name = self.order_data.get("cashier_name", "Bea M.")
        date_str = self.order_data.get("date_str", datetime.now().strftime("%d %b %Y - %I:%M %p"))

        meta_items = [
            ("Receipt", receipt_num),
            ("Order", f"{order_id} · {table_num}"),
            ("Cashier", cashier_name),
            ("Date", date_str)
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

        # Divider 1
        divider_1 = customtkinter.CTkLabel(
            receipt_paper,
            text="--------------------------------------------------",
            text_color="#cbd5e1"
        )
        divider_1.grid(row=current_row, column=0, columnspan=2, pady=5)
        current_row += 1

        # Ordered products item list
        items = self.order_data.get("items", [])
        if not items:
            items = [{"name": "No items", "qty": 1, "price": 0.0}]

        for item in items:
            item_name = item.get("name", "Item")
            qty = item.get("qty", 1)
            unit_price = item.get("price", 0.0)
            line_total = unit_price * qty

            i_lbl = customtkinter.CTkLabel(
                receipt_paper,
                text=f"{qty}×  {item_name}",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#0f172a"
            )
            i_lbl.grid(row=current_row, column=0, sticky="w", padx=14, pady=3)

            i_val = customtkinter.CTkLabel(
                receipt_paper,
                text=f"₱{line_total:,.2f}",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="#0f172a"
            )
            i_val.grid(row=current_row, column=1, sticky="e", padx=14, pady=3)
            current_row += 1

        # Divider 2
        divider_2 = customtkinter.CTkLabel(
            receipt_paper,
            text="--------------------------------------------------",
            text_color="#cbd5e1"
        )
        divider_2.grid(row=current_row, column=0, columnspan=2, pady=5)
        current_row += 1

        # Financial Breakdown
        subtotal = self.order_data.get("subtotal", 880.0)
        vat_sales = subtotal / 1.12 if subtotal > 0 else 0.0
        vat_val = self.order_data.get("vat", (vat_sales * 0.12))
        svc_val = self.order_data.get("service_charge", (subtotal * 0.10))
        total_val = self.order_data.get("total", (subtotal + svc_val))

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
        change_due = max(0.0, cash_received - total_val)

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

    def handle_new_order(self):
        """Reset cart in POS and close the receipt window."""
        if self.parent_window and hasattr(self.parent_window, "reset_cart"):
            self.parent_window.reset_cart()
        self.destroy()

    def destroy(self):
        """Safely cancels all pending Tcl after callbacks before destruction."""
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

    def handle_print_receipt(self):
        """Simulate receipt printing feedback."""
        print("[BASTA POS] Printing receipt...")
        # Can trigger system print or notification dialog if needed


if __name__ == "__main__":
    test_app = customtkinter.CTk()
    test_app.withdraw()  # Hide root window
    receipt_popup = BastaReceiptWindow(test_app)
    receipt_popup.protocol("WM_DELETE_WINDOW", test_app.destroy)
    test_app.mainloop()
