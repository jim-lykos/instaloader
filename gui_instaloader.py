"""Simple GUI for Instaloader.

This script provides a minimal Tkinter-based graphical interface to log in to
Instagram and download a profile using Instaloader.

The user can enter Instagram credentials, choose a target profile and a local
folder where the downloads should be stored. The download is performed when the
"Download" button is pressed.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

import instaloader


class InstaloaderGUI:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Instaloader GUI")

        # Username
        tk.Label(master, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        tk.Label(master, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_entry = tk.Entry(master, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Profile to download
        tk.Label(master, text="Profile:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.profile_entry = tk.Entry(master, width=30)
        self.profile_entry.grid(row=2, column=1, padx=5, pady=5)

        # Download directory selection
        tk.Label(master, text="Download directory:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.dir_var = tk.StringVar()
        self.dir_entry = tk.Entry(master, textvariable=self.dir_var, width=30)
        self.dir_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse...", command=self.browse_dir).grid(row=3, column=2, padx=5, pady=5)

        # Download button
        tk.Button(master, text="Download", command=self.download).grid(row=4, column=1, pady=10)

    def browse_dir(self) -> None:
        directory = filedialog.askdirectory(title="Select Download Directory")
        if directory:
            self.dir_var.set(directory)

    def download(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        profile = self.profile_entry.get().strip()
        directory = self.dir_var.get().strip()

        if not all([username, password, profile, directory]):
            messagebox.showerror("Missing Information", "Please fill in all fields.")
            return

        try:
            os.makedirs(directory, exist_ok=True)
            loader = instaloader.Instaloader(dirname_pattern=os.path.join(directory, "{target}"))
            loader.login(username, password)
            loader.download_profiles({profile}, profile_pic=True)
            messagebox.showinfo("Success", f"Download completed in {directory}.")
        except Exception as exc:  # pragma: no cover - GUI usage only
            messagebox.showerror("Error", f"An error occurred: {exc}")


def main() -> None:
    root = tk.Tk()
    InstaloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
