from datetime import datetime

# The database store dates in UTC, we are converting to local time when
# selecting from database using: DATETIME(created_at, 'localtime').
#
# We store local date to UTC using: DATETIME('2006-09-09 14:32:32', 'utc')


def parse_timestamp_string(timestamp_string):
    return datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S')
