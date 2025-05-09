#!/bin/bash

echo -e "Enter date of logs. This will be used to make a directory of parsed files.\n"
read -p 'Date: ' datevar
echo 

green=$(tput setaf 2)
reset=$(tput sgr0)

subdirectory="$datevar/"

# Make directory if it doesn't exist
if [ -d "$datevar" ]; then
    echo "$datevar directory exists. Skipping dir creation."
else
    echo -e "Creating $datevar directory...\n"
    mkdir $datevar
fi

# Combine all lines, remove duplicates, order by date, export to folder
python3 export_combined_lines.py > "$subdirectory$datevar.log"

# Organize and export logs by user
echo -e "${green}Creating logs by user...\n${reset}"
python3 get_logs_by_user.py > "$subdirectory"logs_by_user.log

# # Export network errors
# echo -e "${green}Creating list of network errors...\n${reset}"
# python3 get_network_errors.py > "$subdirectory"getstream_network_errors.log

# # Export 400 errors
# echo -e "${green}Creating list of 400 errors...\n${reset}"
# python3 get_400_and_500_errors.py > "$subdirectory"400_500_errors.log

# # Export Response Times
# echo -e "${green}Calculating response times...\n${reset}"
# python3 response_times.py > "$subdirectory"response_times.log

# echo -e "${green}DONE!\n${reset}"
