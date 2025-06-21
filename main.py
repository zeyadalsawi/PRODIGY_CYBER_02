import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import json
import sys
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

LANGUAGES = {
    'en': {
        'title': '🔒 Image Encryptor / Decryptor',
        'select_image': 'Select image(s) to encrypt/decrypt:',
        'browse': 'Browse',
        'key_label': 'Enter numeric key (0-255):',
        'encrypt': 'Encrypt',
        'decrypt': 'Decrypt',
        'reset': 'Reset',
        'help': 'Help',
        'footer': '© 2025 | Designed by Zeyad | Powered by Tkinter',
        'success_encrypt': 'Encrypted Successfully',
        'success_decrypt': 'Decrypted Successfully',
        'output_saved': 'Image saved as',
        'invalid_key': 'Key must be an integer between 0 and 255.',
        'no_file': 'Please select at least one image file.',
        'help_text': 'This app encrypts/decrypts images using XOR. Select one or more images, enter a key (0-255), and click Encrypt or Decrypt.',
        'already_encrypted': 'Warning: This image appears already encrypted.',
        'choose_output': 'Choose Output Folder',
        'language': 'العربية',
    },
    'ar': {
        'title': '🔒 برنامج تشفير/فك تشفير الصور',
        'select_image': 'اختر صورة (صور) للتشفير أو فك التشفير:',
        'browse': 'تصفح',
        'key_label': 'أدخل مفتاح رقمي (0-255):',
        'encrypt': 'تشفير',
        'decrypt': 'فك التشفير',
        'reset': 'إعادة ضبط',
        'help': 'مساعدة',
        'footer': '© 2025 | تصميم زياد | يعمل بواسطة Tkinter',
        'success_encrypt': 'تم التشفير بنجاح',
        'success_decrypt': 'تم فك التشفير بنجاح',
        'output_saved': 'تم حفظ الصورة باسم',
        'invalid_key': 'المفتاح يجب أن يكون رقم بين 0 و255.',
        'no_file': 'يرجى اختيار صورة واحدة على الأقل.',
        'help_text': 'يشفّر هذا التطبيق الصور باستخدام XOR. اختر صورة أو أكثر، أدخل مفتاح (0-255)، ثم اضغط تشفير أو فك التشفير.',
        'already_encrypted': 'تحذير: تبدو هذه الصورة مشفرة بالفعل.',
        'choose_output': 'اختر مجلد الحفظ',
        'language': 'English',
    }
}

CONFIG_FILE = 'user_config.json'
LOGO_PATH = 'app_logo.png'

# Helper to load/save config
class UserConfig:
    def __init__(self):
        self.data = {'last_folder': '', 'last_key': '', 'lang': 'en'}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.data.update(json.load(f))
            except Exception:
                pass
    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f)

user_config = UserConfig()

# Encrypt/Decrypt function using XOR with a key
def process_image(input_path, output_path, key):
    try:
        img = Image.open(input_path)
        img = img.convert('RGB')
        pixels = img.load()
        width, height = img.size
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                pixels[x, y] = (
                    r ^ key,
                    g ^ key,
                    b ^ key
                )
        img.save(output_path)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

