
# Q2 Log Parser Tool

This tool assists in parsing through thousands of lines of logs in order to quickly find errors and determine response times of the Neural Payments P2P extension per FI.

## Configuration
1. Modify config.py and update the `directory` variable to the directory of where you will be downloading and parsing the Q2 logs.
2. You will have multiple files in this directory that the tool will read.
3. The `fi_dict` contains fake institution names.

## Log Download
Download logs from the [Q2 Dashboard](https://q2developer.com/selfservice/logs)

Q2 logs are limited to 9,999 lines. The time range of a log is dependent on the amount of traffic for that day. It could be 4 hours or 12 hours and will not include the entire day. To ensure you are able to collect the entire day's worth of logs, follow these steps.

1. Start with the "To" time with your selected date and max time of 11:59pm
2. "From" time should be the same date but go about 10 hours back (1:59pm).
	- If the log fails to generate, try shortening the time.
3. Save the log in a Q2 logs directory with a common filename i.e. "06-05-2023-1.log"
4. Find the oldest date in this log. In `find_timestamp_range.py`, change the file_name and run this file.
	-  `file_name = '06-10-2023-1.log'`
	- The terminal will display the time ranges within the file.
	- Make note of the oldest timestamp.
	```
	9999 lines in file
	Oldest Date: 2023-06-30T21:06:53.456Z
	Newest Date: 2023-06-30T23:58:56.947Z
	```

5. Download the next file and input the oldest timestamp + 1 minute from the last file as the "To" timestamp.
	- If timestamp is `2023-06-30T21:06:53.456Z`, input the 'To' time as `21:07`
	- Overlapping by a minute will ensure no lines get lost.
	- The parser removes duplicate lines automatically.
6. Repeat the steps until you have the entire day's worth of logs.
	- This ranges from 10-20 files for one day 12:00am to 11:59pm
7. Update config.py and input the directory of where the logs are saved.

## Running the Parser and Generating Organized Logs

1. From this directory, run: `./parse_logs.sh`
2. Enter the date for the logs when prompted. This will be used to make a directory of parsed files.
3. The parser will generate these files in the directory you provided:
	1. 06-29-2023.log
	2. 400_errors.log
	3. getstream_network_errors.log
	4. logs_by_user.log
	5. response_times.log

## Generated Logs

### LOG: \<Date\>.log
This file is a combination of all the lines of logs in all the files provided in the config file list.

### LOG: 400_errors.log
Lists 400 errors by user.
```
Q2 user_id 778899
External_id xxx-xx-1234
Nyce Fictional Financial Institution
2023-06-29T04:20:32.643Z INFO extension.NeuralPaymentsP2P Cust 063b2fc1c44543eea22394f9f78e8c11 Received HTTP response after 163.66ms - 400 Bad Request

2023-06-29T04:20:32.644Z WARNING extension.NeuralPaymentsP2P Cust 063b2fc1c44543eea22394f9f78e8c11 Response Body: b'{"status":400,"type":"https://api.neuralpayments.com/errors/bad-request","title":"Bad Request","detail":"Transfer exceeds allowed limits"}'
```

### LOG: getstream_network_errors.log
Lists instances of a rare error seen in some users related to getstream.
- Counts affected users
- Lists all lines of this error
The USER_ID shown in this log is a getstream specific log. To link this error to a user and FI, search for this USER_ID in the combined \<Date\>.log file. Scroll up to see which user hit /stream just before the error. Grab the Q2 user Id ‘User: 1234’ and search the logs_by_user.log file.

### LOG: logs_by_user.log
Lists logs by user. These logs are useful to view the session activity of a particular user. Includes all logs including warnings and errors.
```
Q2 user_id 1234
External_id 654321
NYCE Fictional Financial Institution
<ALL LINES FOR THIS USER HERE>
```

### LOG: response_times.log
Lists all FIs with activity for that day. Gets the neuralpayments extension response times (how long it takes to load the extension within Q2). Displays Avg, Min and Max times and number of requests per FI.
```
Sunrise Valley Credit Union
Avg: 1023.59
Min: 554.11
Max: 2051.47
189 requests
```