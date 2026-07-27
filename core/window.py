import tkinter as tk


class AppWindow:

    def __init__(self, root, title="Window", width=700, height=450):

        self.root = root
        self.maximized = False

        self.old_x = 200
        self.old_y = 100
        self.old_w = width
        self.old_h = height

        self.window = tk.Frame(
            root,
            bg="#2B2B2B",
            highlightbackground="#555555",
            highlightthickness=1
        )

        self.window.place(
            x=self.old_x,
            y=self.old_y,
            width=width,
            height=height
        )

        self.window.lift()

        # ==========================
        # Title Bar
        # ==========================

        self.titlebar = tk.Frame(
            self.window,
            bg="#181818",
            height=35
        )

        self.titlebar.pack(fill="x")

        self.title = tk.Label(
            self.titlebar,
            text=title,
            bg="#181818",
            fg="white",
            font=("Segoe UI", 10, "bold")
        )

        self.title.pack(side="left", padx=10)

        # Buttons

        self.close_btn = tk.Button(
            self.titlebar,
            text="✕",
            bg="#D32F2F",
            fg="white",
            bd=0,
            width=4,
            command=self.window.destroy
        )

        self.close_btn.pack(side="right")

        self.max_btn = tk.Button(
            self.titlebar,
            text="□",
            bg="#404040",
            fg="white",
            bd=0,
            width=4,
            command=self.toggle_maximize
        )

        self.max_btn.pack(side="right")

        self.min_btn = tk.Button(
            self.titlebar,
            text="—",
            bg="#404040",
            fg="white",
            bd=0,
            width=4,
            command=self.minimize
        )

        self.min_btn.pack(side="right")

        # ==========================
        # Content
        # ==========================

        self.content = tk.Frame(
            self.window,
            bg="#303030"
        )

        self.content.pack(fill="both", expand=True)

        # Drag Support

        self.titlebar.bind("<Button-1>", self.start_move)
        self.titlebar.bind("<B1-Motion>", self.move)

    # ------------------------

    def start_move(self, event):

        if self.maximized:
            return

        self.window.lift()

        self.start_x = event.x
        self.start_y = event.y

    # ------------------------

    def move(self, event):

        if self.maximized:
            return

        x = self.window.winfo_x() + event.x - self.start_x
        y = self.window.winfo_y() + event.y - self.start_y

        self.window.place(x=x, y=y)

    # ------------------------

    def minimize(self):

        self.window.place_forget()

    # ------------------------

    def restore(self):

        self.window.place(
            x=self.old_x,
            y=self.old_y,
            width=self.old_w,
            height=self.old_h
        )

    # ------------------------

    def toggle_maximize(self):

        if not self.maximized:

            self.old_x = self.window.winfo_x()
            self.old_y = self.window.winfo_y()
            self.old_w = self.window.winfo_width()
            self.old_h = self.window.winfo_height()

            self.root.update_idletasks()

            self.window.place(
                x=0,
                y=0,
                width=self.root.winfo_width(),
                height=self.root.winfo_height() - 45
            )

            self.maximized = True

        else:

            self.restore()

            self.maximized = False