class ImageEncryptorApp:
    def __init__(self, master):
        self.master = master
        self.lang = user_config.data.get('lang', 'en')
        self.strings = LANGUAGES[self.lang]
        master.title(self.strings['title'])
        master.geometry("540x600")
        master.configure(bg="#232946")
        self.file_paths = []
        self.preview_images = []
        self.last_folder = user_config.data.get('last_folder', '')
        self.last_key = user_config.data.get('last_key', '')

        # Custom Fonts
        self.title_font = ("Helvetica", 22, "bold")
        self.label_font = ("Helvetica", 12, "bold")
        self.button_font = ("Helvetica", 11, "bold")
        self.footer_font = ("Helvetica", 9, "italic")

        # Logo
        logo_frame = tk.Frame(master, bg="#232946")
        logo_frame.pack(pady=(16, 5), fill=tk.BOTH, expand=False)
        try:
            logo_img = Image.open(LOGO_PATH)
            logo_img = logo_img.resize((60, 60), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.logo_photo, bg="#232946").pack()
        except Exception:
            tk.Label(logo_frame, text="🔒", font=("Helvetica", 36), bg="#232946", fg="#eebbc3").pack()

        # Title
        self.title_label = tk.Label(master, text=self.strings['title'], font=self.title_font, fg="#eebbc3", bg="#232946")
        self.title_label.pack(pady=(0, 10), fill=tk.BOTH, expand=False)

        # Language toggle
        lang_btn = tk.Button(master, text=self.strings['language'], font=self.button_font, bg="#b8c1ec", fg="#232946", command=self.toggle_language, relief=tk.RAISED, bd=2, width=10)
        lang_btn.pack(pady=(0, 7), fill=tk.X, expand=False)
        self.add_tooltip(lang_btn, "Switch language")

        # Card Frame
        card = tk.Frame(master, bg="#393e63", bd=2, relief=tk.RIDGE)
        card.pack(pady=8, padx=18, fill=tk.BOTH, expand=True)

        # File selection area
        self.label = tk.Label(card, text=self.strings['select_image'], font=self.label_font, fg="#b8c1ec", bg="#393e63")
        self.label.pack(pady=(12, 2))
        file_btn_frame = tk.Frame(card, bg="#393e63")
        file_btn_frame.pack(pady=(0, 8))
        self.select_button = tk.Button(file_btn_frame, text=self.strings['browse'], font=self.button_font, bg="#eebbc3", fg="#232946", activebackground="#b8c1ec", activeforeground="#232946", command=self.browse_files, relief=tk.RAISED, bd=2)
        self.select_button.pack(side=tk.LEFT, padx=(0, 8))
        self.add_tooltip(self.select_button, "Select images (supports multiple)")
        if DND_AVAILABLE and hasattr(master, 'drop_target_register'):
            self.dnd_label = tk.Label(file_btn_frame, text="⬇ Drag images here ⬇", font=("Helvetica", 10), fg="#eebbc3", bg="#393e63")
            self.dnd_label.pack(side=tk.LEFT)
            master.drop_target_register(DND_FILES)
            master.dnd_bind('<<Drop>>', self.drop_files)
        # Preview area
        self.preview_frame = tk.Frame(card, bg="#393e63")
        self.preview_frame.pack(pady=(0, 8))
        self.preview_labels = []

        # Key entry
        self.key_label = tk.Label(card, text=self.strings['key_label'], font=self.label_font, fg="#b8c1ec", bg="#393e63")
        self.key_label.pack(pady=(0, 2))
        key_frame = tk.Frame(card, bg="#393e63")
        key_frame.pack(pady=(0, 8))
        self.key_entry = tk.Entry(key_frame, font=self.label_font, width=8, justify='center', bg="#fffffe", fg="#232946")
        self.key_entry.pack(side=tk.LEFT, padx=(0, 8))
        if self.last_key:
            self.key_entry.insert(0, self.last_key)
        self.add_tooltip(self.key_entry, "Encryption key (0-255)")
        # Output folder
        self.output_btn = tk.Button(key_frame, text=self.strings['choose_output'], font=("Helvetica", 10), bg="#b8c1ec", fg="#232946", command=self.choose_output_folder)
        self.output_btn.pack(side=tk.LEFT)
        self.add_tooltip(self.output_btn, "Choose output folder")
        self.output_folder = self.last_folder or os.getcwd()

        # Action buttons
        action_frame = tk.Frame(card, bg="#393e63")
        action_frame.pack(pady=(0, 10))
        self.encrypt_button = tk.Button(action_frame, text=self.strings['encrypt'], font=self.button_font, width=12, bg="#eebbc3", fg="#232946", activebackground="#b8c1ec", activeforeground="#232946", command=self.encrypt, relief=tk.RAISED, bd=2)
        self.encrypt_button.pack(side=tk.LEFT, padx=8)
        self.add_tooltip(self.encrypt_button, "Encrypt selected images")
        self.decrypt_button = tk.Button(action_frame, text=self.strings['decrypt'], font=self.button_font, width=12, bg="#eebbc3", fg="#232946", activebackground="#b8c1ec", activeforeground="#232946", command=self.decrypt, relief=tk.RAISED, bd=2)
        self.decrypt_button.pack(side=tk.LEFT, padx=8)
        self.add_tooltip(self.decrypt_button, "Decrypt selected images")
        self.reset_btn = tk.Button(action_frame, text=self.strings['reset'], font=self.button_font, width=10, bg="#b8c1ec", fg="#232946", command=self.reset_form)
        self.reset_btn.pack(side=tk.LEFT, padx=8)
        self.add_tooltip(self.reset_btn, "Clear all fields")
        self.help_btn = tk.Button(action_frame, text=self.strings['help'], font=self.button_font, width=8, bg="#b8c1ec", fg="#232946", command=self.show_help)
        self.help_btn.pack(side=tk.LEFT, padx=8)
        self.add_tooltip(self.help_btn, "Show help/instructions")

        # Progress bar
        self.progress = ttk.Progressbar(card, orient='horizontal', length=320, mode='determinate')
        self.progress.pack(pady=(0, 10))
        self.progress['value'] = 0

        # Footer
        self.footer_label = tk.Label(master, text=self.strings['footer'], font=self.footer_font, fg="#b8c1ec", bg="#232946")
        self.footer_label.pack(side=tk.BOTTOM, pady=12, fill=tk.X)

        # Keyboard shortcuts
        master.bind('<Return>', lambda e: self.encrypt())
        master.bind('<Escape>', lambda e: master.quit())

        # Hover effects
        for btn in [self.encrypt_button, self.decrypt_button, self.select_button, self.reset_btn, self.help_btn, lang_btn, self.output_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#b8c1ec", fg="#232946"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#eebbc3" if b in [self.encrypt_button, self.decrypt_button, self.select_button] else "#b8c1ec", fg="#232946"))

        self.update_preview()

    # --- UI/UX Methods ---
    def add_tooltip(self, widget, text):
        def on_enter(e):
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + 20
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=text, bg="#22223b", fg="#eebbc3", relief=tk.SOLID, borderwidth=1, font=("Helvetica", 9))
            label.pack()
        def on_leave(e):
            if hasattr(self, 'tooltip') and self.tooltip:
                self.tooltip.destroy()
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def show_help(self):
        messagebox.showinfo(self.strings['help'], self.strings['help_text'])

    def reset_form(self):
        self.file_paths = []
        self.last_folder = os.getcwd()
        self.key_entry.delete(0, tk.END)
        self.preview_images.clear()
        self.update_preview()
        self.progress['value'] = 0

    def toggle_language(self):
        self.lang = 'ar' if self.lang == 'en' else 'en'
        user_config.data['lang'] = self.lang
        user_config.save()
        self.master.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def choose_output_folder(self):
        folder = filedialog.askdirectory(title=self.strings['choose_output'])
        if folder:
            self.output_folder = folder
            user_config.data['last_folder'] = folder
            user_config.save()

    def browse_files(self):
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All files", "*.*")]
        files = filedialog.askopenfilenames(title=self.strings['select_image'], initialdir=self.last_folder, filetypes=filetypes)
        if files:
            self.file_paths = list(files)
            self.last_folder = os.path.dirname(self.file_paths[0])
            user_config.data['last_folder'] = self.last_folder
            user_config.save()
            self.update_preview()

    def drop_files(self, event):
        files = self.master.tk.splitlist(event.data)
        self.file_paths = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))]
        if self.file_paths:
            self.last_folder = os.path.dirname(self.file_paths[0])
            user_config.data['last_folder'] = self.last_folder
            user_config.save()
            self.update_preview()

    def update_preview(self):
        # Clear previous previews
        for lbl in getattr(self, 'preview_labels', []):
            lbl.destroy()
        self.preview_labels = []
        self.preview_images = []
        if not self.file_paths:
            return
        for i, path in enumerate(self.file_paths[:3]):  # Show up to 3 previews
            try:
                img = Image.open(path)
                img.thumbnail((90, 90))
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.preview_frame, image=photo, bg="#393e63", borderwidth=2, relief=tk.GROOVE)
                lbl.image = photo
                lbl.pack(side=tk.LEFT, padx=7)
                self.preview_labels.append(lbl)
                self.preview_images.append(photo)
            except Exception:
                pass
        if len(self.file_paths) > 3:
            more_lbl = tk.Label(self.preview_frame, text=f"+{len(self.file_paths)-3} more", bg="#393e63", fg="#eebbc3", font=("Helvetica", 10, "italic"))
            more_lbl.pack(side=tk.LEFT, padx=7)
            self.preview_labels.append(more_lbl)

    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if 0 <= key <= 255:
                user_config.data['last_key'] = str(key)
                user_config.save()
                return key
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.strings['invalid_key'], self.strings['invalid_key'])
            return None

    def encrypt(self):
        self.process(True)

    def decrypt(self):
        self.process(False)

    def process(self, encrypting):
        if not self.file_paths:
            messagebox.showerror(self.strings['no_file'], self.strings['no_file'])
            return
        key = self.get_key()
        if key is None:
            return
        action = self.strings['encrypt'] if encrypting else self.strings['decrypt']
        suffix = "_encrypted" if encrypting else "_decrypted"
        self.progress['maximum'] = len(self.file_paths)
        self.progress['value'] = 0
        for idx, path in enumerate(self.file_paths):
            base, ext = os.path.splitext(os.path.basename(path))
            output_path = os.path.join(self.output_folder, f"{base}{suffix}{ext}")
            # Warn if file already has suffix
            if (encrypting and base.endswith('_encrypted')) or (not encrypting and base.endswith('_decrypted')):
                messagebox.showwarning(self.strings['already_encrypted'], f"{os.path.basename(path)}\n{self.strings['already_encrypted']}")
            success = process_image(path, output_path, key)
            if success:
                messagebox.showinfo(action, f"{self.strings['output_saved']} {output_path}")
            self.progress['value'] = idx + 1
            self.master.update_idletasks()

    # The old browse_file method is no longer needed. Use browse_files instead, which updates self.file_paths and the preview.

    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if 0 <= key <= 255:
                return key
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Key", "Key must be an integer between 0 and 255.")
            return None

    def encrypt(self):
        self.process(True)

    def decrypt(self):
        self.process(False)

    def process(self, encrypting):
        if not self.file_paths:
            messagebox.showerror(self.strings['no_file'], self.strings['no_file'])
            return
        key = self.get_key()
        if key is None:
            return
        action = self.strings['encrypt'] if encrypting else self.strings['decrypt']
        suffix = "_encrypted" if encrypting else "_decrypted"
        self.progress['maximum'] = len(self.file_paths)
        self.progress['value'] = 0
        for idx, path in enumerate(self.file_paths):
            base, ext = os.path.splitext(os.path.basename(path))
            output_path = os.path.join(self.output_folder, f"{base}{suffix}{ext}")
            # Warn if file already has suffix
            if (encrypting and base.endswith('_encrypted')) or (not encrypting and base.endswith('_decrypted')):
                messagebox.showwarning(self.strings['already_encrypted'], f"{os.path.basename(path)}\n{self.strings['already_encrypted']}")
            success = process_image(path, output_path, key)
            if success:
                messagebox.showinfo(action, f"{self.strings['output_saved']} {output_path}")
            else:
                messagebox.showerror("Error", "Failed to process the image.")
            self.progress['value'] = idx + 1
            self.master.update_idletasks()

def main():
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()

def main():
    import sys
    if DND_AVAILABLE:
        try:
            root = TkinterDnD.Tk()
        except Exception:
            root = tk.Tk()
    else:
        root = tk.Tk()
    # Set full screen (Windows)
    root.state('zoomed')
    # Allow Esc to exit full screen
    def exit_fullscreen(event=None):
        root.state('normal')
    root.bind('<Escape>', exit_fullscreen)
    app = ImageEncryptorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
