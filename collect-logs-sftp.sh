#!/bin/bash
# Check SSH connection before executing scripts
ssh -o BatchMode=yes -o ConnectTimeout=5 $ENV.$SITE_UUID@appserver.$ENV.$SITE_UUID.drush.in echo ssh_connection_ok
if [ $? -ne 0 ]; then
    echo "SSH connection failed"
    exit 1
fi


# local directory path to copy files
LOG_DIR="logs"

# Site UUID is REQUIRED: Site UUID from Dashboard URL, e.g. 12345678-1234-1234-abcd-0123456789ab
if [ "$1" != "" ]; then
    SITE_UUID=$1
else
    echo "Site UUID is REQUIRED"
    exit 1
fi
# Environment is REQUIRED: dev/test/live/or a Multidev
if [ "$2" != "" ]; then
    ENV=$2
else
    echo "Environment is REQUIRED"
    exit 1
fi


########### Additional settings you don't have to change unless you want to ###########
# OPTIONAL: Set AGGREGATE_NGINX to true if you want to aggregate nginx logs.
#  WARNING: If set to true, this will potentially create a large file
AGGREGATE_NGINX=false
# if you just want to aggregate the files already collected, set COLLECT_LOGS to FALSE
COLLECT_LOGS=true
# CLEANUP_AGGREGATE_DIR removes all logs except combined.logs from aggregate-logs directory.
CLEANUP_AGGREGATE_DIR=false


if [ $COLLECT_LOGS == true ]; then
echo 'COLLECT_LOGS set to $COLLECT_LOGS. Beginning the process...'
for app_server in $(dig +short -4 appserver.$ENV.$SITE_UUID.drush.in);
do
    echo "get -R logs $LOG_DIR/\"app_server_$app_server\"" | sftp -o StrictHostKeyChecking=no -o Port=2222 "$ENV.$SITE_UUID@$app_server"
done

# Include MySQL logs
for db_server in $(dig +short -4 dbserver.$ENV.$SITE_UUID.drush.in);
do
    echo "get -R logs $LOG_DIR/\"db_server_$db_server\"" | sftp -o StrictHostKeyChecking=no -o Port=2222 "$ENV.$SITE_UUID@$db_server"
done
else
echo 'skipping the collection of logs..'
fi

if [ $AGGREGATE_NGINX == true ]; then
echo 'AGGREGATE_NGINX set to $AGGREGATE_NGINX. Starting the process of combining nginx-access logs...'
mkdir aggregate-logs

for d in $(ls -d app*/nginx); do
    for f in $(ls -f "$d"); do
    if [[ $f == "nginx-access.log" ]]; then
        cat "$d/$f" >> aggregate-logs/nginx-access.log
        cat "" >> aggregate-logs/nginx-access.log
    fi
    if [[ $f =~ \.gz ]]; then
        cp -v "$d/$f" aggregate-logs/
    fi
    done
done

echo "unzipping nginx-access logs in aggregate-logs directory..."
for f in $(ls -f aggregate-logs); do
    if [[ $f =~ \.gz ]]; then
    gunzip aggregate-logs/"$f"
    fi
done

echo "combining all nginx access logs..."
for f in $(ls -f aggregate-logs); do
    cat aggregate-logs/"$f" >> aggregate-logs/combined.logs
done
echo 'the combined logs file can be found in aggregate-logs/combined.logs'
else
echo "AGGREGATE_NGINX set to $AGGREGATE_NGINX. So we're done."
fi

if [ $CLEANUP_AGGREGATE_DIR == true ]; then
echo 'CLEANUP_AGGREGATE_DIR set to $CLEANUP_AGGREGATE_DIR. Cleaning up the aggregate-logs directory'
find ./aggregate-logs/ -name 'nginx-access*' -print -exec rm {} \;
fi