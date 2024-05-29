# Get the current date in YYYY-MM-DD format
$date = Get-Date -Format "yyyy-MM-dd"
$user = $env:username

# Define your local directory and S3 bucket
$localDir = "C:\Users\FYZICALOrem\footscan\gaitessentials9"
$s3Bucket = "fyzical-superfeet"

# Define the S3 path with the current date
$s3Path = "$user"

# Run the AWS S3 sync command to upload new files
aws s3 sync $localDir s3://$s3Bucket/$date/$s3Path --exclude "updates/*" --exclude "*.log" --exclude "WebCache/*" --exclude "*.dmp"