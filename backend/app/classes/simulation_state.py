is_simulation_cancelled = False

def cancel_simulation():
    global is_simulation_cancelled
    is_simulation_cancelled = True

def reset_simulation():
    global is_simulation_cancelled
    is_simulation_cancelled = False

def check_cancellation():
    return is_simulation_cancelled