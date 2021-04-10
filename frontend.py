from dearpygui.core import *
from dearpygui.simple import *
from SEIQR import SEIQR
from SEIQR import System

# Initialize global variables:
NODAYS = 0
_seiqr = None

# CONSIDER: Add a fourth window for "Start over" button which resets all
# values and windows for enabling using the app over and over
  
# CHECK:
    # - GSI values

# THESE FUNCTIONS RECEIVE THE SIMULATION INFORMATION FROM THE
# SIMULATION WINDOWS.
# They run their simulations separately and visualize the plots.
def receiveTriggerSim1(sender, data):
    gsi = get_value("1. Government Stringency Index")
    maskPrc = get_value("1. Usage of masks (%)")
    quarantinePrc = get_value("1. Compliance of quarantine (%)")
    
    # Disable sliders and button
    configure_item("1. Government Stringency Index", enabled=False)
    configure_item("1. Usage of masks (%)", enabled=False)
    configure_item("1. Compliance of quarantine (%)", enabled=False)
    configure_item("1. Enter", enabled=False)
    
    if (gsi == 0):
        gsi = 0.5
    alpha = 10/gsi # the higher value, the more strict the restrictions are
    delta = maskPrc/100
    eeta = quarantinePrc/100
    
    # RUN SIMULATION
    _system = System(_seiqr, alpha, delta, eeta, NODAYS)
    S, E, I, Q, R = System.runSimulation(_system)
    
    add_separator(parent="Simulation plot 1")
    
    # PLOT
    # this is used as the x-axis in the plots:
    listOfDays = list(range(1, NODAYS+1)) # if noDays=14, range: [1, 2, ..., 13, 14]
    add_spacing(count=6, parent="Simulation plot 1")
    add_plot("Scenario 1", x_axis_name="Day", y_axis_name="Number of cases", parent="Simulation plot 1")
    add_scatter_series("Scenario 1", "Susceptible 1", listOfDays, S, size=2)
    add_scatter_series("Scenario 1", "Exposed 1", listOfDays, E, size=2)
    add_scatter_series("Scenario 1", "Infected 1", listOfDays, I, size=2)
    add_scatter_series("Scenario 1", "Quarantined 1", listOfDays, Q, size=2)
    add_scatter_series("Scenario 1", "Recovered 1", listOfDays, R, size=2)
    
    
def receiveTriggerSim2(sender, data):
    gsi = get_value("2. Government Stringency Index")
    maskPrc = get_value("2. Usage of masks (%)")
    quarantinePrc = get_value("2. Compliance of quarantine (%)")
    
    # Disable sliders and button
    configure_item("2. Government Stringency Index", enabled=False)
    configure_item("2. Usage of masks (%)", enabled=False)
    configure_item("2. Compliance of quarantine (%)", enabled=False)
    configure_item("2. Enter", enabled=False)
      
    if (gsi == 0):
        gsi = 0.5
    alpha = 10/gsi # the higher value, the more strict the restrictions are
    delta = maskPrc/100
    eeta = quarantinePrc/100
    
    # RUN SIMULATION
    _system = System(_seiqr, alpha, delta, eeta, NODAYS)
    S, E, I, Q, R = System.runSimulation(_system)
    
    add_separator(parent="Simulation plot 2")
    
    # PLOT
    # this is used as the x-axis in the plots:
    listOfDays = list(range(1, NODAYS+1)) # if noDays=14, range: [1, 2, ..., 13, 14]
    add_spacing(count=6, parent="Simulation plot 2")
    add_plot("Scenario 2", x_axis_name="Day", y_axis_name="Number of cases", parent="Simulation plot 2")
    add_scatter_series("Scenario 2", "Susceptible 2", listOfDays, S, size=2)
    add_scatter_series("Scenario 2", "Exposed 2", listOfDays, E, size=2)
    add_scatter_series("Scenario 2", "Infected 2", listOfDays, I, size=2)
    add_scatter_series("Scenario 2", "Quarantined 2", listOfDays, Q, size=2)
    add_scatter_series("Scenario 2", "Recovered 2", listOfDays, R, size=2)


# THIS FUNCTION RECEIVES THE KEY INFORMATION THE USER ENTERS FIRST:
# It is a callback function of the Enter button.
# Only once the key information has been entered, the user can enter
# the information regarding the simulations
def receiveInputs(sender, data):
    # Get slider values of the key information:
    global NODAYS
    global _seiqr
    NODAYS = get_value("Simulation days")
    popltn = get_value("Population size")
    noInfected1 = get_value("Number of infected on day 1")
    # Create a SEIQR object (global variable)
    _seiqr = SEIQR(popltn-noInfected1, 0, noInfected1, 0, 0)
    
    # Disable "main information" sliders and button:
    configure_item("Simulation days", enabled=False)
    configure_item("Population size", enabled=False)
    configure_item("Number of infected on day 1", enabled=False)
    configure_item("Enter", enabled=False)
    
    # SETTING UP THE SIMULATION WINDOWS:
    
    # CONSIDER: 
    # A plot running and changing all the time based on the slider inputs
    # then add callback function for each slider
    # https://hoffstadt.github.io/DearPyGui/api_core.html#dearpygui.core.add_slider_int
    
    # At the moment the user enters information and clicks "Enter"
    # -> triggers the simulation in the corresponding callback function
    with window("Simulation plot 1", width=700, height=605):
        print("GUI2 is running...")
        set_window_pos("Simulation plot 1", 0, 250)
        add_text("Parameters for scenario 1", color=(163, 102, 255))
        
        add_slider_int("1. Government Stringency Index", default_value=50, min_value=0, max_value=100, width=300)
        add_slider_int("1. Usage of masks (%)", default_value=50, min_value=0, max_value=100, width=300)
        add_slider_int("1. Compliance of quarantine (%)", default_value=50, min_value=0, max_value=100, width=300)
        
        add_button("1. Enter", callback=receiveTriggerSim1)
        
    with window("Simulation plot 2", width=700, height=605):
        print("GUI3 is running...")
        set_window_pos("Simulation plot 2", 710, 250)
        add_text("Parameters for scenario 2", color=(163, 102, 255))
        
        add_slider_int("2. Government Stringency Index", default_value=50, min_value=0, max_value=100, width=300)
        add_slider_int("2. Usage of masks (%)", default_value=50, min_value=0, max_value=100, width=300)
        add_slider_int("2. Compliance of quarantine (%)", default_value=50, min_value=0, max_value=100, width=300)
        
        add_button("2. Enter", callback=receiveTriggerSim2)


# MAIN WINDOW THAT IS FIRST VISIBLE TO THE USER:
# INITIALIZATION: Setting up the main window object
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
    add_slider_int("Simulation days", default_value=60, min_value=30, max_value=90, width=300)
    add_slider_int("Population size", default_value=650, min_value=300, max_value=1000, width=300)
    add_slider_int("Number of infected on day 1", default_value=1, min_value=1, max_value=100, width=300)
    
    # Action button
    # the callback function is receiving inputs from the user and
    # triggering the simulation
    add_button("Enter", callback=receiveInputs)
    

    
start_dearpygui()