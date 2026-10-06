"""
BASTA BURGER - POS and Inventory Management System
Sales and Inventory Reports Module
Faithfully recreates Designs/ADMIN_REPORTS.png using CustomTkinter and Pillow.
All variables and functions strictly use snake_case.
"""

import os
import sys
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


class ReportsView(customtkinter.CTkFrame):
    """
    Sales and Inventory Reports frame matching Designs/ADMIN_REPORTS.png.
    Can be embedded directly into BastaPOSApp or displayed in any window.
    """

    def __init__(self, master, app_controller=None, **kwargs):
        super().__init__(master, fg_color="#f1f5f9", **kwargs)
        self.app_controller = app_controller

        # Period Filter State: Daily, Weekly, Monthly, Yearly
        self.active_period = "Weekly"
        self.period_buttons = {}

        # Period Data
        self.period_data = {
            "Daily": {
                "date_label": "Today · Monday, Sep 28, 2026",
                "metrics": [
                    {"title": "TODAY'S GROSS SALES", "val": "₱28,450", "diff": "+14.2% vs yesterday", "icon": "💵"},
                    {"title": "NET REVENUE", "val": "₱25,180", "diff": "+11.8% vs yesterday", "icon": "📈"},
                    {"title": "AVG ORDER TICKET", "val": "₱412.30", "diff": "+₱24.50 vs avg", "icon": "🧾"},
                    {"title": "TOTAL ORDERS TODAY", "val": "69 orders", "diff": "+8 orders vs avg", "icon": "👥"}
                ],
                "bars": [
                    ("9 AM", 1200), ("11 AM", 4500), ("1 PM", 7800),
                    ("3 PM", 3400), ("5 PM", 6200), ("7 PM", 9100), ("9 PM", 3250)
                ],
                "max_bar": 10000
            },
            "Weekly": {
                "date_label": "Sep 22 - Sep 28, 2026 (Last 7 Days)",
                "metrics": [
                    {"title": "WEEKLY GROSS SALES", "val": "₱142,890", "diff": "+8.4% vs last week", "icon": "💵"},
                    {"title": "NET REVENUE", "val": "₱127,580", "diff": "+6.2% vs last week", "icon": "📈"},
                    {"title": "AVG ORDER VALUE", "val": "₱385.50", "diff": "+₱12.30 vs target", "icon": "🧾"},
                    {"title": "TOTAL ORDERS", "val": "371 orders", "diff": "+32 orders this week", "icon": "👥"}
                ],
                "bars": [
                    ("Mon", 16800), ("Tue", 18450), ("Wed", 15200),
                    ("Thu", 19800), ("Fri", 26400), ("Sat", 28500), ("Sun", 22740)
                ],
                "max_bar": 30000
            },
            "Monthly": {
                "date_label": "September 1 - September 30, 2026",
                "metrics": [
                    {"title": "MONTHLY GROSS SALES", "val": "₱584,200", "diff": "+18.1% vs last month", "icon": "💵"},
                    {"title": "NET REVENUE", "val": "₱521,400", "diff": "+15.3% vs last month", "icon": "📈"},
                    {"title": "AVG ORDER VALUE", "val": "₱392.10", "diff": "+₱18.40 vs target", "icon": "🧾"},
                    {"title": "TOTAL ORDERS", "val": "1,490 orders", "diff": "+184 orders", "icon": "👥"}
                ],
                "bars": [
                    ("Week 1", 132000), ("Week 2", 148500),
                    ("Week 3", 145000), ("Week 4", 158700)
                ],
                "max_bar": 180000
            },
            "Yearly": {
                "date_label": "Fiscal Year 2026",
                "metrics": [
                    {"title": "ANNUAL GROSS SALES", "val": "₱4,820,000", "diff": "+24.6% vs FY 2025", "icon": "💵"},
                    {"title": "NET REVENUE", "val": "₱4,290,000", "diff": "+22.4% vs FY 2025", "icon": "📈"},
                    {"title": "AVG ORDER VALUE", "val": "₱378.00", "diff": "+₱31.20 vs FY 2025", "icon": "🧾"},
                    {"title": "TOTAL ORDERS", "val": "12,750 orders", "diff": "+2,410 orders", "icon": "👥"}
                ],
                "bars": [
                    ("Q1", 1050000), ("Q2", 1180000),
                    ("Q3", 1240000), ("Q4", 1350000)
                ],
                "max_bar": 1500000
            }
        }

        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_main_content()

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

        # 1. Header with Period Filter Toggle
        top_bar = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 16))
        top_bar.grid_columnconfigure(0, weight=1)

        header_info = customtkinter.CTkFrame(top_bar, fg_color="transparent")
        header_info.grid(row=0, column=0, sticky="w")
        customtkinter.CTkLabel(header_info, text="Sales & Performance Reports", font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#09090b").pack(anchor="w")
        customtkinter.CTkLabel(header_info, text="Comprehensive analytics, product sales breakdown, and audit log", font=customtkinter.CTkFont(size=12), text_color="#64748b").pack(anchor="w")

        # Period Filter Buttons & Date Range
        filter_box = customtkinter.CTkFrame(top_bar, fg_color="transparent")
        filter_box.grid(row=0, column=1, sticky="e")

        pill_container = customtkinter.CTkFrame(filter_box, fg_color="#e2e8f0", corner_radius=10, height=38)
        pill_container.pack(side="left", padx=(0, 10))

        for p_name in ["Daily", "Weekly", "Monthly", "Yearly"]:
            is_active = (p_name == self.active_period)
            p_btn = customtkinter.CTkButton(
                pill_container,
                text=p_name,
                width=70,
                height=30,
                corner_radius=8,
                font=customtkinter.CTkFont(size=11, weight="bold" if is_active else "normal"),
                fg_color="#18181b" if is_active else "transparent",
                text_color="#ffffff" if is_active else "#475569",
                hover_color="#27272a",
                command=lambda p=p_name: self.set_period(p)
            )
            p_btn.pack(side="left", padx=3, pady=3)
            self.period_buttons[p_name] = p_btn

        self.date_range_pill = customtkinter.CTkLabel(
            filter_box,
            text=self.period_data[self.active_period]["date_label"],
            font=customtkinter.CTkFont(size=11, weight="bold"),
            text_color="#047857",
            fg_color="#dcfce7",
            corner_radius=8,
            height=34,
            padx=12
        )
        self.date_range_pill.pack(side="left", padx=4)

        print_btn = customtkinter.CTkButton(
            filter_box,
            text="⎙ Print Report",
            font=customtkinter.CTkFont(size=11, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=34,
            corner_radius=8
        )
        print_btn.pack(side="left", padx=4)

        export_btn = customtkinter.CTkButton(
            filter_box,
            text="⤓ Export CSV",
            font=customtkinter.CTkFont(size=11),
            fg_color="#ffffff",
            text_color="#0f172a",
            hover_color="#f1f5f9",
            border_width=1,
            border_color="#cbd5e1",
            height=34,
            corner_radius=8
        )
        export_btn.pack(side="left", padx=4)

        # 2. Key Metrics Row (4 Dark Cards)
        self.metrics_container = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        self.metrics_container.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        for c in range(4):
            self.metrics_container.grid_columnconfigure(c, weight=1)

        self.render_metric_cards()

        # 3. Bar Chart Card
        self.bar_card = customtkinter.CTkFrame(main_scroll, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        self.bar_card.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        self.bar_card.grid_columnconfigure(0, weight=1)

        self.render_bar_chart()

        # 4. Two Split Cards: Category Share & Top Selling Products
        split_row = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        split_row.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
        split_row.grid_columnconfigure(0, weight=1)
        split_row.grid_columnconfigure(1, weight=1)

        # Left: Category Revenue Share
        cat_card = customtkinter.CTkFrame(split_row, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        cat_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        customtkinter.CTkLabel(cat_card, text="Revenue Share by Category", font=customtkinter.CTkFont(size=14, weight="bold"), text_color="#09090b").pack(anchor="w", padx=16, pady=(14, 10))

        cats = [
            ("Burgers & Sandwiches", 0.54, "₱77,160 (54%)", "#10b981"),
            ("Sides & Fries", 0.21, "₱30,006 (21%)", "#3b82f6"),
            ("Beverages & Shakes", 0.16, "₱22,862 (16%)", "#f59e0b"),
            ("Desserts & Sweets", 0.09, "₱12,860 (9%)", "#8b5cf6")
        ]
        for c_title, c_pct, c_val, c_color in cats:
            row_f = customtkinter.CTkFrame(cat_card, fg_color="transparent")
            row_f.pack(fill="x", padx=16, pady=4)
            customtkinter.CTkLabel(row_f, text=c_title, font=customtkinter.CTkFont(size=11), text_color="#475569").pack(side="left")
            customtkinter.CTkLabel(row_f, text=c_val, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").pack(side="right")

            pb = customtkinter.CTkProgressBar(cat_card, progress_color=c_color, fg_color="#f1f5f9", height=8, corner_radius=4)
            pb.pack(fill="x", padx=16, pady=(0, 6))
            pb.set(c_pct)

        # Right: Top 5 Best Selling Products
        top_card = customtkinter.CTkFrame(split_row, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        top_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        customtkinter.CTkLabel(top_card, text="Top Selling Products", font=customtkinter.CTkFont(size=14, weight="bold"), text_color="#09090b").pack(anchor="w", padx=16, pady=(14, 10))

        top_products = [
            ("#1", "Classic Basta Smash Burger", "142 sold", "₱26,838", "#10b981"),
            ("#2", "Truffle Mushroom Cheeseburger", "86 sold", "₱21,414", "#3b82f6"),
            ("#3", "Crispy Golden Fries", "118 sold", "₱9,322", "#f59e0b"),
            ("#4", "Ube Shake Special", "74 sold", "₱8,880", "#8b5cf6"),
            ("#5", "Spicy BBQ Bacon Deluxe", "36 sold", "₱8,244", "#ef4444")
        ]
        for rank, p_name, q_sold, rev, r_col in top_products:
            p_row = customtkinter.CTkFrame(top_card, fg_color="transparent")
            p_row.pack(fill="x", padx=16, pady=5)

            rk_badge = customtkinter.CTkLabel(p_row, text=rank, font=customtkinter.CTkFont(size=11, weight="bold"), text_color=r_col, width=28)
            rk_badge.pack(side="left")

            name_box = customtkinter.CTkFrame(p_row, fg_color="transparent")
            name_box.pack(side="left", fill="x", expand=True, padx=6)
            customtkinter.CTkLabel(name_box, text=p_name, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").pack(anchor="w")
            customtkinter.CTkLabel(name_box, text=q_sold, font=customtkinter.CTkFont(size=10), text_color="#94a3b8").pack(anchor="w")

            customtkinter.CTkLabel(p_row, text=rev, font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#09090b").pack(side="right")

        # 5. Recent Sales Transactions Table
        tx_card = customtkinter.CTkFrame(main_scroll, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        tx_card.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 24))
        tx_card.grid_columnconfigure(0, weight=1)

        tx_head = customtkinter.CTkFrame(tx_card, fg_color="transparent")
        tx_head.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        tx_head.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(tx_head, text="Recent Transactions Audit Log", font=customtkinter.CTkFont(size=14, weight="bold"), text_color="#09090b").grid(row=0, column=0, sticky="w")
        customtkinter.CTkLabel(tx_head, text="Showing latest 5 orders", font=customtkinter.CTkFont(size=11), text_color="#64748b").grid(row=0, column=1, sticky="e")

        self.table_f = customtkinter.CTkFrame(tx_card, fg_color="transparent")
        self.table_f.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        for c in range(7):
            self.table_f.grid_columnconfigure(c, weight=1)
        self.table_f.grid_columnconfigure(3, weight=2)

        self.transactions_data = [
            ("TXN-0928-1048", "#B-1048", "Today 09:48 AM", "2x Smash, 1x Fries, 1x Ube Shake", "Cash", "Bea M.", "₱968.00"),
            ("TXN-0928-1047", "#B-1047", "Today 09:32 AM", "1x Truffle Burger, 1x Calamansi Fizz", "GCash", "Bea M.", "₱344.00"),
            ("TXN-0928-1046", "#B-1046", "Today 09:15 AM", "3x Bacon Deluxe, 2x Fries", "Card", "Marco S.", "₱845.00"),
            ("TXN-0928-1045", "#B-1045", "Today 08:50 AM", "1x Classic Smash, 1x Cold Brew", "Cash", "Bea M.", "₱284.00"),
            ("TXN-0928-1044", "#B-1044", "Today 08:30 AM", "4x Brioche Ice Cream Buns", "Maya", "Marco S.", "₱476.00")
        ]
        self.render_transactions_table()

    def render_transactions_table(self):
        for w in self.table_f.winfo_children():
            w.destroy()

        t_headers = ["TXN ID", "ORDER #", "TIME", "ITEMS", "PAYMENT", "CASHIER", "TOTAL"]
        for c_idx, h in enumerate(t_headers):
            customtkinter.CTkLabel(self.table_f, text=h, font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#64748b").grid(row=0, column=c_idx, sticky="w", padx=6, pady=8)

        for r_idx, (t_id, ord_id, t_time, itm, pay, cash, tot) in enumerate(self.transactions_data[:10], start=1):
            row_bg = "#f8fafc" if r_idx % 2 == 0 else "#ffffff"
            r_box = customtkinter.CTkFrame(self.table_f, fg_color=row_bg, corner_radius=6)
            r_box.grid(row=r_idx, column=0, columnspan=7, sticky="ew", pady=2)
            for c in range(7):
                r_box.grid_columnconfigure(c, weight=1)
            r_box.grid_columnconfigure(3, weight=2)

            customtkinter.CTkLabel(r_box, text=t_id, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").grid(row=0, column=0, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_box, text=ord_id, font=customtkinter.CTkFont(size=11), text_color="#475569").grid(row=0, column=1, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_box, text=t_time, font=customtkinter.CTkFont(size=10), text_color="#64748b").grid(row=0, column=2, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_box, text=itm, font=customtkinter.CTkFont(size=11), text_color="#1e293b").grid(row=0, column=3, sticky="w", padx=6, pady=8)

            pay_pill = customtkinter.CTkFrame(r_box, fg_color="#ecfdf5", corner_radius=6)
            pay_pill.grid(row=0, column=4, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(pay_pill, text=pay, font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#047857").pack(padx=8, pady=2)

            customtkinter.CTkLabel(r_box, text=cash, font=customtkinter.CTkFont(size=11), text_color="#475569").grid(row=0, column=5, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_box, text=tot, font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#09090b").grid(row=0, column=6, sticky="w", padx=6, pady=8)

    def add_completed_transaction(self, t_id, ord_id, t_time, itm, pay, cash, tot_val):
        """Adds a completed POS transaction to the live reports audit log and metric counters."""
        self.transactions_data.insert(0, (t_id, ord_id, t_time, itm, pay, cash, f"₱{tot_val:,.2f}"))
        self.render_transactions_table()

        # Update Daily metrics
        try:
            m_list = self.period_data["Daily"]["metrics"]
            # Increment Gross Sales
            curr_gross_str = m_list[0]["val"].replace("₱", "").replace(",", "")
            new_gross = float(curr_gross_str) + tot_val
            m_list[0]["val"] = f"₱{new_gross:,.2f}"

            # Increment Total Orders
            curr_ord_str = m_list[3]["val"].replace(" orders", "").replace(",", "")
            new_ord = int(curr_ord_str) + 1
            m_list[3]["val"] = f"{new_ord} orders"

            if self.active_period == "Daily":
                self.render_metric_cards()
        except Exception:
            pass

    def render_metric_cards(self):
        for w in self.metrics_container.winfo_children():
            w.destroy()

        metrics = self.period_data[self.active_period]["metrics"]
        for idx, m in enumerate(metrics):
            card = customtkinter.CTkFrame(self.metrics_container, fg_color="#09090b", corner_radius=14)
            card.grid(row=0, column=idx, padx=6, pady=4, sticky="nsew")

            c_head = customtkinter.CTkFrame(card, fg_color="transparent")
            c_head.grid(row=0, column=0, padx=16, pady=(14, 4), sticky="ew")
            c_head.grid_columnconfigure(0, weight=1)

            ico_cir = customtkinter.CTkButton(c_head, text=m["icon"], width=32, height=32, corner_radius=16, fg_color="#27272a", text_color="#ffffff", hover=False)
            ico_cir.grid(row=0, column=0, sticky="w")

            customtkinter.CTkLabel(c_head, text=m["title"], font=customtkinter.CTkFont(size=10), text_color="#94a3b8").grid(row=0, column=1, padx=8, sticky="w")

            customtkinter.CTkLabel(card, text=m["val"], font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#f8fafc").grid(row=1, column=0, padx=16, pady=(2, 2), sticky="w")
            customtkinter.CTkLabel(card, text=m["diff"], font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#4ade80").grid(row=2, column=0, padx=16, pady=(0, 14), sticky="w")

    def render_bar_chart(self):
        for w in self.bar_card.winfo_children():
            w.destroy()

        head = customtkinter.CTkFrame(self.bar_card, fg_color="transparent")
        head.grid(row=0, column=0, padx=16, pady=(14, 6), sticky="ew")
        head.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(head, text=f"Sales Overview ({self.active_period})", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="#09090b").grid(row=0, column=0, sticky="w")

        legend = customtkinter.CTkFrame(head, fg_color="transparent")
        legend.grid(row=0, column=1, sticky="e")
        customtkinter.CTkLabel(legend, text="● Gross Revenue", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#10b981").pack(side="left", padx=4)

        bars_container = customtkinter.CTkFrame(self.bar_card, fg_color="#f8fafc", corner_radius=10, height=160)
        bars_container.grid(row=1, column=0, padx=16, pady=(6, 14), sticky="nsew")
        bars_container.grid_propagate(False)

        bars = self.period_data[self.active_period]["bars"]
        max_val = self.period_data[self.active_period]["max_bar"]

        for b_idx, (b_label, b_val) in enumerate(bars):
            bars_container.grid_columnconfigure(b_idx, weight=1)

            col_box = customtkinter.CTkFrame(bars_container, fg_color="transparent")
            col_box.grid(row=0, column=b_idx, sticky="nsew", padx=6, pady=8)
            col_box.grid_rowconfigure(0, weight=1)
            col_box.grid_columnconfigure(0, weight=1)

            pct = min(1.0, max(0.1, b_val / max_val))
            bar_height = int(95 * pct)

            bar_frame = customtkinter.CTkFrame(col_box, width=28, height=bar_height, corner_radius=6, fg_color="#10b981")
            bar_frame.grid(row=0, column=0, sticky="s")
            bar_frame.grid_propagate(False)

            customtkinter.CTkLabel(col_box, text=b_label, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#64748b").grid(row=1, column=0, pady=(4, 0))

    def set_period(self, period_name):
        self.active_period = period_name
        for p, btn in self.period_buttons.items():
            is_act = (p == period_name)
            btn.configure(
                fg_color="#18181b" if is_act else "transparent",
                text_color="#ffffff" if is_act else "#475569",
                font=customtkinter.CTkFont(size=11, weight="bold" if is_act else "normal")
            )
        self.date_range_pill.configure(text=self.period_data[period_name]["date_label"])
        self.render_metric_cards()
        self.render_bar_chart()


class ReportsApp:
    """Wrapper that launches the unified application on the Reports tab."""

    def __new__(cls, *args, **kwargs):
        try:
            from ProjectMain.POS import BastaPOSApp
        except ImportError:
            from POS import BastaPOSApp
        return BastaPOSApp(initial_view="reports")


if __name__ == "__main__":
    app = ReportsApp()
    app.mainloop()
