import os
from config import directory

# Logs are compiled from end date to start date
# When logs are cut off after 9999 lines,
# you will need to get the true start date
# from these logs. This date will be used as
# the end date when pulling the next log in Q2.

file_name = '2025-02-03-5_masked.log'
file_path = f"{directory}/{file_name}"

is_file = os.path.isfile(file_path)
if is_file:
    f = open(file_path, "r")
    lines = f.readlines(-1)
    print(f"{len(lines)} lines in file ---> '{file_name}'")

    first_line = lines[0]
    last_line = lines[-1]

    start_date = first_line.split(" ")[0]
    end_date = last_line.split(" ")[0]

    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
