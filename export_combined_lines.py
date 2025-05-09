import sys
from combine_lines_from_files import combine_lines_from_files

combined_lines, q2_user_ids = combine_lines_from_files()
print(f"Parsing {len(combined_lines)} lines...\n", file=sys.stderr)

for line in combined_lines:
    print(line, end='')