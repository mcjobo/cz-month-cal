from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from babel.dates import format_date, format_time
import dates

import pytz
import datetime


styles = getSampleStyleSheet()
normal = styles["Normal"]
normal.fontSize = 8
italic = styles["Italic"]
italic.fontSize = 8

startMonth = format_date(datetime.datetime.now().date(), "MMMM YYYY", locale='de_DE');

def go(start, end, eventList, filePath):
    global startMonth;
    startMonth = format_date(start, "MMMM YYYY", locale='de_DE')
    doc = SimpleDocTemplate(filePath)
    Story = []
    Story.append(createEventTable(start, end, eventList))
    Story.append(createImpressumPara())
    doc.build(Story, onFirstPage=templateBackground, onLaterPages=templateBackground)


def templateBackground(canvas, doc):
    canvas.drawImage("month-background.jpeg", 0, 0, height=842, width=595);
    canvas.saveState()
    pagesize = canvas._pagesize
    canvas.setFont("Helvetica", 7)
    formatetDate = format_date(datetime.datetime.now().date(), locale='de_DE', format="long")
    canvas.drawRightString(pagesize[0] - 20, 10, "erstellt am: " + formatetDate)
    canvas.restoreState()
    canvas.saveState()
    pagesize = canvas._pagesize
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(pagesize[0] - 168, 782, startMonth)
    canvas.restoreState()


def createImpressumPara():

    k = Paragraph('<b>Kontakt:</b>',italic)
    kt = Paragraph('0381- 210 364 20 | <b>eMail:</b> nachricht@cz-rostock.de | <b>Internet:</b> cz-rostock.de',italic)
    p = Paragraph('<b>Pastor:</b>', italic)
    pt = Paragraph('Daniel Reimer | 0381 - 21 04 54 21 | daniel.reimer@cz-rostock.de', italic)
    a = Paragraph('<b>Adresse:</b>', italic)
    at = Paragraph('<b>Am Schmarler Bach 2; 18106 Rostock</b>', italic)
    b = Paragraph('<b>Bankverbindung:</b>', italic)
    bt = Paragraph('<b>CZ ROSTOCK IBAN: DE77130500000205013414 BIC: NOLADE21ROS</b><br/>Wenn Sie eine Spendenbescheinigung empfangen möchten, geben Sie bitte bei der Überweisung auch Ihre Adresse an.', italic)
    data = [[k, kt],
            [p, pt],
            [a, at],
            [b, bt]]
    table = Table(data, colWidths=[110,400], spaceBefore=20)
    style = TableStyle([('BOX', (0,0), (-1,-1), 2, colors.orange),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (1, 0), 10),
                        ('BOTTOMPADDING',(0,3), (1,3), 10),
                        ('BACKGROUND', (0,0), (-1,-1), colors.white)])
    table.setStyle(style)
    return table


def createEventTable(start, end, eventList):
    data = []
    monthDateList = dates.daterange2(start, end)

    for date in monthDateList:
        dayPara = Paragraph(format_date(date, "d", locale='de_DE'), normal)
        weekdayPara = Paragraph(format_date(date, "E", locale='de_DE'), normal)
        descPara = createDescriptionPara(date, eventList)
        timePara = createtimePara(date, eventList)
        data.append([dayPara, weekdayPara, timePara, descPara])

    table = Table(data, colWidths=[30,30,50,400])
    style = TableStyle([('BOX', (0,0), (-1,-1), 0.5, colors.black),
                        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING',(0,0), (-1, -1), 0)])

    # create blue background on sunday
    for i in range(len(monthDateList)):
        if monthDateList[i].weekday() == 6:
            style.add('BACKGROUND', (0,i), (-1,i), colors.lightblue)



    table.setStyle(style)
    return table


def createDescriptionPara(day, eventList):
    result = []
    events = dates.getAllEventsOfDay(day, eventList, "start")
    for event in events:
        if("data" in event and event["data"]):
            para = Paragraph(event["data"], normal)
        else:
            para = Paragraph(event["description"].replace('\n', '<br/>'), normal)
        result.append(para)
    return result


def createtimePara(day, eventList):
    result = []
    events = dates.getAllEventsOfDay(day, eventList, "start")
    for event in events:
        para = Paragraph(format_time(event["starttime"], "HH:mm", locale='de_DE'), normal)
        result.append(para)
    return result

# tz = pytz.timezone('Europe/Berlin')
# start = datetime.datetime(2017,3,1, tzinfo=tz)
# end = datetime.datetime(2017,3,31, tzinfo=tz)
#
# events = caldav2.get_events(start, end)
# list = parsecal.populate_list(events, start, end)
# list = parsecal.sort_events_time(list)
#
# go(start, end, list)
