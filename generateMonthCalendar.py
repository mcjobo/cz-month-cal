import monthCalendarPdf
import pytz
import datetime
import loadCal
import parseCal
import os
import boto3
import logging
from dateutil import relativedelta
from babel.dates import format_date



def generate(start, end):

    tz = pytz.timezone('Europe/Berlin');
    bucket = os.environ.get('CT_BUCKET');
    filename = os.environ.get('CT_FILENAME');
    aws_access_key_id = os.environ.get('CT_AWS_KEY_ID');
    aws_secret_access_key = os.environ.get('CT_AWS_ACCESS_KEY');
    region_name = os.environ.get('CT_AWS_REGION');


    events = loadCal.load(None, None);
    list = parseCal.parsecal(events);
    # list = parsecal.populate_list(events, start, end)
    # list = parsecal.sort_events_time(list)

    filename = format_date(start, "YYYY-MM", locale='de_DE')+".pdf"
    monthCalendarPdf.go(start, end, list, "/tmp/cal-pdf");

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name);
    s3.upload_file("/tmp/cal-pdf", bucket, filename, ExtraArgs={'ACL': 'public-read'})


    file_url = '%s/%s/%s' % (s3.meta.endpoint_url, bucket, filename)
    logging.debug("fileurl: %s", file_url);
    return file_url;

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def go(event, context):
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


    # print("event--1: ", str(event));
    # print("context--1:", str(context));
    logging.debug("event--2: ", str(event));
    # logging("context:", str(context));

    start = datetime.date.today().replace(day=1)
    end = last_day_of_month(datetime.date.today());

    if("path" in event and event['path'] == '/next'):
        start = datetime.date.today().replace(day=1) + relativedelta.relativedelta(months=1)
        end = last_day_of_month(datetime.date.today() + relativedelta.relativedelta(months=1));

    elif("path" in event and event['path'] == '/custom'):
        logging.error("custom month generating not yet implemented")
        raise Exception("custom month generating not yet implemented")

    url = generate(start, end);
    response = {
        "isBase64Encoded": 'false',
        "statusCode": 302,
        "headers": { "Location": url },
        "body": ""
    }
    return response;

os.environ['CT_URL']='https://cz-hro-test.church.tools/index.php'
os.environ['CT_CAL_ID']='2'
os.environ['CT_USER']='jorg@bolay.org'
os.environ['CT_PASSWORD']='pNlKukogySl0MhsOebot'
os.environ['CT_BUCKET'] = 'cz-cal.bolay.org'
os.environ['CT_FILENAME'] ='cal.pdf'
os.environ['CT_AWS_KEY_ID']='AKIAIGVLPEG3VD7IXHGA'
os.environ['CT_AWS_ACCESS_KEY']='tN4v9CKnhrkiEnDBYNQXV5izwPDfmFd1gld7t5D5'
os.environ['CT_AWS_REGION']='eu-west-1'
# start = datetime.date.today().replace(day=1)
# end = last_day_of_month(datetime.date.today());
start = datetime.date.today().replace(day=1) + relativedelta.relativedelta(months=1)
end = last_day_of_month(datetime.date.today() + relativedelta.relativedelta(months=1));
generate(start, end);