import datetime


def parse_hours(hours_str):
    if not hours_str:
        return None
    try:
        start_str, end_str = hours_str.split('-')
        try:
            start = datetime.datetime.strptime(
                start_str.strip(), "%I %p").time()
            end = datetime.datetime.strptime(end_str.strip(), "%I %p").time()
        except:
            start = datetime.datetime.strptime(
                start_str.strip(), "%I:%M %p").time()
            end = datetime.datetime.strptime(
                end_str.strip(), "%I:%M %p").time()
        return start, end
    except Exception as e:
        print(f"Error in  parse_hours: {e}, input={hours_str}")
        return None


def is_gym_open(gym):
    now = datetime.datetime.now()
    current_time = now.time()
    weekday = now.weekday()

    if weekday < 5:
        hours = gym.opening_hours_weekdays
    elif weekday == 5:
        hours = gym.opening_hours_saturday
    else:
        hours = gym.opening_hours_sunday

    start, end = parse_hours(hours)
    if start and end:
        if start < end:
            return start <= current_time <= end
        else:
            return current_time >= start or current_time <= end
    return False
