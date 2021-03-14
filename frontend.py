from dearpygui.core import *
from dearpygui.simple import *

# Define the callback function of the Enter button:
def receiveInputs(sender, data):
    # Get slider values of the key information:
    noDays = get_value("Simulation days")
    popltn = get_value("Population size")
    noInfected1 = get_value("Number of infected on day 1")
    
    # Disable sliders and button:
    configure_item("Simulation days", enabled=False)
    configure_item("Population size", enabled=False)
    configure_item("Number of infected on day 1", enabled=False)
    configure_item("Enter", enabled=False)
    
    print("Sliders disabled. Fetched values:")
    print(noDays, popltn, noInfected1)

# Setting the window object
set_main_window_size(1540, 1020)
set_global_font_scale(1.25)
set_theme("Classic") # try Classic / Dark / Grey
set_style_window_padding(30, 30)

with window("SEIQR simulation (COVID-19)", width=700, height=240):
    print("GUI1 is running...")
    set_window_pos("SEIQR simulation (COVID-19)", 0, 0)
    
    # Intructions
    add_text("Please enter the key information of the simulation")
    add_separator()
    add_spacing(count=6)
    
    # Input sliders
    
    # CONSIDER: 
    # A plot running and changing all the time based on the slider inputs
    # then add callback function for each slider
    # https://hoffstadt.github.io/DearPyGui/api_core.html#dearpygui.core.add_slider_int
    add_slider_int("Simulation days", default_value=60, min_value=30, max_value=90, width=300)
    add_slider_int("Population size", default_value=650, min_value=300, max_value=1000, width=300)
    add_slider_int("Number of infected on day 1", default_value=1, min_value=1, max_value=100, width=300)
    
    # Action button
    # the callback function is receiving inputs from the user and
    # triggering the simulation
    add_button("Enter", callback=receiveInputs)
    # After these simulation details have been entered, the sliders above should
    # be made frozen (values can't be changed until simulation is finished)
    
    
# CONSIDER: Add a fourth window for "Start over" button which resets all
# values and windows for enabling using the app over and over
    
with window("Simulation plot 1", width=700, height=605):
    print("GUI2 is running...")
    set_window_pos("Simulation plot 1", 0, 250)
    add_text("Parameters for scenario 1", color=(163, 102, 255))
    
    add_slider_int("1. Government Stringency Index", default_value=50, min_value=0, max_value=100, width=300)
    add_slider_int("1. Usage of masks (%)", default_value=50, min_value=0, max_value=100, width=300)
    add_slider_int("1. Compliance of quarantine (%)", default_value=50, min_value=0, max_value=100, width=300)
    
    
    # Add this widget only AFTER the button has been clicked.
    # The plots will be shown here.
    
    # PLOT: add_scatter_series? x [] y []
    
    add_separator()
    add_spacing(count=6)
    add_plot("Scenario 1", x_axis_name="Day", y_axis_name="Number of cases")
    
with window("Simulation plot 2", width=700, height=605):
    print("GUI2 is running...")
    set_window_pos("Simulation plot 2", 710, 250)
    add_text("Parameters for scenario 2", color=(163, 102, 255))
    
    add_slider_int("2. Government Stringency Index", default_value=50, min_value=0, max_value=100, width=300)
    add_slider_int("2. Usage of masks (%)", default_value=50, min_value=0, max_value=100, width=300)
    add_slider_int("2. Compliance of quarantine (%)", default_value=50, min_value=0, max_value=100, width=300)
    
    
    # Add this widget only AFTER the button has been clicked.
    # The plots will be shown here.
    
    add_separator()
    add_spacing(count=6)
    add_plot("Scenario 2", x_axis_name="Day", y_axis_name="Number of cases")
    
start_dearpygui()