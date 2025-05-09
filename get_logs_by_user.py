from config import get_fi_dict
from combine_lines_from_files import combine_lines_from_files

fi_dict = get_fi_dict()
combined_lines, q2_user_ids = combine_lines_from_files()
delimiter = "=" * 100 + "\n"
kid_line = " Found keyset matching kid "

"""
    Flow of things:

    Loop through unique q2_user_ids.
        Get all customer_ids to link lines for this q2_user_id
        Get lines for each customer_id for this q2_user_id
        Order lines by timestamp
        Loop through the lines with external_ids to make list of unique external_ids for q2_user_id
            ***If more than one external_id is linked to the same q2_user_id
                print a note showing the q2_user_ids and list external_ids
            Loop through the list of unique_external_ids
                Get all customer_ids to link lines for this external_id
                Get lines for each customer_id for this external_id
                Order lines by timestamp
                Find the line to match KID with FI Name
                For each external_id, print the following before looping and printing each user line:
                    Q2 user_id 1234
                    External_id abc123
                    NYCE Fictional Credit Union
                    2023-11-01T00:10:34.255Z INFO extension.NeuralPaymentsP2P Cust d77f0950b64043b8adfc4b3356ecb9a5 Transition: routing to 'default'
"""


def parse_lines_same_user_id(external_id, user_lines):
    user_customer_ids = []
    customer_id_lines = [line for line in combined_lines if f'Got external id: {external_id} for user_id' in line and 'DEBUG' not in line]
    # 2023-11-01T20:45:37.120Z INFO extension.NeuralPaymentsP2P Cust 6906074ac5eb458c96e2f72f0932e623 Got external id: 12345 for user_id QABC123

    for line in customer_id_lines:
        customer_id_split = line.split('extension.NeuralPaymentsP2P Cust ')
        # 2023-11-01T20:45:55.844Z INFO extension.NeuralPaymentsP2P Cust 2fd2433e7bb84f9f87b5cd28c52f7e01 Sending HTTP request POST
        # Split: ["2023-11-01T20:45:55.844Z INFO extension.NeuralPaymentsP2P Cust ", "2fd2433e7bb84f9f87b5cd28c52f7e01 Sending HTTP request POST"]
        if len(customer_id_split) > 1:
            customer_id = customer_id_split[1].split(" ")[0]
            # ["2fd2433e7bb84f9f87b5cd28c52f7e01", " Sending HTTP request POST"] ---> "2fd2433e7bb84f9f87b5cd28c52f7e01"
            user_customer_ids.append(customer_id)

    user_customer_ids = list(set(user_customer_ids))

    # Get all lines for this user
    user_lines = []
    for user_customer_id in user_customer_ids:
        user_customer_id_lines = [line for line in combined_lines if user_customer_id in line and 'DEBUG' not in line]
        user_lines += user_customer_id_lines
    user_lines = sorted(user_lines, key=lambda x: x.split(" ")[0]) # Sort by timestamp

    # Find 'kid' of FI to link customer_id with FI
    user_kid_line = None
    for user_customer_id in user_customer_ids:
        str_query = f"{user_customer_id} Found keyset matching kid "
        # "2fd2433e7bb84f9f87b5cd28c52f7e01 Found keyset matching kid "
        customer_fi_kid_line = next((line for line in user_lines if str_query in str(line)), None)
        if customer_fi_kid_line is not None:
            user_kid_line = customer_fi_kid_line
            break

    # Get FI name from the FI KID
    fi_name = "Unknown FI"
    if user_kid_line is not None:
        fi_kid = user_kid_line.split("Found keyset matching kid ")[1]
        fi_kid = fi_kid.split("\n")[0]
        fi = fi_dict.get(fi_kid)
        if fi:
            fi_name = fi['name']

    # Show Q2 user_id, external_id, fi_name
    # Print all user lines
    if len(user_lines) > 0:
        print(fi_name)
        print("Q2 user_id", q2_user_id)
        print("External_id", external_id)
        for line in user_lines:
            print(line, end="")
        print(f"{delimiter}\n")


for q2_user_id in q2_user_ids:
    # Get all customer Ids
    user_customer_ids = []
    customer_id_lines = [line for line in combined_lines if f'for user_id {q2_user_id}' in line and 'DEBUG' not in line]

    for line in customer_id_lines:
        customer_id_split = line.split('extension.NeuralPaymentsP2P Cust ')
        if len(customer_id_split) > 1:
            customer_id = customer_id_split[1].split(" ")[0]
            user_customer_ids.append(customer_id)

    user_customer_ids = list(set(user_customer_ids))

    # Get all lines for this user
    user_lines = []
    for user_customer_id in user_customer_ids:
        user_customer_id_lines = [line for line in combined_lines if user_customer_id in line and 'DEBUG' not in line]
        user_lines += user_customer_id_lines
    user_lines = sorted(user_lines, key=lambda x: x.split(" ")[0]) # Sort by timestamp

    # Get user external_id
    external_id = 'Could not find external_id'
    str_query = "Got external id: "
    str_user_id = f"for user_id {q2_user_id}\n"
    found_external_id_lines = [line for line in user_lines if str_query in str(line) and str_user_id in str(line)]
    # Got external id: 6491901 for user_id 1

    # Look for multiple users with the same q2 user_id
    unique_external_ids = set(line.split(str_query)[1].split(" for user_id ")[0].split("\n")[0] for line in found_external_id_lines)
    # Split by "Got external id: "
    # ["2023-11-01T20:46:49.848Z INFO extension.NeuralPaymentsP2P Cust 6c21b51236a14a3d919b375e8601c1f2 Got external id: ", "xxx-xx-1234 for user_id abcd1234\n"]
    # Split by " for user_id " ---> ["xxx-xx-1234 for user_id ", "abcd1234\n"]
    # Split by line break "\n" ----> "abcd1234"
    unique_external_ids_for_q2_user_id = list(unique_external_ids)
    
    if len(unique_external_ids_for_q2_user_id) > 1:
        print(f"Found {len(unique_external_ids_for_q2_user_id)} external ids with the same online user_id of {q2_user_id}:", unique_external_ids_for_q2_user_id, "\n")
    
    for external_id in unique_external_ids_for_q2_user_id:
        parse_lines_same_user_id(external_id, user_lines)
