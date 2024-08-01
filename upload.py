import sqlite3
import csv
import os
from datetime import datetime  # Ensure datetime is imported
import subprocess

# Get the current date in YYYY-MM-DD format and username
current_date = datetime.now().strftime("%Y-%m-%d")
username = os.getlogin()

# Define paths
db_path = rf'C:\Users\{username}\footscan\gaitessentials9\footscan.sqlite'
combined_csv_dir = rf'C:\Users\{username}\footscan\gaitessentials9\Converted'
combined_csv_file = os.path.join(combined_csv_dir, 'Converted.csv')
local_dir = rf'C:\Users\{username}\footscan\gaitessentials9\Converted'
s3_bucket = "fyzical-superfeet"
s3_path = f"{current_date}/{username}"

# Ensure the directory exists
os.makedirs(combined_csv_dir, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query data from the Person table
cursor.execute('''SELECT FirstName, LastName, Gender, Birthdate, Remarks, globalid, orphan FROM Person''')
person_data = cursor.fetchall()

# Query data from the Session table
cursor.execute('''SELECT Subject_Session, DateTime, Remarks, Name, orphan FROM Session''')
session_data = cursor.fetchall()

# Close the database connection
conn.close()

# Write combined data to CSV
with open(combined_csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header with a source column
    writer.writerow(['Source', 'FirstName', 'LastName', 'Gender', 'Birthdate', 'Remarks', 'globalid', 'orphan', 'Subject_Session', 'SessionDateTime', 'SessionRemarks', 'SessionName', 'SessionOrphan'])
    
    # Write person data with the 'Person' source
    for row in person_data:
        writer.writerow(['Person'] + list(row) + [None, None, None, None])

    # Write session data with the 'Session' source, shifted eight columns to the right
    for row in session_data:
        writer.writerow(['Session', None, None, None, None, None, None, None] + list(row))

print(f'Data has been written to {combined_csv_file}')

# Run the AWS S3 sync command to upload new files
subprocess.run([
    'aws', 's3', 'cp', 
    local_dir, 
    f's3://{s3_bucket}/{s3_path}', 
    '--exclude', 'updates/*', 
    '--exclude', '*.log', 
    '--exclude', 'WebCache/*', 
    '--exclude', '*.dmp', 
    '--recursive'
])

print(f'Files have been uploaded to s3://{s3_bucket}/{s3_path}')
