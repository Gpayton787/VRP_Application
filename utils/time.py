#Time conversion functions
def standard_to_minutes(time):
    time = time.split(':')
    hours = int(time[0])
    minutes = int(time[1])
    hours *= 60
    total_minutes = hours + minutes
    return total_minutes

def minutes_to_standard(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    if minutes < 10:
        minutes = f"0{minutes}"
    return f"{hours}:{minutes}"

def standard_to_seconds(time):
    time = time.split(':')
    hours = int(time[0])
    minutes = int(time[1])
    hours *= 60
    total_minutes = hours + minutes
    total_seconds = total_minutes * 60
    return total_seconds

def seconds_to_standard(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes % 60
    if minutes < 10:
        minutes = f"0{minutes}"
    return f"{hours}:{minutes}"