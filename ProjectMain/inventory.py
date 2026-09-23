import customtkinter

# Set appearance mode and theme
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class BurgerInventoryApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("BASTA POS")
        self.geometry("900x600")
        self.minsize(700, 450)

        # Configure root grid weights for full window responsiveness
        # Row 1 (table) expands vertically to take all available space
        self.grid_rowconfigure(1, weight=1)
        # Column 0 expands horizontally across the entire window
        self.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_inventory_table()
        self._create_action_buttons()

    def _create_header(self):
        # Header banner frame
        header_frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#1e293b")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        # Title
        title_label = customtkinter.CTkLabel(
            header_frame,
            text="🍔 Burger Shop Inventory",
            font=customtkinter.CTkFont(size=22, weight="bold"),
            text_color="#f8fafc"
        )
        title_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        # Stat badge / subtitle
        stats_label = customtkinter.CTkLabel(
            header_frame,
            text="Total Items: 2 | Status: All In Stock",
            font=customtkinter.CTkFont(size=13),
            text_color="#94a3b8"
        )
        stats_label.grid(row=0, column=1, padx=15, pady=12, sticky="e")

    def _create_inventory_table(self):
        # Container frame for the inventory list
        table_container = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#0f172a")
        table_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        table_container.grid_rowconfigure(1, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Table Header
        header_row = customtkinter.CTkFrame(table_container, corner_radius=6, fg_color="#334155")
        header_row.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Configure column weights for responsive distribution
        header_row.grid_columnconfigure(0, weight=1)  # ID
        header_row.grid_columnconfigure(1, weight=3)  # Name
        header_row.grid_columnconfigure(2, weight=2)  # Category
        header_row.grid_columnconfigure(3, weight=2)  # Price
        header_row.grid_columnconfigure(4, weight=2)  # Stock
        header_row.grid_columnconfigure(5, weight=2)  # Status

        columns = ["Item ID", "Product Name", "Category", "Price", "Stock", "Status"]
        for col_idx, col_name in enumerate(columns):
            lbl = customtkinter.CTkLabel(
                header_row,
                text=col_name,
                font=customtkinter.CTkFont(size=14, weight="bold"),
                text_color="#e2e8f0"
            )
            if col_idx < 3:
                lbl.grid(row=0, column=col_idx, padx=10, pady=8, sticky="w")
            else:
                lbl.grid(row=0, column=col_idx, padx=10, pady=8)

        # Scrollable area for products
        product_scroll = customtkinter.CTkScrollableFrame(table_container, fg_color="transparent")
        product_scroll.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
        product_scroll.grid_columnconfigure(0, weight=1)

        # Mock Products Data (Burger and Cheeseburger only)
        products = [
            {
                "id": "BRG-001",
                "name": "Classic Burger",
                "category": "Burgers",
                "price": "$5.99",
                "stock": "35 pcs",
                "status": "In Stock"
            },
            {
                "id": "BRG-002",
                "name": "Cheeseburger",
                "category": "Burgers",
                "price": "$6.99",
                "stock": "28 pcs",
                "status": "In Stock"
            }
        ]

        for i, prod in enumerate(products):
            row_frame = customtkinter.CTkFrame(
                product_scroll,
                corner_radius=8,
                fg_color="#1e293b" if i % 2 == 0 else "#253347"
            )
            row_frame.grid(row=i, column=0, padx=5, pady=4, sticky="ew")

            # Column weights match header
            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=3)
            row_frame.grid_columnconfigure(2, weight=2)
            row_frame.grid_columnconfigure(3, weight=2)
            row_frame.grid_columnconfigure(4, weight=2)
            row_frame.grid_columnconfigure(5, weight=2)

            # Item ID
            customtkinter.CTkLabel(
                row_frame, text=prod["id"], font=customtkinter.CTkFont(weight="bold"), text_color="#38bdf8"
            ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

            # Product Name
            customtkinter.CTkLabel(
                row_frame, text=prod["name"], font=customtkinter.CTkFont(size=14, weight="bold"), text_color="#f8fafc"
            ).grid(row=0, column=1, padx=10, pady=10, sticky="w")

            # Category
            customtkinter.CTkLabel(
                row_frame, text=prod["category"], text_color="#94a3b8"
            ).grid(row=0, column=2, padx=10, pady=10, sticky="w")

            # Price
            customtkinter.CTkLabel(
                row_frame, text=prod["price"], font=customtkinter.CTkFont(weight="bold"), text_color="#4ade80"
            ).grid(row=0, column=3, padx=10, pady=10)

            # Stock
            customtkinter.CTkLabel(
                row_frame, text=prod["stock"], text_color="#e2e8f0"
            ).grid(row=0, column=4, padx=10, pady=10)

            # Status pill badge
            status_frame = customtkinter.CTkFrame(row_frame, corner_radius=12, fg_color="#065f46")
            status_frame.grid(row=0, column=5, padx=10, pady=8)
            customtkinter.CTkLabel(
                status_frame, text=prod["status"], text_color="#6ee7b7", font=customtkinter.CTkFont(size=12, weight="bold")
            ).pack(padx=10, pady=2)

    def _create_action_buttons(self):
        # Responsive bottom action bar frame
        action_bar = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#1e293b")
        action_bar.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Configure equal weights for all three button columns so they expand and contract evenly
        action_bar.grid_columnconfigure(0, weight=1)
        action_bar.grid_columnconfigure(1, weight=1)
        action_bar.grid_columnconfigure(2, weight=1)

        # 1. Add Product Button (Emerald Green)
        add_btn = customtkinter.CTkButton(
            action_bar,
            text="➕ Add Product",
            height=44,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            text_color="#ffffff"
        )
        add_btn.grid(row=0, column=0, padx=10, pady=12, sticky="ew")

        # 2. Update Price Button (Warm Amber)
        update_btn = customtkinter.CTkButton(
            action_bar,
            text="✏️ Update Price",
            height=44,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#f59e0b",
            hover_color="#d97706",
            text_color="#ffffff"
        )
        update_btn.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        # 3. Delete Product Button (Crimson Red)
        delete_btn = customtkinter.CTkButton(
            action_bar,
            text="🗑️ Delete Product",
            height=44,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="#ffffff"
        )
        delete_btn.grid(row=0, column=2, padx=10, pady=12, sticky="ew")


if __name__ == "__main__":
    app = BurgerInventoryApp()
    app.mainloop()
