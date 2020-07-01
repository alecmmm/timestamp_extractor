
import os
import platform
import pandas as pd

"""
creation_date function is modified code, originally created by Mark Amery on September 14, 2016, and found on Stack Overflow.
See: https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
"""

def creation_date(path_to_file):

    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """

    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file), os.path.getmtime(path_to_file)

    else:
        stat = os.stat(path_to_file)

        try:
            return stat.st_birthtime, stat.st_mtime

        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime, stat.st_mtime

directory = input("Please input directory to search: ")

df = pd.DataFrame({"file_name": [], "date_created": [], "last_date_modified": []})

for file_name in os.listdir(directory):
    file_info = creation_date(os.path.join(directory, file_name))
    df = df.append(pd.Series([file_name, file_info[0], file_info[1]], index=df.columns), ignore_index=True)

#convert to date time
df["date_created"] = pd.to_datetime(df["date_created"], unit='s')
df["last_date_modified"] = pd.to_datetime(df["last_date_modified"], unit='s')

#convert to EST
df["date_created"] = df["date_created"].dt.tz_localize("GMT").dt.tz_convert('US/Eastern').dt.tz_localize(None)
df["last_date_modified"] = df["last_date_modified"].dt.tz_localize("GMT").dt.tz_convert('US/Eastern').dt.tz_localize(None)

#print to csv
df.to_csv("time_stamps.csv")
print_msg = "\ntimestamp.csv printed to " + os.getcwd()
print_msg_len = len(print_msg)
print("=" * print_msg_len + print_msg + "\n" + "=" * print_msg_len)
df.to_csv("time_stamps.csv")
