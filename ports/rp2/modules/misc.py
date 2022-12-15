def date_converter_to_date_string(datetime : list):

    return f"{add_null(datetime[2])}/{add_null(datetime[1])}/{add_null(datetime[0])} {datetime[4]}:{datetime[5]}:{datetime[6]}"

def date_converter_to_hour_string(datetime : list):

    return f"{datetime[3]}:{datetime[4]}"

def add_null(num : str):
    if len(str(num)) == 1:

        return "0" + str(num)
    else:

        return str(num)
    
def check_if_time_is_between(start_time : str, end_time : str, aktuell_time : str):
    if start_time <= end_time:

        return start_time <= aktuell_time <= end_time
    else:

        return start_time <= aktuell_time
    
def convert_bytes_to_string(line : str):
    try:
        try:

            return line.decode('utf-8').strip()
        except UnicodeDecodeError:

            return line.decode('latin1').strip()
    except:

        return line

def replace_placeholder(string : str, args : list):
  for index, arg in enumerate(args):
    string = string.replace(f"@{index + 1}", str(arg))

  return string

def convert_hour_min_to_milliseconds(tulpe):

    return tulpe[0] * 60 * 60 * 1000 + tulpe[1] * 60 * 1000

def how_long_sleep(starttime, timenow):

    def how_long_hour(starttime, timenow):
        if int(starttime[0:2]) >= int(timenow[0:2]):
            sleep = int(starttime[0:2]) - int(timenow[0:2])
        else:
            tn = int(timenow[0:2])
            to = 0
            sleep = 0
            while tn != int(starttime[0:2]):
                if tn == 24:
                    break
                else:
                    tn += 1
                    sleep += 1
            while to != int(starttime[0:2]):
                sleep += 1
                to += 1

        return(sleep)

    def how_long_min(starttime, timenow):
        if int(starttime[3:5]) >= int(timenow[3:5]):
            sleep = int(starttime[3:5]) - int(timenow[3:5])
        else:
            tn = int(timenow[3:5])
            to = 0
            sleep = 0
            while tn != int(starttime[3:5]):
                if tn == 60:
                    break
                else:
                    tn += 1
                    sleep += 1
            while to != int(starttime[3:5]):
                sleep += 1
                to += 1
                
        return(sleep)

    Minuten = how_long_min(starttime , timenow)
    if Minuten >= int(starttime[3:5]):
        Stunden = how_long_hour(starttime , timenow)-1
    else:
        Stunden = how_long_hour(starttime , timenow)
    
    return Stunden, Minuten
