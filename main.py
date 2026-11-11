"""
Classical Cipher Lab — Professional Edition
Modern Tkinter interface with button-based algorithm selection.
"""

import importlib.util
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

BASE_DIR = Path(__file__).resolve().parent
CIPHERS_FILE = BASE_DIR / "Ciphers-2.py"

spec = importlib.util.spec_from_file_location("ciphers_backend", CIPHERS_FILE)
if spec is None or spec.loader is None:
    raise ImportError("Could not load Ciphers-2.py")
ciphers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ciphers)


class CipherApp(tk.Tk):
    BG = "#0b1220"
    PANEL = "#111a2e"
    CARD = "#16223a"
    CARD_2 = "#1b2945"
    TEXT = "#f4f7fb"
    MUTED = "#91a0b8"
    ACCENT = "#5b8cff"
    ACCENT_HOVER = "#78a0ff"
    SUCCESS = "#35d399"
    DANGER = "#ff6b7a"
    BORDER = "#263654"

    ALGORITHM_META = {
        "Caesar Cipher": ("01", "CAESAR", "Numeric shift", "Classic substitution"),
        "Additive Cipher": ("02", "ADDITIVE", "Numeric shift", "Additive substitution"),
        "Multiplicative Cipher": ("03", "MULTIPLICATIVE", "Coprime key", "Multiplicative substitution"),
        "Affine Cipher": ("04", "AFFINE", "a, b", "Two-parameter substitution"),
        "Vigenere Cipher": ("05", "VIGENERE", "Keyword", "Polyalphabetic"),
        "Auto-Key Vigenere Cipher": ("06", "AUTO-KEY", "Keyword", "Autokey stream"),
        "Playfair Cipher": ("07", "PLAYFAIR", "Keyword", "Digraph substitution"),
        "Hill Cipher": ("08", "HILL 2×2", "4 numbers", "Matrix cipher"),
        "Keyless Transposition Cipher": ("09", "TRANSPOSITION", "No key", "Reversal transposition"),
    }

    def __init__(self):
        super().__init__()
        self.title("CipherLab Pro — Classical Cryptography Studio")
        self.geometry("1240x820")
        self.minsize(1000, 700)
        self.configure(bg=self.BG)

        self.algorithm_var = tk.StringVar(value="Caesar Cipher")
        self.key_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="Encrypt")
        self.status_var = tk.StringVar(value="Ready • Select a cipher to begin")
        self.key_hint_var = tk.StringVar()
        self.operation_count = 0
        self.history = []
        self._toast_after_id = None
        self._toast_fade_id = None

        self._configure_style()
        self._build_ui()
        self._create_toast()
        self._select_algorithm("Caesar Cipher")
        self.bind("<Control-Return>", lambda e: self.process())
        self.bind("<Control-l>", lambda e: self.clear_all())
        self.bind("<Control-c>", lambda e: self.copy_result())

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TScrollbar", troughcolor=self.PANEL, background=self.CARD_2,
                        bordercolor=self.PANEL, arrowcolor=self.MUTED)
        style.configure("TEntry", fieldbackground=self.CARD_2, foreground=self.TEXT,
                        insertcolor=self.TEXT, bordercolor=self.BORDER, padding=10)
        style.map("TEntry", bordercolor=[("focus", self.ACCENT)])

    def _label(self, parent, text, size=10, bold=False, color=None):
        return tk.Label(parent, text=text, bg=parent.cget("bg"),
                        fg=color or self.TEXT,
                        font=("Segoe UI", size, "bold" if bold else "normal"))

    def _button(self, parent, text, command, bg=None, fg=None, active=None,
                font_size=10, width=None, anchor="center"):
        b = tk.Button(parent, text=text, command=command,
                      bg=bg or self.CARD_2, fg=fg or self.TEXT,
                      activebackground=active or self.ACCENT,
                      activeforeground=self.TEXT, relief="flat", bd=0,
                      highlightthickness=0, cursor="hand2",
                      font=("Segoe UI", font_size, "bold"),
                      padx=12, pady=9, anchor=anchor)
        if width:
            b.config(width=width)
        return b

    def _build_ui(self):
        root = tk.Frame(self, bg=self.BG)
        root.pack(fill="both", expand=True)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Sidebar
        side = tk.Frame(root, bg=self.PANEL, width=285)
        side.grid(row=0, column=0, rowspan=2, sticky="nsew")
        side.grid_propagate(False)

        brand = tk.Frame(side, bg=self.PANEL)
        brand.pack(fill="x", padx=22, pady=(24, 20))
        tk.Label(brand, text="CIPHER", bg=self.PANEL, fg=self.ACCENT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(brand, text="LAB  PRO", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(brand, text="Classical cryptography studio", bg=self.PANEL,
                 fg=self.MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

        tk.Label(side, text="CIPHERS", bg=self.PANEL, fg=self.MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(4, 8))

        self.algorithm_buttons = {}
        list_frame = tk.Frame(side, bg=self.PANEL)
        list_frame.pack(fill="both", expand=True, padx=12)

        for name, meta in self.ALGORITHM_META.items():
            btn = tk.Button(list_frame, text=f"  {meta[0]}   {meta[1]}",
                            command=lambda n=name: self._select_algorithm(n),
                            bg=self.PANEL, fg=self.MUTED, activebackground=self.CARD_2,
                            activeforeground=self.TEXT, relief="flat", bd=0,
                            highlightthickness=0, cursor="hand2",
                            anchor="w", padx=10, pady=8,
                            font=("Segoe UI", 9, "bold"))
            btn.pack(fill="x", pady=2)
            self.algorithm_buttons[name] = btn

        footer = tk.Frame(side, bg=self.PANEL)
        footer.pack(fill="x", padx=22, pady=20)
        tk.Label(footer, text="●  SYSTEM ONLINE", bg=self.PANEL, fg=self.SUCCESS,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(footer, text="Local processing • No network required", bg=self.PANEL,
                 fg=self.MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 0))

        # Header
        header = tk.Frame(root, bg=self.BG)
        header.grid(row=0, column=1, sticky="ew", padx=30, pady=(22, 12))
        header.grid_columnconfigure(0, weight=1)

        h = tk.Frame(header, bg=self.BG)
        h.grid(row=0, column=0, sticky="w")
        tk.Label(h, text="CRYPTOGRAPHY", bg=self.BG, fg=self.ACCENT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(h, text="Encryption Workspace", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 25, "bold")).pack(anchor="w")
        self.selection_label = tk.Label(h, text="", bg=self.BG, fg=self.MUTED,
                                        font=("Segoe UI", 10))
        self.selection_label.pack(anchor="w", pady=(2, 0))

        stats = tk.Frame(header, bg=self.BG)
        stats.grid(row=0, column=1, sticky="e")
        self._stat_card(stats, "CIPHERS", "09", 0)
        self._stat_card(stats, "OPERATIONS", "00", 1)

        # Main content
        content = tk.Frame(root, bg=self.BG)
        content.grid(row=1, column=1, sticky="nsew", padx=30, pady=(0, 25))
        content.grid_rowconfigure(2, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Selected algorithm card
        selected = tk.Frame(content, bg=self.CARD, highlightthickness=1,
                            highlightbackground=self.BORDER)
        selected.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        selected.grid_columnconfigure(1, weight=1)
        self.selected_title = tk.Label(selected, text="", bg=self.CARD, fg=self.TEXT,
                                       font=("Segoe UI", 15, "bold"))
        self.selected_title.grid(row=0, column=0, sticky="w", padx=18, pady=(15, 2))
        self.selected_desc = tk.Label(selected, text="", bg=self.CARD, fg=self.MUTED,
                                      font=("Segoe UI", 9))
        self.selected_desc.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 15))
        self.key_hint = tk.Label(selected, textvariable=self.key_hint_var, bg=self.CARD,
                                 fg=self.ACCENT, font=("Segoe UI", 9, "bold"))
        self.key_hint.grid(row=0, column=1, rowspan=2, sticky="e", padx=18)

        # Controls
        controls = tk.Frame(content, bg=self.BG)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=0)

        key_box = tk.Frame(controls, bg=self.CARD, highlightthickness=1,
                           highlightbackground=self.BORDER)
        key_box.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        tk.Label(key_box, text="KEY / PARAMETERS", bg=self.CARD, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(9, 2))
        self.key_entry = tk.Entry(key_box, textvariable=self.key_var, bg=self.CARD_2,
                                  fg=self.TEXT, insertbackground=self.TEXT, relief="flat",
                                  bd=0, font=("Consolas", 11))
        self.key_entry.pack(fill="x", padx=12, pady=(0, 10), ipady=6)

        op_box = tk.Frame(controls, bg=self.CARD, highlightthickness=1,
                          highlightbackground=self.BORDER)
        op_box.grid(row=0, column=1, sticky="ns")
        tk.Label(op_box, text="OPERATION", bg=self.CARD, fg=self.MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=12, pady=(9, 5))
        ops = tk.Frame(op_box, bg=self.CARD)
        ops.pack(padx=10, pady=(0, 9))
        self.encrypt_btn = self._button(ops, "ENCRYPT", lambda: self._set_mode("Encrypt"),
                                        font_size=9, width=11)
        self.encrypt_btn.pack(side="left", padx=(0, 5))
        self.decrypt_btn = self._button(ops, "DECRYPT", lambda: self._set_mode("Decrypt"),
                                        font_size=9, width=11)
        self.decrypt_btn.pack(side="left")

        # Input/output split
        editor = tk.Frame(content, bg=self.BG)
        editor.grid(row=2, column=0, sticky="nsew")
        editor.grid_columnconfigure(0, weight=1)
        editor.grid_columnconfigure(1, weight=1)
        editor.grid_rowconfigure(1, weight=1)

        self._editor_card(editor, "INPUT", "Plaintext / ciphertext", 0, True)
        self._editor_card(editor, "OUTPUT", "Processed result", 1, False)

        # Actions
        actions = tk.Frame(content, bg=self.BG)
        actions.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self._button(actions, "▶  RUN OPERATION", self.process, self.ACCENT,
                     "white", self.ACCENT_HOVER, 10).pack(side="left")
        self._button(actions, "COPY RESULT", self.copy_result, self.CARD_2,
                     self.TEXT).pack(side="left", padx=7)
        self._button(actions, "SWAP", self.swap_text, self.CARD_2,
                     self.TEXT).pack(side="left", padx=(0, 7))
        self._button(actions, "EXPORT", self.export_result, self.CARD_2,
                     self.TEXT).pack(side="left", padx=(0, 7))
        self._button(actions, "DEMO", self.run_demo, self.CARD_2,
                     self.TEXT).pack(side="left", padx=(0, 7))
        self._button(actions, "ABOUT", self.show_about, self.CARD_2,
                     self.TEXT).pack(side="left")
        tk.Label(actions, textvariable=self.status_var, bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 9)).pack(side="right")

    def _create_toast(self):
        # Small floating notification used for successful clipboard actions.
        self.toast = tk.Frame(self, bg=self.CARD_2, highlightthickness=1,
                              highlightbackground=self.BORDER, bd=0)
        self.toast_icon = tk.Label(self.toast, text="✓", bg=self.CARD_2, fg=self.SUCCESS,
                                   font=("Segoe UI", 13, "bold"))
        self.toast_icon.pack(side="left", padx=(12, 5), pady=8)
        self.toast_text = tk.Label(self.toast, text="Copied ✓", bg=self.CARD_2, fg=self.TEXT,
                                   font=("Segoe UI", 9, "bold"))
        self.toast_text.pack(side="left", padx=(0, 12), pady=8)

    def _show_toast(self, text="Copied ✓"):
        if self._toast_after_id:
            self.after_cancel(self._toast_after_id)
            self._toast_after_id = None
        if self._toast_fade_id:
            self.after_cancel(self._toast_fade_id)
            self._toast_fade_id = None

        self.toast_text.config(text=text)
        self.toast.place(relx=0.97, rely=0.055, anchor="ne")
        self.toast.lift()
        self._toast_after_id = self.after(1700, self._fade_toast)

    def _fade_toast(self):
        # Tkinter does not provide per-widget opacity, so the toast fades by
        # smoothly transitioning its colors toward the application background.
        steps = 8
        self._toast_fade_step(0, steps)

    def _toast_fade_step(self, step, total):
        if step > total:
            self.toast.place_forget()
            self._toast_fade_id = None
            return
        ratio = step / total
        bg = self._blend_hex(self.CARD_2, self.BG, ratio)
        border = self._blend_hex(self.BORDER, self.BG, ratio)
        fg = self._blend_hex(self.TEXT, self.BG, ratio)
        success = self._blend_hex(self.SUCCESS, self.BG, ratio)
        self.toast.config(bg=bg, highlightbackground=border)
        self.toast_icon.config(bg=bg, fg=success)
        self.toast_text.config(bg=bg, fg=fg)
        self._toast_fade_id = self.after(45, lambda: self._toast_fade_step(step + 1, total))

    @staticmethod
    def _blend_hex(first, second, ratio):
        ratio = max(0.0, min(1.0, ratio))
        a = tuple(int(first[i:i+2], 16) for i in (1, 3, 5))
        b = tuple(int(second[i:i+2], 16) for i in (1, 3, 5))
        c = tuple(round(x + (y - x) * ratio) for x, y in zip(a, b))
        return "#%02x%02x%02x" % c

    def _stat_card(self, parent, title, value, col):
        box = tk.Frame(parent, bg=self.CARD, padx=15, pady=8)
        box.grid(row=0, column=col, padx=(8 if col else 0, 0))
        val = tk.Label(box, text=value, bg=self.CARD, fg=self.TEXT,
                       font=("Segoe UI", 14, "bold"))
        val.pack(anchor="e")
        tk.Label(box, text=title, bg=self.CARD, fg=self.MUTED,
                 font=("Segoe UI", 7, "bold")).pack(anchor="e")
        if title == "OPERATIONS":
            self.ops_value = val

    def _editor_card(self, parent, title, subtitle, col, input_side):
        card = tk.Frame(parent, bg=self.CARD, highlightthickness=1,
                        highlightbackground=self.BORDER)
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 6) if col == 0 else (6, 0))
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)
        head = tk.Frame(card, bg=self.CARD)
        head.grid(row=0, column=0, sticky="ew", padx=14, pady=(11, 7))
        tk.Label(head, text=title, bg=self.CARD, fg=self.TEXT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(head, text=subtitle, bg=self.CARD, fg=self.MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(1, 0))
        txt = tk.Text(card, wrap="word", undo=True, bg=self.CARD_2, fg=self.TEXT,
                      insertbackground=self.TEXT, selectbackground=self.ACCENT,
                      relief="flat", bd=0, font=("Consolas", 11), padx=12, pady=12)
        txt.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        sb = ttk.Scrollbar(card, orient="vertical", command=txt.yview)
        sb.grid(row=1, column=1, sticky="ns", pady=(0, 10))
        txt.configure(yscrollcommand=sb.set)
        if input_side:
            self.input_text = txt
        else:
            self.output_text = txt

    def _select_algorithm(self, name):
        self.algorithm_var.set(name)
        meta = self.ALGORITHM_META[name]
        self.selected_title.config(text=f"{meta[1]}  •  {name}")
        self.selected_desc.config(text=meta[3])
        self.key_hint_var.set(ciphers.KEY_HINTS.get(name, "Enter the required key."))
        for n, btn in self.algorithm_buttons.items():
            if n == name:
                btn.config(bg=self.ACCENT, fg="white")
            else:
                btn.config(bg=self.PANEL, fg=self.MUTED)
        if name == "Keyless Transposition Cipher":
            self.key_var.set("")
            self.key_entry.config(state="disabled", disabledbackground=self.CARD_2,
                                  disabledforeground=self.MUTED)
        else:
            self.key_entry.config(state="normal")
        self.status_var.set(f"Selected • {name}")

    def _set_mode(self, mode):
        self.mode_var.set(mode)
        active = self.ACCENT
        inactive = self.CARD_2
        self.encrypt_btn.config(bg=active if mode == "Encrypt" else inactive,
                                fg="white" if mode == "Encrypt" else self.TEXT)
        self.decrypt_btn.config(bg=active if mode == "Decrypt" else inactive,
                                fg="white" if mode == "Decrypt" else self.TEXT)
        self.status_var.set(f"Mode • {mode}")

    def _get_input(self):
        return self.input_text.get("1.0", "end-1c")

    def _set_output(self, value):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", value)

    def process(self):
        text = self._get_input()
        algorithm_name = self.algorithm_var.get()
        key = self.key_var.get().strip()
        decrypt = self.mode_var.get() == "Decrypt"

        if not text.strip():
            messagebox.showwarning("Missing input", "Please enter text to process.")
            return
        if algorithm_name != "Keyless Transposition Cipher" and not key:
            messagebox.showwarning("Missing key", "Please enter the required key.")
            self.key_entry.focus_set()
            return

        try:
            algorithm = ciphers.ALGORITHMS[algorithm_name]
            result = algorithm(text, key, decrypt=decrypt)
            self._set_output(result)
            self.operation_count += 1
            self.ops_value.config(text=f"{self.operation_count:02d}")
            self.history.insert(0, {
                "algorithm": algorithm_name,
                "mode": self.mode_var.get(),
                "input": text,
                "output": result,
            })
            self.history = self.history[:20]
            self.status_var.set(f"Completed • {algorithm_name} • {self.mode_var.get()}")
        except (ValueError, KeyError) as exc:
            self._set_output("")
            self.status_var.set("Operation failed • Check your parameters")
            messagebox.showerror("Invalid parameters", str(exc))
        except Exception as exc:
            self._set_output("")
            self.status_var.set("Unexpected error")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{exc}")

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.key_var.set("")
        self.status_var.set("Ready • Workspace cleared")

    def swap_text(self):
        current_input = self._get_input()
        current_output = self.output_text.get("1.0", "end-1c")
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", current_output)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", current_input)
        self.status_var.set("Swapped • Input and output exchanged")

    def export_result(self):
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            messagebox.showinfo("Nothing to export", "Run an operation first to create a result.")
            return
        path = filedialog.asksaveasfilename(
            title="Export result",
            defaultextension=".txt",
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")],
            initialfile="cipher_result.txt",
        )
        if not path:
            return
        try:
            Path(path).write_text(result, encoding="utf-8")
            self.status_var.set("Exported • Result saved successfully")
            self._show_toast("Saved ✓")
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc))

    def run_demo(self):
        demos = {
            "Caesar Cipher": ("Hello World", "3"),
            "Additive Cipher": ("Hello World", "3"),
            "Multiplicative Cipher": ("Hello World", "5"),
            "Affine Cipher": ("Hello World", "5,8"),
            "Vigenere Cipher": ("Hello World", "KEY"),
            "Auto-Key Vigenere Cipher": ("Hello World", "KEY"),
            "Playfair Cipher": ("HELLO WORLD", "MONARCHY"),
            "Hill Cipher": ("HELP", "3,3,2,5"),
            "Keyless Transposition Cipher": ("Hello World", ""),
        }
        text, key = demos.get(self.algorithm_var.get(), ("Hello World", "3"))
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", text)
        self.key_var.set(key)
        self._set_mode("Encrypt")
        self.process()
        self.status_var.set(f"Demo completed • {self.algorithm_var.get()}")

    def show_about(self):
        win = tk.Toplevel(self)
        win.title("About CipherLab Pro")
        win.geometry("520x470")
        win.resizable(False, False)
        win.configure(bg=self.BG)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="🔐  CIPHERLAB PRO", bg=self.BG, fg=self.ACCENT,
                 font=("Segoe UI", 18, "bold")).pack(pady=(28, 4))
        tk.Label(win, text="Classical Cryptography Studio", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 11, "bold")).pack()
        body = (
            "A local educational application for demonstrating classical\n"
            "encryption and decryption algorithms in a clear, visual way.\n\n"
            "What you can explain in a presentation:\n"
            "• Select an algorithm from the sidebar.\n"
            "• Enter the required key or parameters.\n"
            "• Choose Encrypt or Decrypt.\n"
            "• Run the operation and inspect the result.\n\n"
            "Important: Base64 is encoding, not encryption. Classical ciphers\n"
            "are mainly useful for learning cryptography concepts.\n\n"
            "All processing is performed locally; no network connection is\n"
            "required by this application.\n\n"
            "Student Project Author:\n"
            "Yaqub Ismail Solan (يعقوب إسماعيل صولان)\n"
            "Al-Razi University | Yemen\n"
            "Third-year Engineering Student"
        )
        tk.Label(win, text=body, justify="left", bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 10), padx=28, pady=18).pack(fill="both", expand=True)
        self._button(win, "CLOSE", win.destroy, self.ACCENT, "white", self.ACCENT_HOVER).pack(pady=(0, 25))

    def copy_result(self):
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            messagebox.showinfo("Nothing to copy", "There is no result to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(result)
        self.update()
        self.status_var.set("Copied • Result is now in the clipboard")
        self._show_toast("Copied ✓")


if __name__ == "__main__":
    CipherApp().mainloop()
