import requests
import json
import pprint
import logging
import os



def login():
    url = os.environ.get('CT_URL')

    url2 = url+'?q=login';
    data = {
        "email": os.environ['CT_USER'],
        "password": os.environ['CT_PASSWORD'],
        "directtool": "rest api",
    }
    logging.debug("login data %s", data)
    headers = {"Content-Type": "application/x-www-form-urlencoded"};
    response = requests.post(url2, data=data, headers=headers);
    logging.debug("login response: %s", response.text);
    try:
        if response.json()['status'] == 'success':
            return True;
    except json.decoder.JSONDecodeError:
        return False
    return False;


def loadCalData():
    url = os.environ.get('CT_URL')
    url2 = url + '/index.php?q=churchcal/ajax';
    data = {"func": "getMasterData"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"};
    response = requests.post(url2, data=data, headers=headers);
    response_json = response.json()
    logging.debug("master data response: %s", pprint.pformat(response_json));
    return response_json;


def loadEventData():
    url = os.environ.get('CT_URL')
    commonCalId = os.environ.get('CT_CAL_ID');

    url2 = url + '/index.php?q=churchcal/ajax';
    data = {"func": "getCalPerCategory", "category_ids[0]": commonCalId}
    headers = {"Content-Type": "application/x-www-form-urlencoded"};
    response = requests.post(url2, data=data, headers=headers);
    logging.debug("Event data response: %s", pprint.pformat(response.json()));
    return response.json();





def load(event, context):
    logging.basicConfig(level=logging.DEBUG)
    if login():
        masterData = loadCalData();
        eventData = loadEventData();
        return eventData;
    return None;