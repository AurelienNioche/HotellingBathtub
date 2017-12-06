# This will not me manipulated very often
n_positions = 21
n_prices = 11
n_firms = 2

# Parameters for the firms' perceptrons
alpha = 0.01
momentum = 0.01
temp = 0.01

# This will influence the computation time, but also the robustness of the results
n_simulations = 60
t_max = 5000

# These variables should affect results in an interesting manner
bot_customers = True
mode = "p_fixed"  # could be "r_fixed" or "p_fixed"
discrete = False
fields_of_view = [0.3, 0.7]  # Will be used only if discrete is true

# If you want the data to be saved
save = True
