from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
from tkinter import ttk
import os, sys, pathlib


def get_resource_path(package, path):
    d = os.path.dirname(sys.modules[package].__file__)
    return os.path.join(pathlib.Path(d), pathlib.Path(path))

class NumericEntry(Entry):
    """
    Numeric entry are a class of value entries which do not allow non-numeric values to be entered
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.configure(validate='all', validatecommand=(self.register(self._numeric_validator), "%P"))

    @staticmethod
    def _numeric_validator(value):
        """
        Verifies that the value is a valid floating point number
        :param value: String value to be checked
        :return: True if valid otherwise false
        """
        if value == '':
            # Allow complete deletion
            return True
        try:
            float(value)
            return True
        except ValueError:
            # If conversion fails then the value is not a valid float
            return False


class Main:
    def __init__(self, parent):
        self.myParent = parent
        self.myParent.title("five-timer")
        # self.myParent.resizable(width=0, height=0)

        self.label_config = {
            "bg": "#303030",
            "fg": "#d9d9d9",
            "font": ("sans-serif", 10, "bold")
        }

        self.input_config = {
            "bg": "#303030",
            "fg": "white",
            "font": ("sans-serif", 10),
            "width": 10,
            "relief": FLAT
        }

        self.button_config = {
            "bg": "#4a4a4a",
            "relief": FLAT,
        }

        self.myParent.config(bg="#303030")

        # resistor range dictionary
        self.resistor_range = {
            "Ohms": 1,
            "K": 1000,
            "M": 1000000
        }

        # capacitor range dictionary
        self.capacitor_range = {
            "F": 1,
            "mF": 0.001,
            "uF": 0.000001,
            "nF": 0.000000001,
            "pf": 0.000000000001
        }

         # ==============MENU========================================================
        menubar = Menu(self.myParent)
        menu_graph = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=menu_graph, label="nomographs")  
        menu_graph.add_command(label="monostable", command=self.open_monostable_nomograph)
        menu_graph.add_command(label="astable", command=self.open_astable_nomograph)

        pinout_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=pinout_menu, label="pinout")
        pinout_menu.add_command(label="IC pinout", command=self.open_pinout)

        circuits_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=circuits_menu, label="circuits")
        circuits_menu.add_command(label="monostable", command =  self.open_monostable_circuit)
        circuits_menu.add_command(label="astable",command =  self.open_astable_circuit)

        self.myParent['menu'] = menubar

        # frames
        self.frame1 = Frame(self.myParent, bg="#303030")

        # frame 1
        Label(self.frame1, self.label_config, text="Monostable mode", font=("bold")).grid(row=0, column=1)

        self.monostable_resistor = Label(self.frame1, self.label_config, text="R1:")
        self.monostable_resistor.config(width=2)
        self.monostable_resistor.grid(row=2, column=0, pady=5, sticky="E")

        # Choose resistor range
        self.r_combo = ttk.Combobox(self.frame1, state="readonly", values=["Ohms", "K", "M"])
        self.r_combo.current(0)
        self.r_combo.configure(background="#4a4a4a", width=5)
        self.r_combo.grid(row=2, column=2, pady=5, sticky="W")

        self.monostable_capacitor = Label(self.frame1, self.label_config, text="C1:")
        self.monostable_capacitor.grid(row=3, column=0, pady=5, sticky="E")

        # Choose capacitor range
        self.mono_cap_combo = ttk.Combobox(self.frame1, state="readonly", values=["F", "mF", "uF", "nF", "pF"])
        self.mono_cap_combo.current(0)
        self.mono_cap_combo.config(background="#4a4a4a", width=5)
        self.mono_cap_combo.grid(row=3, column=2, pady=5, sticky="W")

        # R1 entry 
        self.monostable_resistor_entry = NumericEntry(self.frame1)
        self.monostable_resistor_entry.config(self.input_config)
        self.monostable_resistor_entry.focus_set()        
        self.monostable_resistor_entry.grid(row=2, column=1, pady=5)

        # C1 entry
        self.monostable_capacitor_entry = NumericEntry(self.frame1)
        self.monostable_capacitor_entry.config(self.input_config)
        self.monostable_capacitor_entry.grid(row=3, column=1, pady=5)

        # calculate button
        self.mono_calculate = Button(self.frame1, self.button_config, text="calculate", command=self.monostable)
        self.mono_calculate.grid(row=4, column=1)

        # Display the time on
        self.mono_high_time = Label(self.frame1, self.label_config, text="time on:")
        self.mono_high_time.grid(row=5, column=0)

        self.monostable_time_on = Entry(self.frame1, self.input_config)
        self.monostable_time_on.grid(row=5, column=1, pady=5)

        self.frame1.grid(column=0, row=0)

        # end of frame1
    
        # frame 3
        self.frame3 = Frame(self.myParent, background="#303030")
        
        Label(self.frame3, self.label_config, text="Astable mode", font=("bold")).grid(row=1, column=1)
        self.astable_resistor_one = Label(self.frame3, self.label_config, text="R1:")
        self.astable_resistor_one.grid(row=2, column=0, sticky="E", pady=5)

        # Choose resistor one range
        self.r1_combo = ttk.Combobox(self.frame3, state="readonly", values=["Ohms", "K", "M"])
        self.r1_combo.current(0)
        self.r1_combo.config(width=5)
        self.r1_combo.grid(row="2", column="2", sticky="W", pady=5)

        # resistor two label
        self.astable_resistor_two = Label(self.frame3, self.label_config, text="R2:")
        self.astable_resistor_two.grid(row=3, column=0, sticky="E", pady=5)

        # Choose resistor two range
        self.r2_combo = ttk.Combobox(self.frame3, state="readonly", values=["Ohms", "K", "M"])
        self.r2_combo.current(0)
        self.r2_combo.config(width=5)
        self.r2_combo.grid(row=3, column=2, pady=5)

        # astable mode capacitor values
        self.astable_capacitor = Label(self.frame3, self.label_config, text="C:")
        self.astable_capacitor.grid(row=4, column=0, sticky="E", pady=5)

        # R1 entry 
        self.astable_resistor_one_entry = NumericEntry(self.frame3)
        self.astable_resistor_one_entry.configure(self.input_config)
        self.astable_resistor_one_entry.grid(row=2, column=1, pady=5)

        # R2 entry 
        self.astable_resistor_two_entry = NumericEntry(self.frame3)
        self.astable_resistor_two_entry.configure(self.input_config)
        self.astable_resistor_two_entry.grid(row=3, column=1, pady=5)

        # C1 entry
        self.astable_capacitor_entry = NumericEntry(self.frame3)
        self.astable_capacitor_entry.configure(self.input_config)
        self.astable_capacitor_entry.grid(row=4, column=1, pady=5)

        # Choose capacitor range
        self.ast_cap_combo = ttk.Combobox(self.frame3, state="readonly", values=["F", "mF", "uF", "nF", "pF"])
        self.ast_cap_combo.current(0)
        self.ast_cap_combo.configure(background="#4a4a4a", width=5)
        self.ast_cap_combo.grid(row="4", column="2", sticky="W", pady=5)

        # calculate button
        self.ast_calculate = Button(self.frame3, self.button_config, text="Calculate", command=self.astable)
        self.ast_calculate.grid(row=5, column=1, pady=5)

        # outputs
        # Display the frequency
        self.ast_freq = Label(self.frame3, self.label_config, text="Frequency:")
        self.ast_freq.grid(row=7, column=0, pady=5)

        self.astable_frequency = Entry(self.frame3, self.input_config)
        self.astable_frequency.grid(row=7, column=1, pady=5)

        # display the period
        self.ast_period = Label(self.frame3, self.label_config, text="Period: ")
        self.ast_period.grid(row=8, column=0, pady=5)

        self.astable_period = Entry(self.frame3, self.input_config)
        self.astable_period.grid(row=8, column=1, pady=5)

        # display the duty cycle
        self.ast_duty = Label(self.frame3, self.label_config, text="Duty Cycle:")
        self.ast_duty.grid(row=9, column=0, pady=5)

        self.astable_duty = Entry(self.frame3, self.input_config)
        self.astable_duty.grid(row=9, column=1, pady=5)

        # display the time high 
        self.ast_time_high = Label(self.frame3, self.label_config, text="Time High: ")
        self.ast_time_high.grid(row=10, column=0, pady=5)

        self.astable_time_high = Entry(self.frame3, self.input_config)
        self.astable_time_high.grid(row=10, column=1, pady=5)

        # display the time low 
        self.ast_time_low = Label(self.frame3, self.label_config, text="Time Low: ")
        self.ast_time_low.grid(row=11, column=0, pady=5)

        self.astable_time_low = Entry(self.frame3, self.input_config)
        self.astable_time_low.grid(row=11, column=1, pady=5)

        self.frame3.grid(column=0, row=1, pady=5)

    def open_monostable_nomograph(self):
        """Open monostable nomograph from the 555 timer datasheet"""
        graph = Toplevel(self.myParent)
        graph.title('monostable nomograph')

        free_graph = ImageTk.PhotoImage(Image.open(get_resource_path("five_timer", "resources/monostable_nomograph.gif")))
        graph_label = Label(graph, image=free_graph)
        graph_label.image = free_graph
        graph_label.grid(row=1, column=0, padx=10)

    def open_astable_nomograph(self):
        """Open astable nomograph from the 555 timer datasheet"""
        graph = Toplevel(self.myParent)
        graph.title('astable nomograph')

        free_graph = ImageTk.PhotoImage(Image.open(get_resource_path("five_timer", "resources/monostable_nomograph.gif")))
        graph_label = Label(graph, image=free_graph)
        graph_label.image = free_graph
        graph_label.grid(row=1, column=0, padx=10)

    def open_pinout(self):
        """Open astable nomograph from the 555 timer datasheet"""
        graph = Toplevel(self.myParent)
        graph.title('astable nomograph')

        pinout = ImageTk.PhotoImage(Image.open(get_resource_path("five_timer", "resources/pinout.png")))
        pinout_label = Label(graph, image=pinout)
        pinout_label.image = pinout
        pinout_label.grid(row=1, column=0, padx=10)

    def open_monostable_circuit(self):
        """Open astable nomograph from the 555 timer datasheet"""
        graph = Toplevel(self.myParent)
        graph.title('Monostable circuit')

        monostable_circuit = ImageTk.PhotoImage(Image.open(get_resource_path("five_timer", "resources/monostable_circuit.gif")))
        monostable_circuit_label = Label(graph, image=monostable_circuit)
        monostable_circuit_label.image = monostable_circuit
        monostable_circuit_label.grid(row=1, column=0, padx=10)

    def open_astable_circuit(self):
        """Open astable nomograph from the 555 timer datasheet"""
        graph = Toplevel(self.myParent)
        graph.title('Astable circuit')

        astable_circuit = ImageTk.PhotoImage(Image.open(get_resource_path("five_timer", "resources/astable_circuit.gif")))
        astable_circuit_label = Label(graph, image=astable_circuit)
        astable_circuit_label.image = astable_circuit
        astable_circuit_label.grid(row=1, column=0, padx=10)

    def monostable(self):
        """
        Calculate the time on for the monostable mode
        Return: Time High
        """

        # clear the previously calculated value
        self.monostable_time_on.delete(0, END)

        resistance = self.monostable_resistor_entry.get()
        capacitance = self.monostable_capacitor_entry.get()

        # check for empty entries
        if len(resistance) == 0:
            showwarning(title="Error", message="Resistor value required")

        elif len(capacitance) == 0:
            showwarning(title="Error", message="Capacitor value required")
        else:
            # calculate frequency
            resistance = eval(self.monostable_resistor_entry.get())

            # get the resistor range chosen
            res_range = self.r_combo.get()
            resistance *= self.resistor_range[res_range]

            capacitance = eval(self.monostable_capacitor_entry.get())

            # get the capacitor range chosen
            cap_range = self.mono_cap_combo.get()
            capacitance *= self.capacitor_range[cap_range]
            time_on = 1.1 * resistance * capacitance
            time_on = round(time_on, 4) # round to 4 decimal places

            final_time_on = str(time_on) + " s"
            self.monostable_time_on.insert(0, final_time_on)

    def astable(self):
        """Calculate the values from the astable mode"""

        # get the current entered values
        resistance_one = self.astable_resistor_one_entry.get()
        resistance_two = self.astable_resistor_two_entry.get()
        capacitor = self.astable_capacitor_entry.get()

        # check for empty entries
        if len(resistance_one) == 0:
            showwarning(title="Error", message="R1 value required")

        elif len(resistance_two) == 0:
            showwarning(title="Error", message="R2 value required")

        elif len(capacitor) == 0:
            showwarning(title="Error", message="C required")

        else:
            # if no error detected, process the inputs

            resistance_one = eval(resistance_one)
            resistance_two = eval(resistance_two)
            capacitor = eval(capacitor)

            # get the ranges chosen
            r1_range = self.r1_combo.get()
            r2_range = self.r2_combo.get()
            cap_range = self.ast_cap_combo.get()

            resistance_one *= self.resistor_range[r1_range]
            resistance_two *= self.resistor_range[r2_range]
            capacitor *= self.capacitor_range[cap_range]

            # frequency
            raw_frequency = 1.44 / (float(resistance_one) + 2 * float(resistance_two)) * float(capacitor)


            frequency = str(raw_frequency) + " Hz"
            # todo: convert frequency to engineering notation

            # period == reciprocal of frequency
            raw_period = 1 / raw_frequency
            raw_period = round(raw_period, 4)
            period = str(raw_period) + " s"

            # high time -> charge time
            raw_high_time = 0.693 * (resistance_one + resistance_two) * capacitor
            raw_high_time = round(raw_high_time, 4)
            high_time = str(raw_high_time) + " s"

            # low time -> discharge time
            low_time = 0.693 * resistance_two * capacitor
            low_time = round(low_time, 4)
            low_time = str(low_time) + " s"

            # duty cycle
            # duty = (raw_high_time / raw_period) * 100
            # duty = round(duty, 4)
            # duty = str(duty) + " %"

            # duty cycle - > correct duty cycle
            duty = (resistance_two) / ((resistance_one) + 2*resistance_two)
            duty = round(duty, 2)
            duty *= 100
            duty = str(duty) + " %"

            # display the values in the text fields

            # start by clearing the previously calculated values
            self.astable_frequency.delete(0, END)
            self.astable_period.delete(0, END)
            self.astable_duty.delete(0, END)
            self.astable_time_high.delete(0, END)
            self.astable_time_low.delete(0, END)

            # then display the values in their respective fields
            self.astable_frequency.insert(0, frequency)
            self.astable_period.insert(0, period)
            self.astable_duty.insert(0, duty)
            self.astable_time_high.insert(0, high_time)
            self.astable_time_low.insert(0, low_time)

    def engineering_notation(self, raw_value):
        """
        convert the given value to engineering notation
        """
        if raw_value >= 1000000:
            return str(raw_value / 1000) + " K"
        elif 1000 <= raw_value < 1000000:
            return str(raw_value / 1000000) + "M"

    def error_msg(self):
        """Show error message"""
        showwarning(title="Error", message="Enter numerical values only")

def initialize():
    root = Tk()
    main = Main(root)

    # setting window icon
    icon = ImageTk.PhotoImage(Image.open(get_resource_path("five_timer", "resources/icon.jpg")))
    root.iconphoto(False, icon)

    root.mainloop()


if __name__ == '__main__':
    initialize()