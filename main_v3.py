from tkinter import *
from functools import partial
from datetime import date
import re


class Converter:
    def __init__(self):
        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")
        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"
        # Set GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()
        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Convertor",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)
        instructions = "Please enter a temperature below and " \
                       "then press one of the buttons to convert " \
                       "it from centigrade to Fahrenheit."
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "14"))
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.output_label = Label(self.temp_frame, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=3)

        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)
        self.to_celsius_button = Button(self.button_frame,
                                        text="To Degrees C",
                                        bg="#990099",
                                        fg=button_fg, font=button_font, width=12,
                                        command=lambda: self.temp_convert(-459))
        self.to_celsius_button.grid(row=0, column=0, padx=5, pady=5)

        self.to_fahrenheit_button = Button(self.button_frame,
                                           text="To Farenheit",
                                           bg="#009900",
                                           fg=button_fg, font=button_font, width=12,
                                           command=lambda: self.temp_convert(-273))
        self.to_fahrenheit_button.grid(row=0, column=1, padx=5, pady=5)

        self.to_help_button = Button(self.button_frame,
                                     text="Help / Info",
                                     bg="#CC6600",
                                     fg=button_fg,
                                     font=button_font, width=12,
                                     command=lambda: self.to_help())
        self.to_help_button.grid(row=1, column=0, padx=5, pady=5)
        self.to_history_button = Button(self.button_frame,
                                        text="History / Export",
                                        bg="#004C99",
                                        fg=button_fg,
                                        font=button_font, width=12,
                                        state=DISABLED,
                                        command=lambda: self.to_history(self.all_calculations))
        self.to_history_button.grid(row=1, column=1, padx=5, pady=5)

    def check_temp(self, min_value):
        has_error = "no"
        error = f"Please enter a number that is more than {min_value}"
        response = self.temp_entry.get()
        try:

            response = float(response)
            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        else:
            # set to 'no' in case of previous errors
            self.var_has_error.set("no")

            # return number to be
            # converted and enable history button
            self.to_history_button.config(state=NORMAL)
            return response

    @staticmethod
    def round_ans(val):
        var_rounded = (val * 2 + 1) // 2
        return "{:.0f}".format(var_rounded)

    def temp_convert(self, min_val):

        to_convert = self.check_temp(min_val)
        deg_sign = u'\N{DEGREE SIGN}'
        set_feedback = "yes"
        answer = ""
        from_to = ""
        if to_convert == "invalid":
            set_feedback = "no"

        # Convert to Celsius.
        elif min_val == -459:
            # do calculation
            answer = (to_convert - 32) * 5 / 9
            from_to = "{} F{} is {} C{}"
        # convert to Farenheit
        else:
            answer = to_convert * 1.8 + 32
            from_to = "{} C{} is {} F{}"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)
            # create user output and add to calculation history
            feedback = from_to.format(to_convert, deg_sign,
                                      answer, deg_sign)
            self.var_feedback.set(feedback)
            self.all_calculations.append(feedback)

        self.output_answer()

    # Shows user output and clears entry widget
    def output_answer(self):

        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()
        if has_errors == "yes":
            # red text, pink entry box
            self.output_label.config(fg="#9C0000")

            self.temp_entry.config(bg="#F8CECC")
        else:
            self.output_label.config(fg="#004C00")

            self.temp_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)

    # Opens Help / Info dialogue box
    def to_help(self):
        DisplayHelp(self)

    def to_history(self, all_calculations):
        HistoryExport(self, all_calculations)


class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()
        # disable help button
        partner.to_help_button.config(state=DISABLED)
        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE WINDOW',
                               partial(self.close_help, partner))
        self.help_frame = Frame(self.help_box, width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()
        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)
        help_text = ("To use the program, simply enter the temperature "
                     "you wish to convert and then choose to convert "
                     "to either degrees Celsius (centigrade) or "
                     "Fahrenheit.. \n\n"
                     "Note that -273 degrees C "
                     "(-459 F) is absolute zero (the coldest possible "
                     'temperature). If you try to convert a '
                     'temperature that is less than -273 degrees C,'
                     "you will get an error message. \n\n "
                     "To see your "
                     "calculation history and export it to a text "
                     "file, please click the 'History / Export' button")

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wrap=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))

        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


