import os
from config import directory
from datetime import datetime

def combine_lines_from_files():
    combined_lines = []
    q2_user_ids = []

    delimiter = "=" * 100 + "\n"
    print(delimiter)

    file_list = os.listdir(directory)
    file_paths = [os.path.join(directory, filename) for filename in file_list if os.path.isfile(os.path.join(directory, filename))]
    file_paths = [file for file in file_paths if file.endswith(".log")]
    # Combine lines from all files
    print(f"Combining {len(file_list)} files...")
    for file_path in file_paths:
        is_file = os.path.isfile(file_path)
        if is_file:
            f = open(file_path, "r")
            lines = f.readlines(-1)
            combined_lines += lines
    print(f"Parsing {len(combined_lines)} lines...\n")

    # Get unique Q2 user Ids
    for line in combined_lines:
        user_id_line = line.split('for user_id ')
        if len(user_id_line) > 1:
            q2_user_id = user_id_line[1].split("\n")[0]
            if q2_user_id not in q2_user_ids:
                q2_user_ids.append(q2_user_id)
    print(f"{len(q2_user_ids)} unique Q2 users found\n")

    combined_lines = set(combined_lines) # Remove duplicates
    combined_lines = sorted(combined_lines, key=lambda x: x.split(" ")[0]) # Sort by timestamp

    # Get date range
    oldest_date = combined_lines[0].split(" ")[0]
    oldest_date = datetime.strptime(oldest_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    newest_date = combined_lines[-1].split(" ")[0]
    newest_date = datetime.strptime(newest_date, "%Y-%m-%dT%H:%M:%S.%f%z")

    fmt = "%Y-%m-%dT%H:%M:%S"
    print(f"Date Range: \n{datetime.strftime(oldest_date, fmt)} -- {datetime.strftime(newest_date, fmt)}\n")
    print(delimiter)

    return combined_lines, q2_user_ids
