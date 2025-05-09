from config import get_fi_dict
from combine_lines_from_files import combine_lines_from_files

fi_dict = get_fi_dict()
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
    str_query = f"{customer_id} Found keyset matching kid "
    customer_fi_kid_line = next((line for line in user_lines if str_query in str(line)), None)

    # If found, get FI dict
    if customer_fi_kid_line is not None:
        fi_kid = customer_fi_kid_line.split(str_query)[1]
        fi_kid = fi_kid.split("\n")[0]
        fi = fi_dict.get(fi_kid)

        # Find all P2P instances with customer id
        str_query = f"{customer_id} POST /NeuralPaymentsP2P"
        np_ext_lines = [line for line in user_lines if str_query in line]

        np_ext_line = None
        if len(np_ext_lines) != 0 and fi is not None:
            np_ext_line = np_ext_lines[0]
            # Get response time from line and add to list
            split1 = np_ext_line.split(") ")[1]
            time = split1.split("ms\n")[0]
            fi['res_times'].append(time)

# Sort by FI name
fi_items = sorted(fi_dict.items(), key=lambda x:x[1].get('name'))

# Get average for FIs and print to console
for kid, value in fi_items:
    times = len(value['res_times'])
    values = [float(time) for time in value['res_times']]
    values.sort()

    if times > 0:
        min = values[0]
        max = values[-1]
        total = sum(values)
        average = round((total / times), 2)
        print(value['name'])
        print(f"Avg: {average}")
        print(f"Min: {min}")
        print(f"Max: {max}")
        print(f"{times} requests\n")
    else:
        print(value['name'])
        print("0 requests\n")