class HistoryExport:
    def __init__(self, partner, calc_list):
        max_calcs = 5
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()
        # Function converts contents of calculation list
        # into a string.
        calc_string_text = self.get_calc_string(calc_list)

        # setup dialogue box and background colour
        self.history_box = Toplevel()
        # disable help button
        partner.to_history_button.config(state=DISABLED)
        # If users press cross at top, closes help and
        # 'releases' help button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))
        self.history_frame = Frame(self.history_box, width=300,
                                   height=200)

        self.history_frame.grid()
        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Arial", "16", "bold"))
        self.history_heading_label.grid(row=0)
        # History text and label
        num_calcs = len(calc_list)
        if num_calcs > max_calcs:
            calc_background = "#FFE6CC"  # peach
            showing_all = "Here are your recent calculations " \
                          "({}/{} calculations shown). Please export your" \
                          "calculations to see your full calculation " \
                          "history".format(max_calcs, num_calcs)

        else:
            calc_background = "#B4FACB"  # pale green
            showing_all = "Below is your calculation history."

        # History text and label
        hist_text = f"{showing_all} \n\nAll calculations are shown to the nearest degree"
        self.text_instructions_label = Label(self.history_frame,
                                             text=hist_text,
                                             width=45, justify="left",
                                             wraplength=300,
                                             padx=10, pady=10)
        self.text_instructions_label.grid(row=1)

        self.all_calcs_label = Label(self.history_frame,
                                     text=calc_string_text,
                                     padx=10, pady=10, bg=calc_background,
                                     width=40, justify="left")
        self.all_calcs_label.grid(row=2)

        save_text = "Either choose a custom file name (and push " \
                    "<Export>) or simply push <Export> to save your " \
                    "calculations in a text file. If the " \
                    "filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.history_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        # Filename entry widget, white background to start
        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#ffffff", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)
        self.filename_feedback_label = Label(self.history_frame,
                                             text="",
                                             fg="#9C0000",
                                             wraplength=300,
                                             font=("Arial", "12", "bold"))
        self.filename_feedback_label.grid(row=5)
        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)
        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)
        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#666666",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_history, partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)
        # closes help dialogue (used by button and x at top of dialogue)

    def get_calc_string(self, var_calculations):
        # get maximum calculations to display
        # (was set in __init__ function)
        max_calcs = self.var_max_calcs.get()
        calc_string = ""
        oldest_first = ""
        for item in var_calculations:
            oldest_first += item
            oldest_first += "\n"
        self.var_calc_list.set(oldest_first)
        # work out how many times we need to loop
        # to output either the last five calculations
        # or all the calculations
        if len(var_calculations) >= max_calcs:
            stop = max_calcs

        else:
            stop = len(var_calculations)
            # iterate to all but last item,
            # adding item and line break to calculation string
        for item in range(0, stop):
            calc_string += var_calculations[len(var_calculations)
                                            - item - 1]

            calc_string += "\n"

        calc_string = calc_string.strip()

        return calc_string

    def make_file(self):
        # retrieve filename
        filename = self.filename_entry.get()
        filename_ok = ""
        date_part = self.get_date()
        if filename == "":
            # get date and create default filename
            filename = f"{date_part}_temperature_calculations"

        else:
            # check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = "Success! Your calculation history has been saved as {}".format(filename)
            self.var_filename.set(filename)
            self.filename_feedback_label.config(text=success,
                                                fg="dark green")
            self.filename_entry.config(bg="#FFFFFF")
            self.write_to_file()
        else:
            self.filename_feedback_label.config(text=filename_ok,
                                                fg="dark red")
            self.filename_feedback_label.config(bg="#F8CECC")

    def get_date(self):

        today = date.today()
        day = today.strftime("%d")
        month = today.strftime('%m')
        year = today.strftime("%Y")
        todays_date = f"{day}/{month}/{year}"
        self.var_todays_date.set(todays_date)
        return f"{year}_{month}_{day}"

    @staticmethod
    def check_filename(filename):

        problem = ""
        # Regular expression to check filname is valid
        valid_char = "[A-Za-z0-9_]"
        # iterates through filename and checks each letter.
        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed. "
            else:
                problem = ("Sorry, no {}'s allowed. ".format(letter))
            break
        if problem != "":
            problem = "{} Use letters / numbers / underscores only.".format(problem)
        return problem

    def write_to_file(self):

        # retrieve date, filename and calculation history..
        filename = self.var_filename.get()
        generated_date = self.var_todays_date.get()
        # set up strings to be written to file
        heading = '**** Temperature Calculations ****'
        generated = "Generated: {}\n".format(generated_date)
        sub_heading = "Here is your calculation" \
                      "(oldest to newest)...\n"
        all_calculations = self.var_calc_list.get()

        to_output_list = [heading, generated,
                          sub_heading,
                          all_calculations]
        text_file = open(filename, "w+")
        for item in to_output_list:
            text_file.write(item)
            text_file.write("\n")
        # close file
        text_file.close()

    def close_history(self, partner):
        # Put help button back to normal...
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
