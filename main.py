import tkinter as tk
import re
import sys

DEFAULTBG = "black"
BLANKIMG = '''
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=
'''

upperRegex = re.compile(r"^(?=.*?[A-Z])")
lowerRegex = re.compile(r"^(?=.*?[a-z])")
onedigitRegex = re.compile(r"[0-9]+")


class MainApplication(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        master.title("Password Checker")
        master.geometry("700x300")
        master.resizable(width=False, height=False)
        master.tk.call('wm', 'iconphoto', master._w, tk.PhotoImage(file='logo.png'))

        self._frame = None
        self.switch_frame(MenuPage)

        self.password_length = 3

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class MenuPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        start_label = tk.Label(
            self, text="Password Checker\n", font=(None, 24)
        )
        start_label.grid(row=0, column=0, sticky=tk.NSEW)

        start_button = tk.Button(
            self, text="Check Password",
            command=lambda: master.switch_frame(MainPage)
        )
        start_button.grid(row=1, column=0, sticky=tk.NSEW)

        credits_button = tk.Button(
            self, text="Configure Parameters",
            command=lambda: master.switch_frame(SettingsPage)
        )
        credits_button.grid(row=2, column=0, sticky=tk.NSEW)

        quit_button = tk.Button(
            self, text="Quit",
            command=lambda: sys.exit())

        quit_button.grid(row=3, column=0, sticky=tk.NSEW)


class SettingsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame_1 = tk.Frame(self)
        passwordlen_label = tk.Label(frame_1, text="\nLength of Password:", font=("", 12))
        passwordlen_label.pack(side=tk.LEFT, fill=tk.BOTH)

        passwordlen_scale = tk.Scale(frame_1, from_=3, to=30, orient=tk.HORIZONTAL)
        passwordlen_scale.pack()
        frame_1.grid(pady=10)

        end_frame = tk.Frame(self)
        save_button = tk.Button(
            end_frame, text="Save", command=lambda: self.save_settings(master, passwordlen_scale.get())
        )
        save_button.pack(side=tk.LEFT)

        back_button = tk.Button(
            end_frame, text="Back", command=lambda: master.switch_frame(MenuPage)
        )
        back_button.pack(side=tk.RIGHT)
        end_frame.grid()

    def save_settings(self, master, length):
        master.password_length = length
        master.switch_frame(MenuPage)


class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.i = tk.PhotoImage(data=BLANKIMG)
        self.image1 = tk.Label(
            self, image=self.i, width=50, height=50, relief=tk.SOLID, bg=DEFAULTBG
        )
        self.image1.grid(column=0, row=0, padx=10, pady=10)

        text1 = tk.Label(
            self, text="Password contains more than {} characters".format(master.password_length)
        )
        text1.grid(column=1, row=0, sticky=tk.W)

        self.image2 = tk.Label(
            self, image=self.i, width=50, height=50, relief=tk.SOLID, bg=DEFAULTBG
        )
        self.image2.grid(column=0, row=1, padx=10, pady=10)

        text2 = tk.Label(
            self, text="Password has at least 1 uppercase and lowercase character"
        )
        text2.grid(column=1, row=1, sticky=tk.W)

        self.image3 = tk.Label(
            self, image=self.i, width=50, height=50, relief=tk.SOLID, bg=DEFAULTBG
        )
        self.image3.grid(column=0, row=2, padx=10, pady=10)

        text3 = tk.Label(self, text="Password has at least 1 digit")
        text3.grid(column=1, row=2, sticky=tk.W)

        text4 = tk.Label(self, text="Enter a password: ")
        text4.grid(column=0, row=3, padx=10, sticky=tk.W, columnspan=1)

        self.entry1 = tk.Entry(self, width=48)
        self.entry1.grid(column=1, row=3, sticky=tk.W)

        button1 = tk.Button(
            self, text="Submit",
            command=lambda: self.checkPass(master, self.entry1.get())
        )
        button1.grid(column=2, row=3, sticky=tk.W)

        button2 = tk.Button(
            self, text="Back",
            command=lambda: master.switch_frame(MenuPage)
        )
        button2.grid(column=0, row=4, pady=10)

    def checkPass(self, master, text):
        if len(text) > master.password_length:
            self.image1.configure(bg="green")
        else:
            self.image1.configure(bg="red")
        if upperRegex.search(text) is None or lowerRegex.search(text) is None:
            self.image2.configure(bg="red")
        else:
            self.image2.configure(bg="green")
        if onedigitRegex.search(text) is None:
            self.image3.configure(bg="red")
        else:
            self.image3.configure(bg="green")


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).grid()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
