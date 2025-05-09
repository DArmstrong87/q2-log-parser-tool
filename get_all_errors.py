from config import get_fi_dict
from combine_lines_from_files import combine_lines_from_files

fi_dict = get_fi_dict()
kid_line = " Found keyset matching kid "
delimiter = "=" * 100 + "\n"

ERROR = 'ERROR extension.NeuralPaymentsP2P Cust'
WARNING = 'WARNING extension.NeuralPaymentsP2P Cust'
password_changed_line = 'last changed their password on'
FRONTEND = 'Frontend:'

# These are the lines you want to include
error_lines = [
                ERROR,
                WARNING,
                FRONTEND
            ]

customer_ids = []
combined_lines, q2_user_ids = combine_lines_from_files()
for line in combined_lines:
    split1 = line.split('extension.NeuralPaymentsP2P Cust ')
    if len(split1) > 1:
        customer_id = split1[1].split(" ")[0]
        if customer_id not in customer_ids:
            customer_ids.append(customer_id)

# Get response times for FIs    
for customer_id in customer_ids:
    # Get user lines and find 'kid' of FI
    user_lines = [line for line in combined_lines if customer_id in str(line)]
    str_query = f"{customer_id}{kid_line}"
    customer_fi_kid_line = next((line for line in user_lines if str_query in str(line)), None)

    # Get external_id and Q2 user_id
    str_query = f"{customer_id} Got external id: "
    external_id_line = next((line for line in user_lines if str_query in str(line)), None)
    split_str = ' for user_id '
    external_id = None
    user_id = None

    if external_id_line:
        external_id = external_id_line.split(str_query)[1].split(split_str)[0].split("\n")[0]
        user_id = external_id_line.split(str_query)[1].split(split_str)[1].split("\n")[0]

    # If found, get FI dict
    if customer_fi_kid_line is not None:
        fi_kid = customer_fi_kid_line.split(f"{customer_id}{kid_line}")[1]
        fi_kid = fi_kid.split("\n")[0]
        fi = fi_dict.get(fi_kid)

        # Find all instances with customer id and errors
        for error_line in error_lines:
            str_query = f"{error_line} {customer_id}"
            np_error_lines = [line for line in user_lines if str_query in line]
            password_changed_lines = [line for line in user_lines if password_changed_line in line]

            if len(np_error_lines) > 0 and external_id and user_id:
                print(fi.get('name'))
                print("user_id", user_id)
                print("external_id", external_id)

                for error_line in np_error_lines:
                    print(error_line)
        
            # Get password changed lines
            if len(password_changed_lines) > 0 and external_id and user_id and password_changed_line in error_lines:
                print(fi.get('name'))
                print("user_id", user_id)
                print("external_id", external_id)

                for pwd_line in password_changed_lines:
                    print(pwd_line)
            
            if len(np_error_lines) > 0:
                print(f"{delimiter}\n")


    if customer_fi_kid_line is None:
        fi = "Unknown FI - Couldn't find the KID line in these logs to match with an FI"
        # Find all instances with customer id and errors
        for error_line in error_lines:
            str_query = f"{error_line} {customer_id}"
            np_error_lines = [line for line in user_lines if str_query in line]
            password_changed_lines = [line for line in user_lines if password_changed_line in line]

            if len(np_error_lines) > 0 and external_id and user_id:
                print(fi)
                print("customer_id", customer_id)
                print("user_id", user_id)
                print("external_id", external_id)

                for error_line in np_error_lines:
                    print(error_line)

            # Get password changed lines
            if len(password_changed_lines) > 0 and external_id and user_id:
                print(fi)
                print("customer_id", customer_id)
                print("user_id", user_id)
                print("external_id", external_id)

                for pwd_line in password_changed_lines:
                    print(pwd_line)
            
            if len(np_error_lines) > 0:
                print(f"{delimiter}\n")
