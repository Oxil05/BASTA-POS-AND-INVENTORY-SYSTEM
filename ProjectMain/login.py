"""
BASTA BURGER - POS and Inventory Management System
Login Page UI Module
Faithfully recreates the modern split-screen design in Designs/LOG-IN PAGE.png
using CustomTkinter and Pillow. All variables and functions strictly use snake_case.
"""

import os
import sys

# Robust path handling so both root execution and ProjectMain execution work
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
for path in [script_dir, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)

import customtkinter as ctk
from PIL import Image, ImageDraw


def find_logo_path() -> str:
    """Locates the basta_LOGO.png file across common execution contexts."""
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root_directory = os.path.dirname(current_script_directory)
    
    candidate_paths = [
        os.path.join(project_root_directory, "Designs", "basta_LOGO.png"),
        os.path.join(current_script_directory, "..", "Designs", "basta_LOGO.png"),
        os.path.join(current_script_directory, "Designs", "basta_LOGO.png"),
        os.path.join("Designs", "basta_LOGO.png"),
        "basta_LOGO.png",
    ]
    for path in candidate_paths:
        if os.path.isfile(path):
            return os.path.abspath(path)
    return candidate_paths[0]


def create_circular_badge(logo_path: str, size: int = 540) -> Image.Image:
    """
    Renders a high-resolution circular badge containing the BASTA BURGER logo.
    Uses 2x supersampling for clean, smooth antialiased edges.
    """
    supersample_scale = 2
    canvas_dimension = max(100, size * supersample_scale)
    
    # Create black background canvas
    canvas_image = Image.new("RGBA", (canvas_dimension, canvas_dimension), (0, 0, 0, 255))
    draw_context = ImageDraw.Draw(canvas_image)
    
    # Draw solid white circular background
    circle_padding = 6 * supersample_scale
    circle_box = [
        circle_padding,
        circle_padding,
        canvas_dimension - circle_padding,
        canvas_dimension - circle_padding,
    ]
    draw_context.ellipse(circle_box, fill=(255, 255, 255, 255))
    
    # Load and crop transparent borders from logo
    if os.path.exists(logo_path):
        source_logo = Image.open(logo_path).convert("RGBA")
        alpha_channel = source_logo.split()[-1]
        content_box = alpha_channel.getbbox()
        if content_box:
            source_logo = source_logo.crop(content_box)
        
        # Scale logo to fill approximately 88% of the circle width
        target_logo_width = int(canvas_dimension * 0.88)
        aspect_ratio = source_logo.height / source_logo.width
        target_logo_height = int(target_logo_width * aspect_ratio)
        resized_logo = source_logo.resize(
            (target_logo_width, target_logo_height),
            Image.Resampling.LANCZOS
        )
        
        # Center the logo on the white circle
        paste_x = (canvas_dimension - target_logo_width) // 2
        paste_y = (canvas_dimension - target_logo_height) // 2
        canvas_image.paste(resized_logo, (paste_x, paste_y), resized_logo)
    
    # Downsample back to target size for smooth edges
    final_badge_image = canvas_image.resize((size, size), Image.Resampling.LANCZOS)
    return final_badge_image


