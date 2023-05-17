def seconds_formatted(sec:int) -> str:
    # only positive number
    if sec == 0:
        return '0 seconds'
    elif sec < 0:
        return 'Please enter a positive number'
    else:
        # calculate the number of each part
        day_count = sec // 86400
        hour_count = sec % 86400 // 3600
        minute_count = sec % 86400 % 3600 // 60
        second_count = sec % 86400 % 3600 % 60
        time_frame = [(day_count, 'day'), (hour_count, 'hour'), (minute_count, 'minute'), (second_count, 'second')]

    # format each part of the output
    output_format = []
    for x, y in time_frame:
        if x > 0:
            # whether it's singular
            if x == 1:
                output_format.append(f'{x} {y}')
            else:
                output_format.append(f'{x} {y}s')
    
    # join each part together
    human_friendlyformatted = ', '.join(output_format)
    return human_friendlyformatted

def main():
    time_convert = input('Please enter your number: ')
    #test whether the input is a number
    try:
        # read from input and convert
        sec_int = int(time_convert)
        print(seconds_formatted(sec_int))
    except:
        # ask for a number
        print('Invalid number. Please try again.')

# implement main() program
main()