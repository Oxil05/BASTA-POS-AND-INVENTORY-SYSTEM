"""
BASTA BURGER - Inventory Module Wrapper
Imports and runs the InventoryOverviewApp from ProjectMain/inventory_overview.py.
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
for path in [script_dir, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from inventory_overview import InventoryOverviewApp
except ImportError:
    from ProjectMain.inventory_overview import InventoryOverviewApp

if __name__ == "__main__":
    app = InventoryOverviewApp()
    app.mainloop()
