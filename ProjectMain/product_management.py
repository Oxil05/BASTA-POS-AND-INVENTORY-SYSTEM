"""
BASTA BURGER - POS and Inventory Management System
Product Management Module
Faithfully recreates Designs/ADMIN_PRODUCTMANAGEMENT.png using CustomTkinter and Pillow.
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


class ProductManagementView(customtkinter.CTkFrame):
    """
    Product Management frame matching Designs/ADMIN_PRODUCTMANAGEMENT.png.
    Can be embedded directly into BastaPOSApp or displayed in any window.
    """

    def __init__(self, master, app_controller=None, **kwargs):
        super().__init__(master, fg_color="#f1f5f9", **kwargs)
        self.app_controller = app_controller

        # Load products from database or fallback to default dataset
        default_products = [
            {
                "id": 1, "sku": "BUR-001", "name": "Classic Basta Smash Burger", "category": "Burgers",
                "price": 189.00, "cost_price": 85.00, "stock": 32, "low_stock": 10,
                "in_store": True, "online": True, "grabfood": True, "status": "Active"
            },
            {
                "id": 2, "sku": "BUR-002", "name": "Truffle Mushroom Cheeseburger", "category": "Burgers",
                "price": 249.00, "cost_price": 110.00, "stock": 18, "low_stock": 8,
                "in_store": True, "online": True, "grabfood": False, "status": "Active"
            },
            {
                "id": 3, "sku": "BUR-003", "name": "Spicy BBQ Bacon Deluxe", "category": "Burgers",
                "price": 229.00, "cost_price": 95.00, "stock": 24, "low_stock": 10,
                "in_store": True, "online": True, "grabfood": True, "status": "Active"
            },
            {
                "id": 4, "sku": "DRK-001", "name": "Ube Shake Special", "category": "Beverages",
                "price": 120.00, "cost_price": 45.00, "stock": 45, "low_stock": 15,
                "in_store": True, "online": True, "grabfood": False, "status": "Active"
            },
            {
                "id": 5, "sku": "DRK-002", "name": "Calamansi Cold Brew Fizz", "category": "Beverages",
                "price": 95.00, "cost_price": 30.00, "stock": 50, "low_stock": 15,
                "in_store": True, "online": True, "grabfood": True, "status": "Active"
            },
            {
                "id": 6, "sku": "SDE-001", "name": "Crispy Golden Fries", "category": "Sides",
                "price": 79.00, "cost_price": 25.00, "stock": 60, "low_stock": 20,
                "in_store": True, "online": True, "grabfood": True, "status": "Active"
            },
            {
                "id": 7, "sku": "DES-001", "name": "Warm Brioche Ice Cream Bun", "category": "Desserts",
                "price": 119.00, "cost_price": 40.00, "stock": 8, "low_stock": 10,
                "in_store": True, "online": False, "grabfood": False, "status": "Active"
            }
        ]

        self.products_data = default_products
        try:
            from database import fetch_all_products
            db_prods = fetch_all_products()
            if db_prods:
                self.products_data = [
                    {
                        "id": p["id"],
                        "sku": p["sku"],
                        "name": p["name"],
                        "category": p["category"],
                        "price": float(p["price"]),
                        "cost_price": float(p.get("cost_price", 0.0) or 0.0),
                        "stock": int(p.get("stock_quantity", 0)),
                        "low_stock": int(p.get("low_stock_threshold", 10)),
                        "in_store": bool(p.get("in_store", 1)),
                        "online": bool(p.get("online_ordering", 1)),
                        "grabfood": bool(p.get("grabfood", 0)),
                        "status": p.get("status", "Active")
                    }
                    for p in db_prods
                ]
        except Exception:
            pass

        self.selected_product = self.products_data[0] if self.products_data else None
        self.is_creating_new = False

        # Grid configuration: Column 0 is main catalog, Column 1 is right drawer
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)  # Catalog table
        self.grid_columnconfigure(1, weight=2)  # Side editing drawer

        self._build_main_content()
        self._build_editor_drawer()

    def _build_main_content(self):
        self.main_scroll = customtkinter.CTkScrollableFrame(
            self,
            fg_color="#f8fafc",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.main_scroll.grid(row=0, column=0, sticky="nsew", padx=(18, 9), pady=18)
        self.main_scroll.grid_columnconfigure(0, weight=1)

        # 1. Header Bar
        header_bar = customtkinter.CTkFrame(self.main_scroll, fg_color="transparent")
        header_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 16))
        header_bar.grid_columnconfigure(0, weight=1)

        header_info = customtkinter.CTkFrame(header_bar, fg_color="transparent")
        header_info.grid(row=0, column=0, sticky="w")
        customtkinter.CTkLabel(
            header_info, text="Product Management", font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#09090b"
        ).pack(anchor="w")
        customtkinter.CTkLabel(
            header_info, text="Configure product catalog, adjust pricing, and track availability", font=customtkinter.CTkFont(size=12), text_color="#64748b"
        ).pack(anchor="w")

        add_btn = customtkinter.CTkButton(
            header_bar,
            text="+ Add Product",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=38,
            corner_radius=10,
            command=self.start_add_new_product
        )
        add_btn.grid(row=0, column=1, sticky="e")

        # 2. Key Metrics Row
        metrics_frame = customtkinter.CTkFrame(self.main_scroll, fg_color="transparent")
        metrics_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        for col_idx in range(3):
            metrics_frame.grid_columnconfigure(col_idx, weight=1)

        metrics = [
            ("TOTAL ACTIVE PRODUCTS", "32 items", "+3 added this month", "#10b981"),
            ("LOW STOCK ALERT", "4 items", "Order re-stock required", "#ef4444"),
            ("OUT OF STOCK", "1 item", "Temporarily paused", "#94a3b8")
        ]
        for idx, (m_title, m_val, m_sub, m_sub_color) in enumerate(metrics):
            m_card = customtkinter.CTkFrame(metrics_frame, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
            m_card.grid(row=0, column=idx, padx=6, pady=4, sticky="nsew")
            customtkinter.CTkLabel(m_card, text=m_title, font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#64748b").pack(anchor="w", padx=16, pady=(12, 2))
            customtkinter.CTkLabel(m_card, text=m_val, font=customtkinter.CTkFont(size=22, weight="bold"), text_color="#09090b").pack(anchor="w", padx=16, pady=2)
            customtkinter.CTkLabel(m_card, text=m_sub, font=customtkinter.CTkFont(size=11, weight="bold"), text_color=m_sub_color).pack(anchor="w", padx=16, pady=(0, 12))

        # 3. Product Catalog Table
        catalog_card = customtkinter.CTkFrame(self.main_scroll, fg_color="#ffffff", corner_radius=14, border_width=1, border_color="#e2e8f0")
        catalog_card.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 24))
        catalog_card.grid_columnconfigure(0, weight=1)

        filter_bar = customtkinter.CTkFrame(catalog_card, fg_color="transparent")
        filter_bar.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        filter_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = customtkinter.CTkEntry(
            filter_bar, placeholder_text="🔍 Search products by name, SKU or category...",
            height=36, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1"
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.table_container = customtkinter.CTkFrame(catalog_card, fg_color="transparent")
        self.table_container.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        self.table_container.grid_columnconfigure(0, weight=3)
        for c in range(1, 6):
            self.table_container.grid_columnconfigure(c, weight=1)

        self.render_product_list()

    def _build_editor_drawer(self):
        self.editor_panel = customtkinter.CTkScrollableFrame(
            self,
            fg_color="#ffffff",
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.editor_panel.grid(row=0, column=1, sticky="nsew", padx=(9, 18), pady=18)
        self.editor_panel.grid_columnconfigure(0, weight=1)

        # Drawer Title
        title_box = customtkinter.CTkFrame(self.editor_panel, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=16, pady=(16, 12), sticky="ew")
        title_box.grid_columnconfigure(0, weight=1)

        self.editor_title_lbl = customtkinter.CTkLabel(
            title_box, text="PRODUCT DETAILS", font=customtkinter.CTkFont(size=13, weight="bold"), text_color="#09090b"
        )
        self.editor_title_lbl.grid(row=0, column=0, sticky="w")

        # Product Image Preview / Upload Box
        img_box = customtkinter.CTkFrame(self.editor_panel, fg_color="#f8fafc", corner_radius=12, border_width=1, border_color="#e2e8f0", height=130)
        img_box.grid(row=1, column=0, padx=16, pady=(0, 14), sticky="ew")
        img_box.grid_propagate(False)
        img_box.grid_columnconfigure(0, weight=1)

        logo_img = get_logo_image(size=(70, 70))
        if logo_img:
            customtkinter.CTkLabel(img_box, image=logo_img, text="").pack(pady=(12, 4))
        else:
            customtkinter.CTkLabel(img_box, text="🍔", font=customtkinter.CTkFont(size=32)).pack(pady=(12, 4))
        customtkinter.CTkLabel(img_box, text="Product Photo Preview", font=customtkinter.CTkFont(size=11), text_color="#64748b").pack()

        # Product Name
        customtkinter.CTkLabel(self.editor_panel, text="PRODUCT NAME", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=2, column=0, padx=16, sticky="w")
        self.name_entry = customtkinter.CTkEntry(self.editor_panel, height=38, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1")
        self.name_entry.grid(row=3, column=0, padx=16, pady=(4, 10), sticky="ew")

        # SKU & Category Row
        meta_row = customtkinter.CTkFrame(self.editor_panel, fg_color="transparent")
        meta_row.grid(row=4, column=0, padx=16, pady=(0, 10), sticky="ew")
        meta_row.grid_columnconfigure(0, weight=1)
        meta_row.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(meta_row, text="SKU", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=0, column=0, sticky="w")
        self.sku_entry = customtkinter.CTkEntry(meta_row, height=38, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1")
        self.sku_entry.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(4, 0))

        customtkinter.CTkLabel(meta_row, text="CATEGORY", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=0, column=1, sticky="w")
        self.category_combo = customtkinter.CTkComboBox(meta_row, values=["Burgers", "Beverages", "Sides", "Desserts", "Meals"], height=38, corner_radius=10)
        self.category_combo.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(4, 0))

        # Price & Cost Price
        pricing_frame = customtkinter.CTkFrame(self.editor_panel, fg_color="transparent")
        pricing_frame.grid(row=5, column=0, padx=16, pady=(0, 10), sticky="ew")
        pricing_frame.grid_columnconfigure(0, weight=1)
        pricing_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(pricing_frame, text="PRICE (₱)", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=0, column=0, sticky="w")
        self.price_entry = customtkinter.CTkEntry(pricing_frame, height=38, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1")
        self.price_entry.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(4, 0))

        customtkinter.CTkLabel(pricing_frame, text="COST PRICE (₱)", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=0, column=1, sticky="w")
        self.cost_entry = customtkinter.CTkEntry(pricing_frame, height=38, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1")
        self.cost_entry.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(4, 0))

        # Stock & Low Stock
        stock_frame = customtkinter.CTkFrame(self.editor_panel, fg_color="transparent")
        stock_frame.grid(row=6, column=0, padx=16, pady=(0, 12), sticky="ew")
        stock_frame.grid_columnconfigure(0, weight=1)
        stock_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(stock_frame, text="STOCK ON HAND", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=0, column=0, sticky="w")
        self.stock_entry = customtkinter.CTkEntry(stock_frame, height=38, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1")
        self.stock_entry.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(4, 0))

        customtkinter.CTkLabel(stock_frame, text="LOW STOCK AT", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=0, column=1, sticky="w")
        self.low_stock_entry = customtkinter.CTkEntry(stock_frame, height=38, corner_radius=10, fg_color="#f8fafc", border_color="#cbd5e1")
        self.low_stock_entry.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(4, 0))

        # Availability Switches
        customtkinter.CTkLabel(self.editor_panel, text="AVAILABILITY", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#334155").grid(row=7, column=0, padx=16, sticky="w")

        switches_frame = customtkinter.CTkFrame(self.editor_panel, fg_color="transparent")
        switches_frame.grid(row=8, column=0, padx=16, pady=(4, 12), sticky="ew")
        switches_frame.grid_columnconfigure(0, weight=1)

        self.in_store_switch = customtkinter.CTkSwitch(switches_frame, text="In-store POS", progress_color="#10b981")
        self.in_store_switch.grid(row=0, column=0, sticky="ew", pady=3)
        self.in_store_switch.select()

        self.online_switch = customtkinter.CTkSwitch(switches_frame, text="Online ordering", progress_color="#10b981")
        self.online_switch.grid(row=1, column=0, sticky="ew", pady=3)
        self.online_switch.select()

        self.grabfood_switch = customtkinter.CTkSwitch(switches_frame, text="GrabFood", progress_color="#10b981")
        self.grabfood_switch.grid(row=2, column=0, sticky="ew", pady=3)

        # Action Buttons: Delete & Save
        actions_drawer = customtkinter.CTkFrame(self.editor_panel, fg_color="transparent")
        actions_drawer.grid(row=9, column=0, padx=16, pady=(10, 16), sticky="ew")
        actions_drawer.grid_columnconfigure(0, weight=1)
        actions_drawer.grid_columnconfigure(1, weight=2)

        self.delete_btn = customtkinter.CTkButton(
            actions_drawer, text="🗑 Delete", height=42, corner_radius=10, font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="#ffffff", text_color="#ef4444", border_width=1, border_color="#fca5a5", hover_color="#fee2e2",
            command=self.delete_current_product
        )
        self.delete_btn.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.save_btn = customtkinter.CTkButton(
            actions_drawer, text="✓ Save changes", height=42, corner_radius=10, font=customtkinter.CTkFont(size=13, weight="bold"),
            fg_color="#10b981", text_color="#ffffff", hover_color="#059669",
            command=self.save_current_product
        )
        self.save_btn.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.populate_drawer(self.selected_product)

    def render_product_list(self, query=""):
        for w in self.table_container.winfo_children():
            w.destroy()

        headers = ["PRODUCT NAME", "CATEGORY", "STOCK", "PRICE", "AVAILABILITY", "ACTION"]
        for c_idx, h in enumerate(headers):
            customtkinter.CTkLabel(
                self.table_container, text=h, font=customtkinter.CTkFont(size=10, weight="bold"), text_color="#64748b"
            ).grid(row=0, column=c_idx, sticky="w", padx=6, pady=8)

        filtered = [p for p in self.products_data if query.lower() in p["name"].lower() or query.lower() in p["sku"].lower() or query.lower() in p["category"].lower()]

        for r_idx, prod in enumerate(filtered, start=1):
            is_sel = (self.selected_product and self.selected_product["id"] == prod["id"])
            row_bg = "#ecfdf5" if is_sel else ("#f8fafc" if r_idx % 2 == 0 else "#ffffff")

            r_frame = customtkinter.CTkFrame(self.table_container, fg_color=row_bg, corner_radius=6)
            r_frame.grid(row=r_idx, column=0, columnspan=6, sticky="ew", pady=2)
            r_frame.grid_columnconfigure(0, weight=3)
            for c in range(1, 6):
                r_frame.grid_columnconfigure(c, weight=1)

            # Name & SKU
            name_box = customtkinter.CTkFrame(r_frame, fg_color="transparent")
            name_box.grid(row=0, column=0, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(name_box, text=prod["name"], font=customtkinter.CTkFont(size=12, weight="bold"), text_color="#0f172a").pack(anchor="w")
            customtkinter.CTkLabel(name_box, text=f"SKU: {prod['sku']}", font=customtkinter.CTkFont(size=10), text_color="#94a3b8").pack(anchor="w")

            # Category pill
            cat_pill = customtkinter.CTkFrame(r_frame, fg_color="#e2e8f0", corner_radius=6)
            cat_pill.grid(row=0, column=1, sticky="w", padx=6, pady=8)
            customtkinter.CTkLabel(cat_pill, text=prod["category"], font=customtkinter.CTkFont(size=10), text_color="#334155").pack(padx=6, pady=2)

            # Stock count
            customtkinter.CTkLabel(r_frame, text=f"{prod['stock']} units", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").grid(row=0, column=2, sticky="w", padx=6, pady=8)

            # Price
            customtkinter.CTkLabel(r_frame, text=f"₱{prod['price']:,.2f}", font=customtkinter.CTkFont(size=11, weight="bold"), text_color="#0f172a").grid(row=0, column=3, sticky="w", padx=6, pady=8)

            # Availability channels
            avail_txt = "POS" if prod["in_store"] else ""
            if prod["online"]:
                avail_txt += " · Online" if avail_txt else "Online"
            if prod["grabfood"]:
                avail_txt += " · Grab" if avail_txt else "Grab"
            customtkinter.CTkLabel(r_frame, text=avail_txt or "Inactive", font=customtkinter.CTkFont(size=10), text_color="#64748b").grid(row=0, column=4, sticky="w", padx=6, pady=8)

            # Edit Button
            edit_btn = customtkinter.CTkButton(
                r_frame, text="✏ Edit", font=customtkinter.CTkFont(size=10, weight="bold"),
                fg_color="#f1f5f9" if not is_sel else "#10b981",
                text_color="#0f172a" if not is_sel else "#ffffff",
                hover_color="#e2e8f0", width=60, height=28, corner_radius=6,
                command=lambda p=prod: self.select_product(p)
            )
            edit_btn.grid(row=0, column=5, sticky="w", padx=6, pady=8)

    def select_product(self, prod):
        self.selected_product = prod
        self.is_creating_new = False
        self.populate_drawer(prod)
        self.render_product_list(query=self.search_entry.get().strip())

    def start_add_new_product(self):
        self.selected_product = None
        self.is_creating_new = True
        self.editor_title_lbl.configure(text="+ ADD NEW PRODUCT")
        self.name_entry.delete(0, "end")
        self.sku_entry.delete(0, "end")
        self.sku_entry.insert(0, f"BUR-00{len(self.products_data) + 1}")
        self.category_combo.set("Burgers")
        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, "199.00")
        self.cost_entry.delete(0, "end")
        self.cost_entry.insert(0, "80.00")
        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, "20")
        self.low_stock_entry.delete(0, "end")
        self.low_stock_entry.insert(0, "10")
        self.in_store_switch.select()
        self.online_switch.select()
        self.grabfood_switch.deselect()
        self.render_product_list(query=self.search_entry.get().strip())

    def populate_drawer(self, prod):
        if not prod:
            return
        self.editor_title_lbl.configure(text=f"EDIT: {prod['sku']}")
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, prod["name"])
        self.sku_entry.delete(0, "end")
        self.sku_entry.insert(0, prod["sku"])
        self.category_combo.set(prod["category"])
        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, str(prod["price"]))
        self.cost_entry.delete(0, "end")
        self.cost_entry.insert(0, str(prod["cost_price"]))
        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, str(prod["stock"]))
        self.low_stock_entry.delete(0, "end")
        self.low_stock_entry.insert(0, str(prod["low_stock"]))

        if prod["in_store"]:
            self.in_store_switch.select()
        else:
            self.in_store_switch.deselect()

        if prod["online"]:
            self.online_switch.select()
        else:
            self.online_switch.deselect()

        if prod["grabfood"]:
            self.grabfood_switch.select()
        else:
            self.grabfood_switch.deselect()

    def save_current_product(self):
        try:
            p_price = float(self.price_entry.get().strip())
        except ValueError:
            p_price = 0.0
        try:
            p_cost = float(self.cost_entry.get().strip())
        except ValueError:
            p_cost = 0.0
        try:
            p_stock = int(self.stock_entry.get().strip())
        except ValueError:
            p_stock = 0
        try:
            p_low = int(self.low_stock_entry.get().strip())
        except ValueError:
            p_low = 5

        p_name = self.name_entry.get().strip() or "Untitled Product"
        p_sku = self.sku_entry.get().strip() or "BUR-NEW"
        p_cat = self.category_combo.get()

        if self.is_creating_new or not self.selected_product:
            new_id = len(self.products_data) + 1
            try:
                from database import add_product
                db_id = add_product(
                    p_name, p_sku, p_cat, p_price, p_cost, p_stock, p_low,
                    bool(self.in_store_switch.get()), bool(self.online_switch.get()), bool(self.grabfood_switch.get())
                )
                if db_id:
                    new_id = db_id
            except Exception as e:
                print(f"[BASTA DB] Product add notice: {e}")

            new_prod = {
                "id": new_id,
                "sku": p_sku, "name": p_name, "category": p_cat,
                "price": p_price, "cost_price": p_cost, "stock": p_stock, "low_stock": p_low,
                "in_store": bool(self.in_store_switch.get()),
                "online": bool(self.online_switch.get()),
                "grabfood": bool(self.grabfood_switch.get()),
                "status": "Active"
            }
            self.products_data.append(new_prod)
            self.selected_product = new_prod
            self.is_creating_new = False
        else:
            try:
                from database import update_product
                update_product(
                    self.selected_product["id"], p_name, p_sku, p_cat, p_price, p_cost, p_stock, p_low,
                    bool(self.in_store_switch.get()), bool(self.online_switch.get()), bool(self.grabfood_switch.get())
                )
            except Exception as e:
                print(f"[BASTA DB] Product update notice: {e}")

            self.selected_product.update({
                "name": p_name, "sku": p_sku, "category": p_cat,
                "price": p_price, "cost_price": p_cost, "stock": p_stock, "low_stock": p_low,
                "in_store": bool(self.in_store_switch.get()),
                "online": bool(self.online_switch.get()),
                "grabfood": bool(self.grabfood_switch.get())
            })

        self.populate_drawer(self.selected_product)
        self.render_product_list(query=self.search_entry.get().strip())

        # Notify main controller (POS) to synchronize immediately
        if self.app_controller and hasattr(self.app_controller, "sync_products_from_management"):
            self.app_controller.sync_products_from_management()

    def delete_current_product(self):
        if self.selected_product and self.selected_product in self.products_data:
            try:
                from database import delete_product
                delete_product(self.selected_product["id"])
            except Exception as e:
                print(f"[BASTA DB] Product delete notice: {e}")

            self.products_data.remove(self.selected_product)
            self.selected_product = self.products_data[0] if self.products_data else None
            self.populate_drawer(self.selected_product)
            self.render_product_list(query=self.search_entry.get().strip())

            # Notify main controller (POS) to synchronize immediately
            if self.app_controller and hasattr(self.app_controller, "sync_products_from_management"):
                self.app_controller.sync_products_from_management()

    def on_search(self, event=None):
        self.render_product_list(query=self.search_entry.get().strip())


class ProductManagementApp:
    """Wrapper that launches the unified application on the Products tab."""

    def __new__(cls, *args, **kwargs):
        try:
            from ProjectMain.POS import BastaPOSApp
        except ImportError:
            from POS import BastaPOSApp
        return BastaPOSApp(initial_view="products")


if __name__ == "__main__":
    app = ProductManagementApp()
    app.mainloop()