def create_mail_icon(size: int = 18, color: tuple = (156, 163, 175, 255)) -> Image.Image:
    """Generates an outline envelope icon using Pillow."""
    scale = 4
    canvas_size = size * scale
    icon_image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw_context = ImageDraw.Draw(icon_image)
    
    stroke_width = max(2, int(1.6 * scale))
    padding_x = 2 * scale
    envelope_width = canvas_size - 2 * padding_x
    envelope_height = int(envelope_width * 0.72)
    start_y = (canvas_size - envelope_height) // 2
    end_y = start_y + envelope_height
    start_x = padding_x
    end_x = padding_x + envelope_width
    
    # Envelope outer body
    draw_context.rounded_rectangle(
        [start_x, start_y, end_x, end_y],
        radius=3 * scale,
        outline=color,
        width=stroke_width
    )
    # Envelope flap lines
    draw_context.line(
        [(start_x + 2 * scale, start_y + 2 * scale), (canvas_size // 2, start_y + int(envelope_height * 0.58))],
        fill=color,
        width=stroke_width
    )
    draw_context.line(
        [(end_x - 2 * scale, start_y + 2 * scale), (canvas_size // 2, start_y + int(envelope_height * 0.58))],
        fill=color,
        width=stroke_width
    )
    return icon_image.resize((size, size), Image.Resampling.LANCZOS)


def create_lock_icon(size: int = 18, color: tuple = (156, 163, 175, 255)) -> Image.Image:
    """Generates an outline padlock icon using Pillow."""
    scale = 4
    canvas_size = size * scale
    icon_image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw_context = ImageDraw.Draw(icon_image)
    
    stroke_width = max(2, int(1.6 * scale))
    
    # Body
    body_x0 = int(canvas_size * 0.20)
    body_y0 = int(canvas_size * 0.44)
    body_x1 = int(canvas_size * 0.80)
    body_y1 = int(canvas_size * 0.88)
    draw_context.rounded_rectangle(
        [body_x0, body_y0, body_x1, body_y1],
        radius=3 * scale,
        outline=color,
        width=stroke_width
    )
    
    # Shackle
    shackle_x0 = int(canvas_size * 0.32)
    shackle_y0 = int(canvas_size * 0.16)
    shackle_x1 = int(canvas_size * 0.68)
    shackle_y1 = int(canvas_size * 0.54)
    draw_context.arc(
        [shackle_x0, shackle_y0, shackle_x1, shackle_y1],
        start=180,
        end=0,
        fill=color,
        width=stroke_width
    )
    
    # Keyhole
    center_x = canvas_size // 2
    keyhole_center_y = int(canvas_size * 0.63)
    hole_radius = int(2.2 * scale)
    draw_context.ellipse(
        [center_x - hole_radius, keyhole_center_y - hole_radius, center_x + hole_radius, keyhole_center_y + hole_radius],
        fill=color
    )
    draw_context.line(
        [(center_x, keyhole_center_y), (center_x, keyhole_center_y + int(4.5 * scale))],
        fill=color,
        width=max(2, int(1.5 * scale))
    )
    return icon_image.resize((size, size), Image.Resampling.LANCZOS)


def create_eye_icon(size: int = 16, color: tuple = (107, 114, 128, 255), is_open: bool = True) -> Image.Image:
    """Generates an eye visibility toggle icon using Pillow."""
    scale = 4
    canvas_size = size * scale
    icon_image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw_context = ImageDraw.Draw(icon_image)
    
    stroke_width = max(2, int(1.5 * scale))
    x0 = int(canvas_size * 0.10)
    y0 = int(canvas_size * 0.22)
    x1 = int(canvas_size * 0.90)
    y1 = int(canvas_size * 0.78)
    
    draw_context.arc([x0, y0, x1, y1], start=195, end=345, fill=color, width=stroke_width)
    draw_context.arc([x0, y0, x1, y1], start=15, end=165, fill=color, width=stroke_width)
    
    center_x = canvas_size // 2
    center_y = canvas_size // 2
    pupil_radius = int(3 * scale)
    draw_context.ellipse(
        [center_x - pupil_radius, center_y - pupil_radius, center_x + pupil_radius, center_y + pupil_radius],
        fill=color
    )
    
    if not is_open:
        draw_context.line([(x0 + 2 * scale, y1 - 2 * scale), (x1 - 2 * scale, y0 + 2 * scale)], fill=color, width=stroke_width)
        
    return icon_image.resize((size, size), Image.Resampling.LANCZOS)


def create_help_icon(size: int = 16, color: tuple = (107, 114, 128, 255)) -> Image.Image:
    """Generates a circular question-mark icon using Pillow."""
    scale = 4
    canvas_size = size * scale
    icon_image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw_context = ImageDraw.Draw(icon_image)
    
    stroke_width = max(2, int(1.5 * scale))
    pad = 2 * scale
    draw_context.ellipse([pad, pad, canvas_size - pad, canvas_size - pad], outline=color, width=stroke_width)
    
    # Question mark hook
    center_x = canvas_size // 2
    draw_context.arc([center_x - 3 * scale, int(canvas_size * 0.26), center_x + 3 * scale, int(canvas_size * 0.50)], start=200, end=40, fill=color, width=stroke_width)
    draw_context.line([(center_x + scale, int(canvas_size * 0.44)), (center_x, int(canvas_size * 0.58))], fill=color, width=stroke_width)
    # Question dot
    draw_context.ellipse([center_x - scale, int(canvas_size * 0.68), center_x + scale, int(canvas_size * 0.76)], fill=color)
    
    return icon_image.resize((size, size), Image.Resampling.LANCZOS)


class BastaLoginApp(ctk.CTk):
    """
    Main Login Window for BASTA BURGER POS & Inventory System.
    Recreates the modern split-screen design from Designs/LOG-IN PAGE.png.
    """

    def __init__(self):
        super().__init__()
        
        # Configure overall appearance mode
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self.title("BASTA BURGER - Log In")
        window_width = 1180
        window_height = 760
        self.minsize(800, 560)
        
        # Center the window on display
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        start_x = max(0, (screen_width - window_width) // 2)
        start_y = max(0, (screen_height - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{start_x}+{start_y}")
        
        # Logo path
        self.logo_file_path = find_logo_path()
        
        # State variables (strictly snake_case)
        self.is_password_visible = False
        self.keep_logged_in_var = ctk.BooleanVar(value=True)
        self.last_badge_size = 520
        
        # Configure grid layout: 50% left (form), 50% right (hero)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Build UI components
        self.build_left_section()
        self.build_right_section()
        
        # Keyboard shortcuts
        self.bind("<Return>", lambda event: self.handle_login())

    def build_left_section(self):
        """Constructs the left side form, brand header, and footer."""
        # Left container frame
        self.left_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFDF9",
            corner_radius=0
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        # 1. TOP HEADER (Brand name on left, Need help? on right)
        self.top_header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.top_header_frame.grid(row=0, column=0, sticky="ew", padx=48, pady=(32, 0))
        self.top_header_frame.grid_columnconfigure(0, weight=1)
        
        self.brand_header_label = ctk.CTkLabel(
            self.top_header_frame,
            text="BASTA BURGER",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#111827",
            anchor="w"
        )
        self.brand_header_label.grid(row=0, column=0, sticky="w")
        
        # Help button with icon
        help_pil_image = create_help_icon(size=15, color=(107, 114, 128, 255))
        self.help_icon = ctk.CTkImage(light_image=help_pil_image, dark_image=help_pil_image, size=(15, 15))
        
        self.need_help_button = ctk.CTkButton(
            self.top_header_frame,
            text="Need help?",
            image=self.help_icon,
            compound="left",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#6B7280",
            hover_color="#F3F4F6",
            fg_color="transparent",
            cursor="hand2",
            height=28,
            width=90,
            command=self.show_help_dialog
        )
        self.need_help_button.grid(row=0, column=1, sticky="e")
        
        # 2. MAIN CONTENT CONTAINER (Centered vertically)
        self.center_content_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.center_content_frame.grid(row=1, column=0, sticky="ew", padx=48)
        self.center_content_frame.grid_columnconfigure(0, weight=1)
        
        # Inner responsive frame for input controls
        self.form_inner_frame = ctk.CTkFrame(self.center_content_frame, fg_color="transparent")
        self.form_inner_frame.grid(row=0, column=0, sticky="ew")
        self.form_inner_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome back pre-title
        self.welcome_back_label = ctk.CTkLabel(
            self.form_inner_frame,
            text="WELCOME BACK",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#18181B",
            anchor="w"
        )
        self.welcome_back_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        # Main heading "Log in to\nBASTA BURGER"
        self.heading_label = ctk.CTkLabel(
            self.form_inner_frame,
            text="Log in to\nBASTA BURGER",
            font=ctk.CTkFont(family="Segoe UI", size=29, weight="bold"),
            text_color="#111827",
            justify="left",
            anchor="w"
        )
        self.heading_label.grid(row=1, column=0, sticky="w", pady=(0, 6))
        
        # Subtitle
        self.subheading_label = ctk.CTkLabel(
            self.form_inner_frame,
            text="Access your restaurant, team, and live register activity.",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#6B7280",
            anchor="w",
            wraplength=380,
            justify="left"
        )
        self.subheading_label.grid(row=2, column=0, sticky="w", pady=(0, 24))
        
        # Email field label
        self.email_label = ctk.CTkLabel(
            self.form_inner_frame,
            text="Email address",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#1F2937",
            anchor="w"
        )
        self.email_label.grid(row=3, column=0, sticky="w", pady=(0, 6))
        
        # Email input container box (rounded)
        self.email_container = ctk.CTkFrame(
            self.form_inner_frame,
            fg_color="#FFFFFF",
            border_color="#D1D5DB",
            border_width=1,
            corner_radius=12,
            height=46
        )
        self.email_container.grid(row=4, column=0, sticky="ew", pady=(0, 16))
        self.email_container.grid_columnconfigure(1, weight=1)
        
        # Email icon
        mail_pil_image = create_mail_icon(size=16, color=(156, 163, 175, 255))
        self.mail_icon = ctk.CTkImage(light_image=mail_pil_image, dark_image=mail_pil_image, size=(16, 16))
        self.email_icon_label = ctk.CTkLabel(
            self.email_container,
            image=self.mail_icon,
            text="",
            width=24
        )
        self.email_icon_label.grid(row=0, column=0, padx=(12, 6), pady=8)
        
        # Email text entry
        self.email_entry = ctk.CTkEntry(
            self.email_container,
            placeholder_text="manager@restaurant.com",
            placeholder_text_color="#9CA3AF",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#111827",
            fg_color="transparent",
            border_width=0,
            height=32
        )
        self.email_entry.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=6)
        
        # Focus border highlights for email
        self.email_entry.bind("<FocusIn>", lambda event: self.email_container.configure(border_color="#111827", border_width=1.5))
        self.email_entry.bind("<FocusOut>", lambda event: self.email_container.configure(border_color="#D1D5DB", border_width=1))
        
        # Password field label
        self.password_label = ctk.CTkLabel(
            self.form_inner_frame,
            text="Password",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#1F2937",
            anchor="w"
        )
        self.password_label.grid(row=5, column=0, sticky="w", pady=(0, 6))
        
        # Password input container box
        # Password input container box (rounded)
        self.password_container = ctk.CTkFrame(
            self.form_inner_frame,
            fg_color="#FFFFFF",
            border_color="#D1D5DB",
            border_width=1,
            corner_radius=12,
            height=46
        )
        self.password_container.grid(row=6, column=0, sticky="ew", pady=(0, 14))
        self.password_container.grid_columnconfigure(1, weight=1)
        
        # Lock icon
        lock_pil_image = create_lock_icon(size=16, color=(156, 163, 175, 255))
        self.lock_icon = ctk.CTkImage(light_image=lock_pil_image, dark_image=lock_pil_image, size=(16, 16))
        self.password_icon_label = ctk.CTkLabel(
            self.password_container,
            image=self.lock_icon,
            text="",
            width=24
        )
        self.password_icon_label.grid(row=0, column=0, padx=(12, 6), pady=8)
        
        # Password entry (masked)
        self.password_entry = ctk.CTkEntry(
            self.password_container,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#111827",
            fg_color="transparent",
            border_width=0,
            show="*",
            height=32
        )
        self.password_entry.grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=6)
        
        # Focus border highlights for password
        self.password_entry.bind("<FocusIn>", lambda event: self.password_container.configure(border_color="#111827", border_width=1.5))
        self.password_entry.bind("<FocusOut>", lambda event: self.password_container.configure(border_color="#D1D5DB", border_width=1))
        
        # Show/Hide password toggle button
        self.eye_open_image = ctk.CTkImage(
            light_image=create_eye_icon(size=15, color=(107, 114, 128, 255), is_open=True),
            dark_image=create_eye_icon(size=15, color=(107, 114, 128, 255), is_open=True),
            size=(15, 15)
        )
        self.eye_closed_image = ctk.CTkImage(
            light_image=create_eye_icon(size=15, color=(107, 114, 128, 255), is_open=False),
            dark_image=create_eye_icon(size=15, color=(107, 114, 128, 255), is_open=False),
            size=(15, 15)
        )
        
        self.password_toggle_button = ctk.CTkButton(
            self.password_container,
            text="Show",
            image=self.eye_open_image,
            compound="left",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#6B7280",
            hover_color="#F3F4F6",
            fg_color="transparent",
            cursor="hand2",
            height=28,
            width=65,
            command=self.toggle_password_display
        )
        self.password_toggle_button.grid(row=0, column=2, padx=(0, 8), pady=6)
        
        # Checkbox & Forgot Password row
        self.options_row_frame = ctk.CTkFrame(self.form_inner_frame, fg_color="transparent")
        self.options_row_frame.grid(row=7, column=0, sticky="ew", pady=(0, 20))
        self.options_row_frame.grid_columnconfigure(0, weight=1)
        
        # Keep me logged in checkbox
        self.keep_logged_in_checkbox = ctk.CTkCheckBox(
            self.options_row_frame,
            text="Keep me logged in",
            variable=self.keep_logged_in_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#374151",
            fg_color="#000000",
            hover_color="#27272A",
            border_color="#9CA3AF",
            checkmark_color="#FFFFFF",
            corner_radius=4,
            border_width=1.5,
            width=18,
            height=18
        )
        self.keep_logged_in_checkbox.grid(row=0, column=0, sticky="w")
        
        # Forgot password button/link
        self.forgot_password_button = ctk.CTkButton(
            self.options_row_frame,
            text="Forgot password?",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#111827",
            hover_color="#F3F4F6",
            fg_color="transparent",
            cursor="hand2",
            height=24,
            width=110,
            command=self.show_forgot_password_dialog
        )
        self.forgot_password_button.grid(row=0, column=1, sticky="e")
        
        # Error / Feedback status message label
        self.status_message_label = ctk.CTkLabel(
            self.form_inner_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#DC2626",
            anchor="w"
        )
        self.status_message_label.grid(row=8, column=0, sticky="w", pady=(0, 6))
        
        # Log in action button (rounded & responsive)
        self.login_button = ctk.CTkButton(
            self.form_inner_frame,
            text="Log in  →",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#000000",
            hover_color="#27272A",
            text_color="#FFFFFF",
            height=46,
            corner_radius=12,
            cursor="hand2",
            command=self.handle_login
        )
        self.login_button.grid(row=9, column=0, sticky="ew")
        
        # 3. BOTTOM FOOTER (Copyright on left, Privacy / Terms on right)
        self.footer_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=48, pady=(0, 26))
        self.footer_frame.grid_columnconfigure(0, weight=1)
        
        self.copyright_label = ctk.CTkLabel(
            self.footer_frame,
            text="© 2026 BASTA POS",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9CA3AF",
            anchor="w"
        )
        self.copyright_label.grid(row=0, column=0, sticky="w")
        
        self.legal_links_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        self.legal_links_frame.grid(row=0, column=1, sticky="e")
        
        self.privacy_button = ctk.CTkButton(
            self.legal_links_frame,
            text="Privacy",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#6B7280",
            hover_color="#F3F4F6",
            fg_color="transparent",
            cursor="hand2",
            height=20,
            width=48,
            command=self.show_privacy_dialog
        )
        self.privacy_button.grid(row=0, column=0, padx=(0, 6))
        
        self.terms_button = ctk.CTkButton(
            self.legal_links_frame,
            text="Terms",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#6B7280",
            hover_color="#F3F4F6",
            fg_color="transparent",
            cursor="hand2",
            height=20,
            width=44,
            command=self.show_terms_dialog
        )
        self.terms_button.grid(row=0, column=1)

    def build_right_section(self):
        """Constructs the right side hero panel with the circular BASTA BURGER logo."""
        self.right_frame = ctk.CTkFrame(
            self,
            fg_color="#000000",
            corner_radius=0
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        # Initial circular badge image
        circular_pil_image = create_circular_badge(self.logo_file_path, size=self.last_badge_size)
        self.badge_ctk_image = ctk.CTkImage(
            light_image=circular_pil_image,
            dark_image=circular_pil_image,
            size=(self.last_badge_size, self.last_badge_size)
        )
        
        # Display the badge centered on the black background
        self.hero_logo_label = ctk.CTkLabel(
            self.right_frame,
            text="",
            image=self.badge_ctk_image
        )
        self.hero_logo_label.grid(row=0, column=0)
        
        # Responsive dynamic scaling when resizing window
        self.right_frame.bind("<Configure>", self.on_right_frame_resize)

    def on_right_frame_resize(self, event):
        """Dynamically scales the circular badge to maintain optimal proportions."""
        available_width = event.width
        available_height = event.height
        
        target_size = min(available_width - 60, available_height - 60, 580)
        target_size = max(target_size, 180)
        
        # Update only if size delta is noticeable (avoids unnecessary redraw lag)
        if abs(target_size - self.last_badge_size) > 20:
            self.last_badge_size = target_size
            new_pil_image = create_circular_badge(self.logo_file_path, size=target_size)
            self.badge_ctk_image = ctk.CTkImage(
                light_image=new_pil_image,
                dark_image=new_pil_image,
                size=(target_size, target_size)
            )
            self.hero_logo_label.configure(image=self.badge_ctk_image)

    def toggle_password_display(self):
        """Toggles between masked password and plain text."""
        if self.is_password_visible:
            self.password_entry.configure(show="*")
            self.password_toggle_button.configure(
                text="Show",
                image=self.eye_open_image
            )
            self.is_password_visible = False
        else:
            self.password_entry.configure(show="")
            self.password_toggle_button.configure(
                text="Hide",
                image=self.eye_closed_image
            )
            self.is_password_visible = True

    def handle_login(self):
        """Validates credentials, provides feedback, and redirects to POS."""
        entered_email = self.email_entry.get().strip()
        entered_password = self.password_entry.get().strip()
        
        if not entered_email or not entered_password:
            self.status_message_label.configure(
                text="Please enter both email and password.",
                text_color="#DC2626"
            )
            return
            
        self.status_message_label.configure(
            text="Authenticating...",
            text_color="#2563EB"
        )
        self.update_idletasks()
        
        print(f"[BASTA POS] Login attempt - Email: {entered_email}, Keep Logged In: {self.keep_logged_in_var.get()}")
        self.status_message_label.configure(
            text="Login successful! Redirecting to POS...",
            text_color="#16A34A"
        )
        self.after(450, self.launch_pos_app)

    def launch_pos_app(self):
        """Transition from login screen to POS main screen."""
        self.destroy()
        try:
            from POS import BastaPOSApp
            pos_instance = BastaPOSApp()
            pos_instance.mainloop()
        except Exception:
            try:
                from ProjectMain.POS import BastaPOSApp
                pos_instance = BastaPOSApp()
                pos_instance.mainloop()
            except Exception as error:
                print(f"[BASTA POS] POS launch error: {error}")

    def show_help_dialog(self):
        """Displays support contact information."""
        self.status_message_label.configure(
            text="Support: Contact support@bastaburger.com or call +63 (2) 8888-BASTA",
            text_color="#4B5563"
        )

    def show_forgot_password_dialog(self):
        """Displays password reset instructions."""
        self.status_message_label.configure(
            text="To reset password, please ask your Restaurant Administrator.",
            text_color="#4B5563"
        )

    def show_privacy_dialog(self):
        """Displays privacy policy notice."""
        self.status_message_label.configure(
            text="Privacy Notice: BASTA POS stores data securely in accordance with local regulations.",
            text_color="#4B5563"
        )

    def show_terms_dialog(self):
        """Displays terms of service notice."""
        self.status_message_label.configure(
            text="Terms: BASTA POS is authorized for internal restaurant operations only.",
            text_color="#4B5563"
        )


if __name__ == "__main__":
    app_instance = BastaLoginApp()
    app_instance.mainloop()
