import datetime
import sys
import os.path

STARTING_YEAR = 1996
ENDING_YEAR = 2011
TOTAL_YEARS = 2011-1996
FILES_PREFIX = "lahore_weather_"
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DATE_INDEX = 0
MAX_TEMP_INDEX = 1
MIN_TEMP_INDEX = 3
MAX_HUMIDITY_INDEX = 7
MIN_HUMIDITY_INDEX = 9


def displayReportOne(report):
    print("{:<20} {:<20} {:<20} {:<20} {:<20}".format(
        'Year', 'Max Temp', 'Min Temp', 'Max Humidity', 'Min Humidity'))
    print("{:<20} {:<20} {:<20} {:<20} {:<20}".format(
        '.'*20, '.'*20, '.'*20, '.'*20, '.'*20))

    for data in report:
        print("{:<20} {:<20} {:<20} {:<20} {:<20}".format(
            data['year'].split('-')[0], data['maxTemp'], data['minTemp'], data['maxHumidity'], data['minHumidity']))


def displayReportTwo(report):
    print("{:<20} {:<20} {:<20}".format(
        'Year', 'Date', 'Temp'))
    print("{:<20} {:<20} {:<20}".format(
        '.'*20, '.'*20, '.'*20))

    for data in report:
        dayDate = datetime.datetime.strptime(
            data['date'], "%Y-%m-%d").strftime("%d/%m/%y")
        print("{:<20} {:<20} {:<20}".format(
            data['date'].split('-')[0], dayDate, data['maxTemp']))


def getReportForMonth(weatherData, reportType):
    maxTemp = -100
    maxHumidity = 0
    minTemp = 100
    minHumidity = 100
    date = None
    monthlyRecord = None

    for index in range(len(weatherData)-1):
        date = weatherData[index].split(',')[DATE_INDEX]
        dailyMaxTemp = weatherData[index].split(',')[MAX_TEMP_INDEX]
        dailyMinTemp = weatherData[index].split(',')[MIN_TEMP_INDEX]
        dailyMaxHumidity = weatherData[index].split(',')[MAX_HUMIDITY_INDEX]
        dailyMinHumidity = weatherData[index].split(',')[MIN_HUMIDITY_INDEX]

        if(reportType == 2):
            if(date.strip() == '' or dailyMaxTemp.strip() == ''):
                continue
            if(int(dailyMaxTemp) > maxTemp):
                maxTemp = int(dailyMaxTemp)
                monthlyRecord = {
                    'date': date, 'maxTemp': int(dailyMaxTemp)}
        else:
            if(date.strip() == '' or dailyMaxTemp.strip() == '' or dailyMinTemp.strip() == '' or dailyMaxHumidity.strip() == '' or dailyMinHumidity.strip() == ''):
                continue

            maxTemp = max(int(dailyMaxTemp), maxTemp)
            minTemp = min(int(dailyMinTemp), minTemp)
            minHumidity = min(int(dailyMinHumidity), minHumidity)
            maxHumidity = max(int(dailyMaxHumidity), maxHumidity)

    if(reportType == 2):
        return monthlyRecord
    else:
        return {'date': date, 'maxTemp': maxTemp, 'minTemp': minTemp, 'maxHumidity': maxHumidity, 'minHumidity': minHumidity}


def fetchRequiredReport(reportType):
    report = []
    maxTemp = -100
    maxHumidity = 0
    minTemp, minHumidity = 100, 100
    monthlyReport = None
    yearlyRecord = None

    for year in range(STARTING_YEAR, ENDING_YEAR+1):
        for monthIndex in range(len(MONTH_NAMES)):
            try:
                fileData = open(
                    f"{sys.argv[2]}/{FILES_PREFIX}{year}_{MONTH_NAMES[monthIndex]}.txt")
                fileData.readline()
                fileData.readline().split(',')
                weatherData = fileData.readlines()
                monthlyReport = getReportForMonth(weatherData, reportType)
                if(reportType == 2):
                    if(monthlyReport['maxTemp'] > maxTemp):
                        yearlyRecord = {
                            'date': monthlyReport['date'], 'maxTemp': monthlyReport['maxTemp']}
                else:
                    maxTemp = max(monthlyReport['maxTemp'], maxTemp)
                    minTemp = min(monthlyReport['minTemp'], minTemp)
                    minHumidity = min(
                        monthlyReport['minHumidity'], minHumidity)
                    maxHumidity = max(
                        monthlyReport['maxHumidity'], maxHumidity)
            except:
                continue
        if(reportType == 2):
            report.append(yearlyRecord)
        else:
            report.append({'year': monthlyReport['date'], 'maxTemp': maxTemp, 'minTemp': minTemp,
                           'maxHumidity': maxHumidity, 'minHumidity': minHumidity})
        maxTemp = -100
        maxHumidity = 0
        minTemp, minHumidity = 100, 100
    return report


def getReportOne():
    reportOne = fetchRequiredReport(1)
    displayReportOne(reportOne)


def getReportTwo():
    reportTwo = fetchRequiredReport(2)
    displayReportTwo(reportTwo)


def driver():
    if(len(sys.argv) == 3):
        if(not os.path.isdir(f"{sys.argv[2]}")):
            print("No record directory found!")
            return
        if(sys.argv[1] == '1'):
            getReportOne()
        elif(sys.argv[1] == '2'):
            getReportTwo()
        else:
            print("Invalid report number. Please try again.")
    else:
        print("""
    Error: Invalid Command line arguments added.
            
    Usage: python3 weatherman.py [report#] [data_dir]

    [Report #]
    1 for Annual Max/Min Temperature
    2 for Hottest day of each year

    [data_dir]
    Directory containing weather data files
        """)


driver()
