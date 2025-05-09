from combine_lines_from_files import combine_lines_from_files

combined_lines = []
unique_users = []

kid_line = " Found keyset matching kid "

NETWORK_ERROR = 'Frontend: stream_info:'

combined_lines, q2_user_ids = combine_lines_from_files()

# Get instances of Network Error
network_error_lines = [line for line in combined_lines if NETWORK_ERROR in line]

for line in network_error_lines:
    user_id = line.split('"userid": ')[1].split(',')[0]
    user_id = user_id.replace('"','')
    if user_id not in unique_users:
        unique_users.append(user_id)

print("Network Error lines count:", len(network_error_lines))
print("Affected users count:", len(unique_users))

for line in network_error_lines:
    print(line)

for user_id in unique_users:
    user_network_error_lines = [line for line in network_error_lines if user_id in line]
    print("USER_ID:", user_id)
    print("Total lines", len(user_network_error_lines))
    started_network_errors = [line for line in user_network_error_lines if '"attempt": "20"' in line]
    ended_network_errors = [line for line in user_network_error_lines if '"attempt": "0"' in line]
    print("Errors at start:", len(started_network_errors))
    print("Errors on last iteration:", len(ended_network_errors), "\n")
