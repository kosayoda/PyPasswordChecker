import tkinter as tk
import re
import sys

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
        master.title("PyPasswordChecker")
        master.tk.call('wm', 'iconphoto', master._w, tk.PhotoImage(file='assets/logo.png'))
        master.geometry("700x300")
        master.resizable(width=False, height=False)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        self._frame = None
        self.switch_frame(MenuPage)

        self.password_length = 3
        self.password_case = True
        self.password_digit = True

    def casecolor(self):
        return "red" if self.password_case else "black"

    def digitcolor(self):
        return "red" if self.password_digit else "black"

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class MenuPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.logo = tk.PhotoImage(file='assets/logo_small.png')
        start_label = tk.Label(
            self, text="PyPasswordChecker", font=(None, 24),
            image=self.logo,
            compound=tk.RIGHT
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

        self.passwordlen_var = tk.IntVar()
        self.passwordlen_var.set(master.password_length)
        self.passwordcase_var = tk.BooleanVar()
        self.passwordcase_var.set(master.password_case)
        self.passworddigit_var = tk.BooleanVar()
        self.passworddigit_var.set(master.password_digit)

        frame_1 = tk.Frame(self)
        passwordlen_label = tk.Label(frame_1, text="\nMinimum Password Length:", font=("", 11))
        passwordlen_label.pack(side=tk.LEFT, fill=tk.BOTH)

        self.passwordlen_scale = tk.Scale(
            frame_1, from_=3, to=30, orient=tk.HORIZONTAL,
            variable=self.passwordlen_var
        )
        self.passwordlen_scale.pack()
        frame_1.grid()

        frame_2 = tk.Frame(self)
        self.passwordcase_checkbutton = tk.Checkbutton(
            frame_2, text="Require Uppercase & Lowercase Characters",
            variable=self.passwordcase_var
        )
        self.passwordcase_checkbutton.pack()
        self.passworddigit_checkbutton = tk.Checkbutton(
            frame_2, text="Require a Digit",
            variable=self.passworddigit_var
        )
        self.passworddigit_checkbutton.pack(anchor=tk.W)
        frame_2.grid(pady=10)

        end_frame = tk.Frame(self)
        save_button = tk.Button(
            end_frame, text="Save",
            command=lambda: self.save_settings(
                master, self.passwordlen_scale.get(),
                self.passwordcase_var.get(),
                self.passworddigit_var.get()
            )
        )
        save_button.pack(side=tk.LEFT)

        back_button = tk.Button(
            end_frame, text="Back", command=lambda: master.switch_frame(MenuPage)
        )
        back_button.pack(side=tk.RIGHT)
        end_frame.grid()

    def save_settings(self, master, length, casevar, digitvar):
        master.password_length = length
        master.password_case = casevar
        master.password_digit = digitvar
        master.switch_frame(MenuPage)


class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.i = tk.PhotoImage(data=BLANKIMG)

        self.passwordlen_image = tk.Label(
            self, image=self.i, width=50, height=50, relief=tk.SOLID, bg="red"
        )
        self.passwordlen_image.grid(column=0, row=0, padx=10, pady=10)

        passwordlen_text = tk.Label(
            self, text="Password contains more than {} characters".format(master.password_length)
        )
        passwordlen_text.grid(column=1, row=0, sticky=tk.W)

        self.passwordcase_image = tk.Label(
            self, image=self.i, width=50, height=50, relief=tk.SOLID, bg=master.casecolor()
        )
        self.passwordcase_image.grid(column=0, row=1, padx=10, pady=10)

        passwordcase_text = tk.Label(
            self, text="Password has at least 1 uppercase and lowercase character"
        )
        passwordcase_text.grid(column=1, row=1, sticky=tk.W)

        self.passworddigit_image = tk.Label(
            self, image=self.i, width=50, height=50, relief=tk.SOLID, bg=master.digitcolor()
        )
        self.passworddigit_image.grid(column=0, row=2, padx=10, pady=10)

        passworddigit_text = tk.Label(self, text="Password has at least 1 digit")
        passworddigit_text.grid(column=1, row=2, sticky=tk.W)

        enter_text = tk.Label(self, text="Enter a password: ")
        enter_text.grid(column=0, row=3, padx=10, sticky=tk.W, columnspan=1)

        self.password_entry = tk.Entry(self, width=48)
        self.password_entry.grid(column=1, row=3, sticky=tk.W)

        submit_button = tk.Button(
            self, text="Check",
            command=lambda: self.checkPass(master, self.password_entry.get())
        )
        submit_button.grid(column=2, row=3, sticky=tk.W)

        back_button = tk.Button(
            self, text="Back",
            command=lambda: master.switch_frame(MenuPage)
        )
        back_button.grid(column=0, row=4, pady=10)

        legend_frame = tk.Frame(self)

        legend_text1 = tk.Label(legend_frame, text="Legend:", font=("", 11))
        legend_text1.pack(side=tk.LEFT)
        tk.Label(legend_frame, text="|", font=("", 11), padx=10).pack(side=tk.LEFT)

        legend_text2 = tk.Label(
            legend_frame, text="Match", font=("", 11), fg="green"
        )
        legend_text2.pack(side=tk.LEFT)
        tk.Label(legend_frame, text="|", font=("", 11), padx=10).pack(side=tk.LEFT)

        legend_text3 = tk.Label(
            legend_frame, text="Does not Match", font=("", 11), fg="red"
        )
        legend_text3.pack(side=tk.LEFT)
        tk.Label(legend_frame, text="|", font=("", 11), padx=10).pack(side=tk.LEFT)

        legend_text4 = tk.Label(
            legend_frame, text="Disabled", font=("", 11)
        )
        legend_text4.pack(side=tk.LEFT)
        legend_frame.grid(column=1, row=4, sticky=tk.W)

    def checkPass(self, master, text):
        if len(text) > master.password_length:
            self.passwordlen_image.configure(bg="green")
        else:
            self.passwordlen_image.configure(bg="red")

        if not master.password_case:
            self.passwordcase_image.configure(bg="black")
        elif upperRegex.search(text) is None or lowerRegex.search(text) is None:
            self.passwordcase_image.configure(bg="red")
        else:
            self.passwordcase_image.configure(bg="green")

        if not master.password_digit:
            self.passworddigit_image.configure(bg="black")
        elif onedigitRegex.search(text) is None:
            self.passworddigit_image.configure(bg="red")
        else:
            self.passworddigit_image.configure(bg="green")


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).grid()
    root.mainloop()
