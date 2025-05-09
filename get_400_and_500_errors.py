from config import get_fi_dict
from combine_lines_from_files import combine_lines_from_files

fi_dict = get_fi_dict()
combined_lines = []
q2_user_ids = []

kid_line = " Found keyset matching kid "

INFO_BAD_REQUEST = '400 Bad Request'
WARNING_BAD_REQUEST = '"status":400'
FIVE_HUNDRED_ERRORS = '"status":500'
# RESPONSES = 'Received HTTP response'

# These are the lines you want to include
error_lines = [
                INFO_BAD_REQUEST,
                WARNING_BAD_REQUEST,
                FIVE_HUNDRED_ERRORS
                # RESPONSES
            ]

affected_users = 0
combined_lines, q2_user_ids = combine_lines_from_files()
for q2_user_id in q2_user_ids:

    # Get all user customer ids
    user_customer_ids = []
    customer_id_lines = [line for line in combined_lines if f'for user_id {q2_user_id}' in line]
    for line in customer_id_lines:
        customer_id_split = line.split('extension.NeuralPaymentsP2P Cust ')
        if len(customer_id_split) > 1:
            customer_id = customer_id_split[1].split(" ")[0]
            if customer_id not in user_customer_ids:
                user_customer_ids.append(customer_id)

    # Get all lines for this user
    user_lines = []
    for user_customer_id in user_customer_ids:
        user_customer_id_lines = [line for line in combined_lines if user_customer_id in line]
        user_lines += user_customer_id_lines

    # Get user external_id
    external_id = 'Could not find external_id'
    str_query = f"{customer_id} Got external id: "
    found_external_id_line = next((line for line in user_lines if str_query in str(line)), None)
    if found_external_id_line:
        external_id = found_external_id_line.split(str_query)[1].split(" for user_id ")[0].split("\n")[0]

    # Find 'kid' of FI to link user with FI
    user_kid_line = None
    for user_customer_id in user_customer_ids:
        str_query = f"{user_customer_id} Found keyset matching kid "
        customer_fi_kid_line = next((line for line in user_lines if str_query in str(line)), None)
        if customer_fi_kid_line is not None:
            user_kid_line = customer_fi_kid_line
            break

    # print(q2_user_id)
    # print("Length of user lines", len(user_lines))
    # print(user_kid_line) if user_kid_line is not None else print('None')
    # print("\n\n")

    fi_name = "Unknown FI"
    if user_kid_line is not None:
        fi_kid = user_kid_line.split("Found keyset matching kid ")[1]
        fi_kid = fi_kid.split("\n")[0]
        fi = fi_dict.get(fi_kid)
        if fi is None:
            print(fi_kid)
        else:
            fi_name = fi.get('name')

    bad_request_lines = [line for line in user_lines if any(error_line for error_line in error_lines if error_line in line)]

    if len(bad_request_lines) > 0:
        affected_users += 1
        print("Q2 user_id", q2_user_id)
        print("External_id", external_id)
        # print(fi_kid)
        print(fi_name)
        for line in bad_request_lines:
            print(line)
        delimiter = "=" * 100 + "\n"
        print(delimiter)
print("Affected users count:", affected_users)
