"""
BASTA BURGER - POS and Inventory Management System
Inventory Overview Module
Faithfully recreates Designs/ADMIN_INVENTORY.png using CustomTkinter and Pillow.
All variables and functions strictly use snake_case.
"""

import os
import sys
import csv
from datetime import datetime
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


class InventoryOverviewView(customtkinter.CTkFrame):
    """
    Inventory Overview frame matching Designs/ADMIN_INVENTORY.png.
    Can be embedded directly into BastaPOSApp or displayed in any window.
    """

    def __init__(self, master, app_controller=None, **kwargs):
        super().__init__(master, fg_color="#f1f5f9", **kwargs)
        self.app_controller = app_controller

        # Inventory Items State
        self.inventory_items = [
            {"sku": "ING-0018", "name": "USDA ground beef 80/20", "category": "Proteins", "on_hand": "18.5 kg", "par": "14 kg", "unit_cost": "₱410 / kg", "status": "Healthy"},
            {"sku": "ING-0031", "name": "Brioche burger buns", "category": "Bakery", "on_hand": "4 packs", "par": "12 packs", "unit_cost": "₱185 / pack", "status": "Critical"},
            {"sku": "ING-0064", "name": "Frozen ube ice cream", "category": "Desserts", "on_hand": "2.4 L", "par": "6 L", "unit_cost": "₱320 / L", "status": "Low stock"},
            {"sku": "ING-0085", "name": "Russet potatoes", "category": "Produce", "on_hand": "31 kg", "par": "20 kg", "unit_cost": "₱86 / kg", "status": "Healthy"},
            {"sku": "ING-0102", "name": "Calamansi glaze", "category": "Sauces", "on_hand": "3 bottles", "par": "8 bottles", "unit_cost": "₱145 / bottle", "status": "Low stock"}
        ]

        # Layout configuration
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

        # 1. Top Header Bar
        top_bar = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 16))
        top_bar.grid_columnconfigure(0, weight=1)

        header_info = customtkinter.CTkFrame(top_bar, fg_color="transparent")
        header_info.grid(row=0, column=0, sticky="w")
        customtkinter.CTkLabel(
            header_info,
            text="Inventory Overview",
            font=customtkinter.CTkFont(size=22, weight="bold"),
            text_color="#09090b"
        ).pack(anchor="w")
        customtkinter.CTkLabel(
            header_info,
            text="Real-time ingredient levels, stock health, and reorder tracking",
            font=customtkinter.CTkFont(size=12),
            text_color="#64748b"
        ).pack(anchor="w")

        top_actions = customtkinter.CTkFrame(top_bar, fg_color="transparent")
        top_actions.grid(row=0, column=1, sticky="e")

        receive_stock_btn = customtkinter.CTkButton(
            top_actions,
            text="+ Receive Stock",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=38,
            corner_radius=10,
            command=self.show_receive_stock_dialog
        )
        receive_stock_btn.pack(side="left", padx=6)

        self.print_btn = customtkinter.CTkButton(
            top_actions,
            text="⎙ Print Report",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=38,
            corner_radius=10,
            command=self.handle_print_report
        )
        self.print_btn.pack(side="left", padx=6)

        self.export_btn = customtkinter.CTkButton(
            top_actions,
            text="⤓ Export CSV",
            font=customtkinter.CTkFont(size=12),
            fg_color="#ffffff",
            text_color="#0f172a",
            hover_color="#f1f5f9",
            border_width=1,
            border_color="#cbd5e1",
            height=38,
            corner_radius=10,
            command=self.handle_export_csv
        )
        self.export_btn.pack(side="left", padx=6)

        # 2. Key Metrics Row (4 Cards - Dynamically calculated)
        self.metrics_frame = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        self.metrics_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        for col_idx in range(4):
            self.metrics_frame.grid_columnconfigure(col_idx, weight=1)

        # 3. Critical Low Stock Alert Banner
        self.alert_box = customtkinter.CTkFrame(main_scroll, fg_color="#fef2f2", corner_radius=14, border_width=1, border_color="#fecaca")
        self.alert_box.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        self.alert_box.grid_columnconfigure(0, weight=1)

        self.render_metrics_and_alerts()

        # 4. Two Split Cards: Category Value Breakdown + Stock Movements
        split_row = customtkinter.CTkFrame(main_scroll, fg_color="transparent")
        split_row.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
        split_row.grid_columnconfigure(0, weight=1)
        split_row.grid_columnconfigure(1, weight=1)

        # Left: Inventory Value by Category
        cat_card = customtkinter.CTkFrame(split_row, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        cat_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        customtkinter.CTkLabel(cat_card, text="Inventory Value by Category", font=customtkinter.CTkFont(size=14, weight="bold"), text_color="#09090b").pack(anchor="w", padx=16, pady=(14, 10))

        cats = [
            ("Proteins (Beef, Chicken, Bacon)", 0.45, "₱66,712 (45%)", "#10b981"),
            ("Bakery (Brioche Buns, Rolls)", 0.22, "₱32,615 (22%)", "#3b82f6"),
            ("Produce & Dairy (Potatoes, Cheese)", 0.18, "₱26,685 (18%)", "#f59e0b"),
            ("Sauces & Condiments", 0.15, "₱22,238 (15%)", "#8b5cf6")
        ]
        for c_name, c_pct, c_val, c_col in cats:
            row_f = customtkinter.CTkFrame(cat_card, fg_color="transparent")
            row_f.pack(fill="x", padx=16, pady=4)
            customtkinter.CTkLabel(row_f, text=c_name, font=customtkinter.CTkFont(size=11), text_color="#475569").pack(side="left")
            customtkinter.CTkLabel(row_f, text=c_val, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").pack(side="right")

            pb = customtkinter.CTkProgressBar(cat_card, progress_color=c_col, fg_color="#f1f5f9", height=8, corner_radius=4)
            pb.pack(fill="x", padx=16, pady=(0, 6))
            pb.set(c_pct)

        # Right: Recent Stock Movements
        mov_card = customtkinter.CTkFrame(split_row, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        mov_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        customtkinter.CTkLabel(mov_card, text="Recent Stock Movements", font=customtkinter.CTkFont(size=14, weight="bold"), text_color="#09090b").pack(anchor="w", padx=16, pady=(14, 10))

        movements = [
            ("+ 15.0 kg", "USDA Ground Beef restocked", "Today, 08:30 AM", "#10b981", "#ecfdf5"),
            ("- 4 packs", "Brioche buns consumed (POS)", "Today, 11:45 AM", "#ef4444", "#fef2f2"),
            ("+ 10 bottles", "Calamansi glaze received", "Yesterday, 04:15 PM", "#10b981", "#ecfdf5"),
            ("- 6.5 kg", "Russet potatoes used", "Yesterday, 02:20 PM", "#ef4444", "#fef2f2")
        ]
        for delta, desc, time_str, tcolor, bg_pill in movements:
            m_row = customtkinter.CTkFrame(mov_card, fg_color="transparent")
            m_row.pack(fill="x", padx=16, pady=5)

            pill = customtkinter.CTkFrame(m_row, fg_color=bg_pill, corner_radius=6, height=24)
            pill.pack(side="left", padx=(0, 10))
            customtkinter.CTkLabel(pill, text=delta, font=customtkinter.CTkFont(size=11, weight="bold"), text_color=tcolor).pack(padx=8, pady=2)

            info = customtkinter.CTkFrame(m_row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)
            customtkinter.CTkLabel(info, text=desc, font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#1e293b").pack(anchor="w")
            customtkinter.CTkLabel(info, text=time_str, font=customtkinter.CTkFont(size=10), text_color="#94a3b8").pack(anchor="w")

        # 5. Inventory Items Table Card
        table_card = customtkinter.CTkFrame(main_scroll, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        table_card.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 24))
        table_card.grid_columnconfigure(0, weight=1)

        # Filter Sub-bar
        filter_bar = customtkinter.CTkFrame(table_card, fg_color="transparent")
        filter_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        filter_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = customtkinter.CTkEntry(
            filter_bar,
            placeholder_text="🔍 Search ingredient name or SKU...",
            height=36,
            corner_radius=10,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            width=280
        )
        self.search_entry.grid(row=0, column=0, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.cat_filter = customtkinter.CTkComboBox(
            filter_bar,
            values=["All Categories", "Proteins", "Bakery", "Desserts", "Produce", "Sauces"],
            height=36,
            corner_radius=10,
            command=self.on_filter_category,
            width=160
        )
        self.cat_filter.grid(row=0, column=1, padx=8, sticky="e")

        # Table Rows Container
        self.table_container = customtkinter.CTkFrame(table_card, fg_color="transparent")
        self.table_container.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        self.table_container.grid_columnconfigure(1, weight=2)
        for c in [0, 2, 3, 4, 5, 6, 7]:
            self.table_container.grid_columnconfigure(c, weight=1)

        self.render_inventory_table()

    def render_metrics_and_alerts(self):
        """Dynamically renders metric cards and alert banner from live inventory items state."""
        if not hasattr(self, "metrics_frame") or not hasattr(self, "alert_box"):
            return

        for w in self.metrics_frame.winfo_children():
            w.destroy()

        low_alerts = [i for i in self.inventory_items if i.get("status") in ["Critical", "Low stock"]]
        low_count = len(low_alerts)

        metrics_data = [
            {"title": "TOTAL INVENTORY VALUE", "val": "₱148,250", "sub": "+2.4% vs last week", "sub_color": "#10b981", "badge": "📦"},
            {"title": "LOW STOCK ALERTS", "val": f"{low_count} items", "sub": "Requires attention" if low_count > 0 else "All par levels healthy", "sub_color": "#ef4444" if low_count > 0 else "#10b981", "badge": "⚠"},
            {"title": "MONTHLY TURNOVER", "val": "4.2x", "sub": "Optimal velocity", "sub_color": "#10b981", "badge": "🔄"},
            {"title": "WASTE & SPOILAGE", "val": "1.2%", "sub": "-0.4% this month", "sub_color": "#10b981", "badge": "📉"}
        ]

        for idx, m in enumerate(metrics_data):
            card = customtkinter.CTkFrame(self.metrics_frame, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
            card.grid(row=0, column=idx, padx=6, pady=4, sticky="nsew")

            card_top = customtkinter.CTkFrame(card, fg_color="transparent")
            card_top.pack(fill="x", padx=16, pady=(14, 4))
            customtkinter.CTkLabel(card_top, text=m["title"], font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#64748b").pack(side="left")
            customtkinter.CTkLabel(card_top, text=m["badge"], font=customtkinter.CTkFont(size=14)).pack(side="right")

            customtkinter.CTkLabel(card, text=m["val"], font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#09090b").pack(anchor="w", padx=16, pady=2)
            customtkinter.CTkLabel(card, text=m["sub"], font=customtkinter.CTkFont(size=11, weight="bold"), text_color=m["sub_color"]).pack(anchor="w", padx=16, pady=(0, 14))

        # Alert Box
        for w in self.alert_box.winfo_children():
            w.destroy()

        if low_count > 0:
            self.alert_box.configure(fg_color="#fef2f2", border_color="#fecaca")
            alert_inner = customtkinter.CTkFrame(self.alert_box, fg_color="transparent")
            alert_inner.grid(row=0, column=0, padx=16, pady=12, sticky="ew")
            alert_inner.grid_columnconfigure(1, weight=1)

            customtkinter.CTkLabel(alert_inner, text="🚨", font=customtkinter.CTkFont(size=18)).grid(row=0, column=0, padx=(0, 10))
            alert_text = customtkinter.CTkFrame(alert_inner, fg_color="transparent")
            alert_text.grid(row=0, column=1, sticky="w")
            customtkinter.CTkLabel(
                alert_text,
                text=f"{low_count} critical ingredient{'s' if low_count != 1 else ''} reached reorder par level",
                font=customtkinter.CTkFont(size=13, weight="bold"),
                text_color="#991b1b"
            ).pack(anchor="w")
            names_str = ", ".join(i["name"] for i in low_alerts[:3])
            customtkinter.CTkLabel(
                alert_text,
                text=f"{names_str} below minimum safety thresholds.",
                font=customtkinter.CTkFont(size=11),
                text_color="#b91c1c"
            ).pack(anchor="w")

            reorder_btn = customtkinter.CTkButton(
                alert_inner,
                text="Reorder Now",
                font=customtkinter.CTkFont(size=11, weight="bold"),
                fg_color="#ef4444",
                hover_color="#dc2626",
                height=32,
                corner_radius=8,
                command=self.show_receive_stock_dialog
            )
            reorder_btn.grid(row=0, column=2, padx=(10, 0))
        else:
            self.alert_box.configure(fg_color="#f0fdf4", border_color="#bbf7d0")
            alert_inner = customtkinter.CTkFrame(self.alert_box, fg_color="transparent")
            alert_inner.grid(row=0, column=0, padx=16, pady=12, sticky="ew")
            alert_inner.grid_columnconfigure(1, weight=1)

            customtkinter.CTkLabel(alert_inner, text="✓", font=customtkinter.CTkFont(size=18, weight="bold"), text_color="#16a34a").grid(row=0, column=0, padx=(0, 10))
            alert_text = customtkinter.CTkFrame(alert_inner, fg_color="transparent")
            alert_text.grid(row=0, column=1, sticky="w")
            customtkinter.CTkLabel(
                alert_text,
                text="All ingredient stock levels are healthy",
                font=customtkinter.CTkFont(size=13, weight="bold"),
                text_color="#166534"
            ).pack(anchor="w")
            customtkinter.CTkLabel(
                alert_text,
                text="No ingredients currently below par level safety thresholds.",
                font=customtkinter.CTkFont(size=11),
                text_color="#15803d"
            ).pack(anchor="w")

    def render_inventory_table(self, query="", category="All Categories"):
        for w in self.table_container.winfo_children():
            w.destroy()

        # Header Row
        headers = ["SKU", "ITEM NAME", "CATEGORY", "ON HAND", "PAR LEVEL", "UNIT COST", "STATUS", "ACTIONS"]
        for col_idx, h in enumerate(headers):
            customtkinter.CTkLabel(
                self.table_container,
                text=h,
                font=customtkinter.CTkFont(size=10, weight="bold"),
                text_color="#64748b"
            ).grid(row=0, column=col_idx, sticky="w", padx=6, pady=8)

        # Filter items
        filtered = []
        for item in self.inventory_items:
            match_q = query.lower() in item["name"].lower() or query.lower() in item["sku"].lower()
            match_c = (category == "All Categories") or (item["category"] == category)
            if match_q and match_c:
                filtered.append(item)

        for row_idx, item in enumerate(filtered, start=1):
            row_bg = "#f8fafc" if row_idx % 2 == 0 else "#ffffff"
            r_frame = customtkinter.CTkFrame(self.table_container, fg_color=row_bg, corner_radius=6)
            r_frame.grid(row=row_idx, column=0, columnspan=8, sticky="ew", pady=2)
            r_frame.grid_columnconfigure(1, weight=2)
            for c in [0, 2, 3, 4, 5, 6, 7]:
                r_frame.grid_columnconfigure(c, weight=1)

            customtkinter.CTkLabel(r_frame, text=item["sku"], font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").grid(row=0, column=0, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_frame, text=item["name"], font=customtkinter.CTkFont(size=11), text_color="#1e293b").grid(row=0, column=1, sticky="w", padx=6, pady=8)

            # Category pill
            cat_pill = customtkinter.CTkFrame(r_frame, fg_color="#e2e8f0", corner_radius=6)
            cat_pill.grid(row=0, column=2, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(cat_pill, text=item["category"], font=customtkinter.CTkFont(size=10), text_color="#334155").pack(padx=6, pady=2)

            customtkinter.CTkLabel(r_frame, text=item["on_hand"], font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").grid(row=0, column=3, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_frame, text=item["par"], font=customtkinter.CTkFont(size=11), text_color="#64748b").grid(row=0, column=4, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(r_frame, text=item["unit_cost"], font=customtkinter.CTkFont(size=11), text_color="#0f172a").grid(row=0, column=5, sticky="w", padx=6, pady=8)

            # Status pill
            status = item["status"]
            if status == "Healthy":
                s_bg, s_fg = "#dcfce7", "#15803d"
            elif status == "Low stock":
                s_bg, s_fg = "#fef9c3", "#a16207"
            else:
                s_bg, s_fg = "#fee2e2", "#b91c1c"

            status_pill = customtkinter.CTkFrame(r_frame, fg_color=s_bg, corner_radius=6)
            status_pill.grid(row=0, column=6, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(status_pill, text=status, font=customtkinter.CTkFont(size=10, weight="bold"), text_color=s_fg).pack(padx=8, pady=2)

            # Action button
            adj_btn = customtkinter.CTkButton(
                r_frame,
                text="Adjust",
                font=customtkinter.CTkFont(size=10),
                fg_color="#f1f5f9",
                text_color="#0f172a",
                hover_color="#e2e8f0",
                width=60,
                height=26,
                corner_radius=6,
                command=lambda it=item: self.show_adjust_stock_dialog(it)
            )
            adj_btn.grid(row=0, column=7, sticky="w", padx=6, pady=8)

    def on_search(self, event=None):
        self.render_inventory_table(query=self.search_entry.get().strip(), category=self.cat_filter.get())

    def on_filter_category(self, cat):
        self.render_inventory_table(query=self.search_entry.get().strip(), category=cat)

    def show_receive_stock_dialog(self):
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Receive Stock")
        dialog.geometry("440x360")
        dialog.grab_set()

        customtkinter.CTkLabel(dialog, text="📦 Receive Stock Shipment", font=customtkinter.CTkFont(size=16, weight="bold")).pack(pady=(20, 14))

        customtkinter.CTkLabel(dialog, text="Select Item:", font=customtkinter.CTkFont(size=12)).pack(anchor="w", padx=30)
        item_names = [f"{i['sku']} - {i['name']}" for i in self.inventory_items]
        item_combo = customtkinter.CTkComboBox(dialog, values=item_names, width=380)
        item_combo.pack(padx=30, pady=(4, 12))

        customtkinter.CTkLabel(dialog, text="Quantity to Add:", font=customtkinter.CTkFont(size=12)).pack(anchor="w", padx=30)
        qty_entry = customtkinter.CTkEntry(dialog, placeholder_text="e.g. 10 kg, 5 packs", width=380)
        qty_entry.pack(padx=30, pady=(4, 18))

        def confirm_receive():
            selected_str = item_combo.get()
            added_qty = qty_entry.get().strip()
            if added_qty:
                for it in self.inventory_items:
                    if it["sku"] in selected_str:
                        it["on_hand"] = f"+{added_qty} (Updated)"
                        it["status"] = "Healthy"
                        break
            dialog.destroy()
            self.render_inventory_table()
            self.render_metrics_and_alerts()

        customtkinter.CTkButton(
            dialog,
            text="Confirm & Update Stock",
            fg_color="#10b981",
            hover_color="#059669",
            height=40,
            width=380,
            command=confirm_receive
        ).pack(padx=30, pady=(6, 0))

    def show_adjust_stock_dialog(self, item):
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Adjust Stock")
        dialog.geometry("420x300")
        dialog.grab_set()

        customtkinter.CTkLabel(dialog, text=f"Adjust: {item['name']}", font=customtkinter.CTkFont(size=14, weight="bold")).pack(pady=(20, 10))
        customtkinter.CTkLabel(dialog, text=f"Current Stock: {item['on_hand']}", font=customtkinter.CTkFont(size=12), text_color="#64748b").pack(pady=(0, 14))

        new_entry = customtkinter.CTkEntry(dialog, placeholder_text="Enter new quantity...", width=320)
        new_entry.pack(pady=10)

        def save_adjustment():
            val = new_entry.get().strip()
            if val:
                item["on_hand"] = val
            dialog.destroy()
            self.render_inventory_table()
            self.render_metrics_and_alerts()

        customtkinter.CTkButton(dialog, text="Save Adjustment", fg_color="#10b981", hover_color="#059669", height=38, width=320, command=save_adjustment).pack(pady=14)

    def handle_print_report(self):
        """Generates formatted inventory stock report text, sends to printer/Notepad, and notifies user."""
        now_str = datetime.now().strftime("%d %b %Y - %I:%M %p")
        lines = [
            "=" * 65,
            "                   BASTA BURGER - POS                   ",
            "             INVENTORY & STOCK STATUS REPORT            ",
            "=" * 65,
            f"Generated On: {now_str}",
            "-" * 65,
            "1. INVENTORY VALUATION & REORDER HEALTH",
            "-" * 65,
            f"  TOTAL INVENTORY VALUE : ₱148,250 (+2.4% vs last week)",
            f"  LOW STOCK ALERTS      : 3 critical items requiring attention",
            f"  MONTHLY TURNOVER      : 4.2x (Optimal velocity)",
            f"  WASTE & SPOILAGE      : 1.2% (-0.4% this month)",
            "-" * 65,
            "2. CURRENT INGREDIENT STOCK LEVELS",
            "-" * 65,
            f"{'SKU':<12}{'INGREDIENT NAME':<26}{'ON HAND':<12}{'PAR':<10}{'STATUS':<10}",
            "-" * 65,
        ]

        for item in self.inventory_items:
            sku = item.get("sku", "")
            name = item.get("name", "")
            on_hand = item.get("on_hand", "")
            par = item.get("par", "")
            status = item.get("status", "Healthy")
            lines.append(f"{sku:<12}{name[:24]:<26}{on_hand:<12}{par:<10}{status:<10}")

        lines.extend([
            "-" * 65,
            "3. CRITICAL STOCK REORDER ALERTS",
            "-" * 65,
            "  * Brioche burger buns (ING-0031) - 4 packs on hand (Par: 12 packs) [CRITICAL]",
            "  * Frozen ube ice cream (ING-0064) - 2.4 L on hand (Par: 6 L) [LOW STOCK]",
            "  * Calamansi glaze (ING-0102) - 3 bottles on hand (Par: 8 bottles) [LOW STOCK]",
            "=" * 65,
            "                END OF INVENTORY REPORT                  ",
            "=" * 65
        ])
        report_text = "\n".join(lines)

        reports_dir = os.path.join(project_root, "Reports")
        os.makedirs(reports_dir, exist_ok=True)
        safe_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(reports_dir, f"Stock_Report_{safe_time}.txt")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report_text)
        except Exception as err:
            print(f"[BASTA POS] Failed to save stock report: {err}")

        if hasattr(self, "print_btn"):
            self.print_btn.configure(text="✓ Printed!", fg_color="#059669")
            self.after(2000, lambda: self.print_btn.configure(text="⎙ Print Report", fg_color="#10b981"))

        if os.path.exists(file_path):
            try:
                os.startfile(file_path, "print")
            except Exception:
                try:
                    os.startfile(file_path)
                except Exception as open_err:
                    print(f"[BASTA POS] Could not open file: {open_err}")

        try:
            from tkinter import messagebox
            messagebox.showinfo(
                "Print Stock Report",
                f"Inventory Stock Report sent to printer!\n\nSaved to:\nReports/{os.path.basename(file_path)}"
            )
        except Exception:
            pass

    def handle_export_csv(self):
        """Exports the full inventory stock data to a CSV spreadsheet."""
        from tkinter import filedialog, messagebox

        default_filename = f"Inventory_Stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        initial_dir = os.path.join(project_root, "Exports")
        os.makedirs(initial_dir, exist_ok=True)

        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile=default_filename,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file)

                # Header
                writer.writerow(["BASTA BURGER - INVENTORY & STOCK OVERVIEW REPORT"])
                writer.writerow(["Export Timestamp", now_str])
                writer.writerow([])

                # KPI Metrics Summary
                writer.writerow(["--- INVENTORY KPI SUMMARY ---"])
                writer.writerow(["Metric", "Value", "Status / Trend"])
                writer.writerow(["Total Inventory Value", "₱148,250", "+2.4% vs last week"])
                writer.writerow(["Low Stock Alerts", "3 items", "Requires reorder"])
                writer.writerow(["Monthly Turnover", "4.2x", "Optimal velocity"])
                writer.writerow(["Waste & Spoilage", "1.2%", "-0.4% this month"])
                writer.writerow([])

                # Category Breakdown
                writer.writerow(["--- INVENTORY VALUE BY CATEGORY ---"])
                writer.writerow(["Category", "Share %", "Value"])
                writer.writerow(["Proteins (Beef, Chicken, Bacon)", "45%", "₱66,712"])
                writer.writerow(["Bakery (Brioche Buns, Rolls)", "22%", "₱32,615"])
                writer.writerow(["Produce & Dairy (Potatoes, Cheese)", "18%", "₱26,685"])
                writer.writerow(["Sauces & Condiments", "15%", "₱22,238"])
                writer.writerow([])

                # Detailed Items Table
                writer.writerow(["--- INVENTORY INGREDIENTS TABLE ---"])
                writer.writerow(["SKU", "Ingredient Name", "Category", "On Hand Quantity", "Par Level (Safety Threshold)", "Unit Cost", "Stock Health Status"])
                for it in self.inventory_items:
                    writer.writerow([
                        it.get("sku", ""),
                        it.get("name", ""),
                        it.get("category", ""),
                        it.get("on_hand", ""),
                        it.get("par", ""),
                        it.get("unit_cost", ""),
                        it.get("status", "")
                    ])

            if hasattr(self, "export_btn"):
                self.export_btn.configure(text="✓ Exported!", fg_color="#10b981", text_color="#ffffff")
                self.after(2000, lambda: self.export_btn.configure(text="⤓ Export CSV", fg_color="#ffffff", text_color="#0f172a"))

            res = messagebox.askyesno(
                "Export Successful",
                f"Inventory stock data successfully exported to:\n{file_path}\n\nWould you like to open the CSV file now?"
            )
            if res:
                try:
                    os.startfile(file_path)
                except Exception as open_err:
                    print(f"[BASTA POS] Could not open CSV file: {open_err}")

        except Exception as err:
            messagebox.showerror("Export Error", f"Failed to export CSV:\n{err}")


class InventoryOverviewApp:
    """Wrapper that launches the unified application on the Stock/Inventory tab."""

    def __new__(cls, *args, **kwargs):
        try:
            from ProjectMain.POS import BastaPOSApp
        except ImportError:
            from POS import BastaPOSApp
        return BastaPOSApp(initial_view="stock")


if __name__ == "__main__":
    app = InventoryOverviewApp()
    app.mainloop()
