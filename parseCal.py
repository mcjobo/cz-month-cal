import logging
import pprint
import datetime
import os
from dateutil.rrule import rrule, rruleset, MONTHLY, WEEKLY, YEARLY, DAILY, SU, MO, TU, WE, TH, FR, SA


def parsecal(eventData):
    commonCalId = os.environ.get('CT_CAL_ID');

    events = eventData['data'];
    events = events[commonCalId];
    eventList = [];

    for key, event in events.items():
        logging.debug("current event: %s", pprint.pformat(event))
        if event['repeat_id'] == '0':
            parsSingleEvent(event, eventList);
        else:
            parseRepeatEvent(event, eventList);
    return eventList;


def parsSingleEvent(event, eventList):

    entry = {};
    entry["data"] = event["bezeichnung"] if "bezeichnung" in event else "";
    entry["summary"] = event["ort"] if "ort" in event else "";
    entry["description"] = event["notizen"] if "notizen" in event else "";
    entry["starttime"] = parseDate(event["startdate"]);
    entry["start"] = entry["starttime"].date();
    entry["end"] = parseDate(event["enddate"]);
    if entry['start'] != entry["end"].date():
        entry["multi"] = True;
    else:
        entry["multi"] = False;
    eventList.append(entry);



def parseRepeatEvent(event, eventList):
    events = [];
    set = rruleset()
    start = parseDate(event["startdate"]).date();
    end = parseDate(event["repeat_until"]).date();
    if event['repeat_id'] == '1':
        rrule = getEventListRepeatDaily(event, start, end);
    elif event['repeat_id'] == '31':
        rrule = getEventListRepeatMonthDay(event, start, end);
    elif event['repeat_id'] == '32':
        rrule = getEventListRepeatMonthWeekday(event, start, end);
    elif event['repeat_id'] == '365':
        rrule = getEventListRepeatYear(event, start, end);
    elif event['repeat_id'] == '7':
        rrule = getEventListRepeatWeek(event, start, end);
    elif event['repeat_id'] == '999':
        rrule = getEventListRepeatManual(event, start, end);

    set.rrule(rrule);
    if "exceptions" in event:
        exc = event['exceptions'];
        for key, exception in exc.items():
            set.exdate(parseDate(exception['except_date_start']))

    events = list(set);

    for singleEvent in events:
        entry = {};
        entry["data"] = event["bezeichnung"] if "bezeichnung" in event else "";
        entry["summary"] = event["ort"] if "ort" in event else "";
        entry["description"] = event["notizen"] if "notizen" in event else "";
        entry["starttime"] = parseDate(event["startdate"]);
        entry["start"] = singleEvent.date();
        entry["end"] = parseDate(event["enddate"]);
        if entry['start'] != entry["end"].date():
            entry["multi"] = True;
        else:
            entry["multi"] = False;
        eventList.append(entry);


def parseDate(dateStr):
    return datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")


def getEventListRepeatDaily(event, start, end):
    return rrule(freq=DAILY, dtstart=start, until=end, interval=int(event["repeat_frequence"]))


def getEventListRepeatMonthDay(event, start, end):
    return rrule(freq=MONTHLY, dtstart=start, until=end, interval=int(event["repeat_frequence"]))


def getEventListRepeatMonthWeekday(event, start, end):
    weekday = start.weekday();
    weeknumber = int(event['repeat_option_id']);

    return rrule(freq=MONTHLY, dtstart=start, until=end, interval=int(event["repeat_frequence"]), byweekday=weekday, bysetpos=weeknumber);


def getEventListRepeatYear(event, start, end):
    return  rrule(freq=YEARLY, dtstart=start, until=end, interval=int(event["repeat_frequence"]))


def getEventListRepeatWeek(event, start, end):
    return rrule(freq=WEEKLY, dtstart=start, until=end, interval=int(event["repeat_frequence"]))


def getEventListRepeatManual(event, start, end):
    logging.error("Manual Repeat not yet implemented please investigate")
    return [];