import datetime
import sys
import os.path

STARTING_YEAR = 1996#Specified starting year
ENDING_YEAR = 2011#Specified ending year
TOTAL_YEARS = ENDING_YEAR-STARTING_YEAR
FILES_PREFIX = "lahore_weather_"#Each file has a name prefix

#Month names as per files. Could have also used Calender library
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

DATE_INDEX = 0#Date index in the file data
MAX_TEMP_INDEX = 1#Maximum temperature index in the file data
MIN_TEMP_INDEX = 3#Minimum Temperature index in the file data
MAX_HUMIDITY_INDEX = 7#maximum humidity index in the file data
MIN_HUMIDITY_INDEX = 9#minimum humidity index in the file data


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


#Parameters:
#   weatherData: Gets the weather data list of string as a parameter
#   report type: Which report is needed by the user. 1 or 2
def getReportForMonth(weatherData, reportType):
    maxTemp = -100
    maxHumidity = 0
    minTemp = 100
    minHumidity = 100
    date = None
    monthlyRecord = None

    for index in range(len(weatherData)-1):
        #Each record is lined and comma separated
        date = weatherData[index].split(',')[DATE_INDEX]
        dailyMaxTemp = weatherData[index].split(',')[MAX_TEMP_INDEX]
        dailyMinTemp = weatherData[index].split(',')[MIN_TEMP_INDEX]
        dailyMaxHumidity = weatherData[index].split(',')[MAX_HUMIDITY_INDEX]
        dailyMinHumidity = weatherData[index].split(',')[MIN_HUMIDITY_INDEX]

        if(reportType == 2):
            if(date.strip() == '' or dailyMaxTemp.strip() == ''):#Check if the required report data fields are empty
                continue
            if(int(dailyMaxTemp) > maxTemp):
                maxTemp = int(dailyMaxTemp)
                monthlyRecord = {
                    'date': date, 'maxTemp': int(dailyMaxTemp)}#Save the temperature if it is maximum for the given year
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
    report = []#List to hold the required records
    maxTemp = -100#Minimum weather temperature taken
    maxHumidity = 0#Humidity is between 0 to 100%
    minTemp, minHumidity = 100, 100
    monthlyReport = None
    yearlyRecord = None

    for year in range(STARTING_YEAR, ENDING_YEAR+1):
        for monthIndex in range(len(MONTH_NAMES)):
            try:
                fileData = open(
                    f"{sys.argv[2]}/{FILES_PREFIX}{year}_{MONTH_NAMES[monthIndex]}.txt")
                fileData.readline()#Empty line at the start. Move the file cursor to the next line
                fileData.readline().split(',')
                weatherData = fileData.readlines()#Read the rest of the lines as they all contains the data
                monthlyReport = getReportForMonth(weatherData, reportType)#Receive monthly report depending upon the required report type
                if(monthlyReport == None):
                    break
                if(reportType == 2):
                    if(monthlyReport['maxTemp'] > maxTemp):
                        yearlyRecord = {
                            'date': monthlyReport['date'], 'maxTemp': monthlyReport['maxTemp']}#Store the temperature as a max if the monthly temperature has greater temperature than the Previous months
                else:
                    maxTemp = max(monthlyReport['maxTemp'], maxTemp)#Get max temperature
                    minTemp = min(monthlyReport['minTemp'], minTemp)#Minimum
                    minHumidity = min(
                        monthlyReport['minHumidity'], minHumidity)
                    maxHumidity = max(
                        monthlyReport['maxHumidity'], maxHumidity)
            except:
                continue
        if(reportType == 2):
            if(monthlyReport):
                report.append(yearlyRecord)
        else:
            if(monthlyReport):
                report.append({'year': monthlyReport['date'], 'maxTemp': maxTemp, 'minTemp': minTemp,
                               'maxHumidity': maxHumidity, 'minHumidity': minHumidity})
        maxTemp = -100
        maxHumidity = 0
        minTemp, minHumidity = 100, 100
    return report


def getReportOne():
    reportOne = fetchRequiredReport(1)
    reportOne = [i for i in reportOne if i]
    displayReportOne(reportOne)


def getReportTwo():
    reportTwo = fetchRequiredReport(2)
    reportTwo = [i for i in reportTwo if i]
    displayReportTwo(reportTwo)


def driver():
    if(len(sys.argv) == 3):#check if the user has entered 3 arguments.
        if(not os.path.isdir(f"{sys.argv[2]}")):#Checking if the data directory that the user has entered exists
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
