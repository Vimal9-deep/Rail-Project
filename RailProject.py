
# http://indianrailapi.com/api/v2/TrainFare/apikey/<apikey>/TrainNumber/<trainNumber>/From/<stationFrom>/To/<stationTo>/Quota/<quota>
# https://indianrailapi.com/api/v2/SeatAvailability/apikey/{apikey}/TrainNumber/{trainNumber}/From/{stationFrom}/To/{stationTo}/Date/{yyyyMMdd}/Quota/GN/Class/{classCode}

# https://indianrailapi.com/api/v2/RescheduledTrains/apikey/<apikey>/Date/<yyyyMMdd>
# https://indianrailapi.com/api/v2/FogAffectedTrains/apikey/<apikey>/
# https://indianrailapi.com/api/v2/DivertedTrains/apikey/<apikey>/Date/<yyyyMMdd>

# Flight api - 67bef5f67742a2a8c598e8a4
import requests
import pandas as pd
import datetime
import time


apiKey = "be691493b6c9d0845bb0158c1562cae7"

def TodayTime():
    current_time = datetime.datetime.now()
    return str(current_time.year)+str(current_time.month)+str(current_time.day)

# Helper Functions

# Train Schedules
def TS(trainnumber):
    traindata = requests.get("http://indianrailapi.com/api/v2/TrainSchedule/apikey/{}/TrainNumber/{}".format(apiKey, trainnumber)).json()
    return pd.DataFrame(traindata)['Route']
# Special Trains
def SP():
    specialtraindata = requests.get("https://indianrailapi.com/api/v2/SpecialTrains/apikey/{}/".format(apiKey)).json()
    return pd.DataFrame(specialtraindata['Trains'])
# Cancelled Trains
def CancelTrains():
    cancelledTrain = requests.get("https://indianrailapi.com/api/v2/CancelledTrains/apikey/{}/Date/{}".format(apiKey , TodayTime())).json()
    return pd.DataFrame(cancelledTrain)
# Coach Position
def CP(trainnumber):
    cp = requests.get("http://indianrailapi.com/api/v2/CoachPosition/apikey/{}/TrainNumber/{}".format(apiKey, trainnumber)).json()
    return pd.DataFrame(cp)
# Station Name to Code
def StationNametoCode(StationName):
    station = requests.get("http://indianrailapi.com/api/v2/StationCodeToName/apikey/{}/StationCode/{}".format(apiKey, StationName)).json()
    return pd.DataFrame(station)['Station']['StationCode']
# Station Code to Name
def StationCodetoName(StationCode):
    station = requests.get("http://indianrailapi.com/api/v2/StationCodeToName/apikey/{}/StationCode/{}".format(apiKey, StationCode)).json()
    return pd.DataFrame(station)['Station']['NameEn']
# Station Code to Hindi Name
def StationHindiName(StationCode):
    station = requests.get("http://indianrailapi.com/api/v2/StationCodeToName/apikey/{}/StationCode/{}".format(apiKey, StationCode)).json()
    return pd.DataFrame(station)['Station']['NameHn']
# Station Code to Longitude
def StationLongitude(StationCode):
    station = requests.get("http://indianrailapi.com/api/v2/StationCodeToName/apikey/{}/StationCode/{}".format(apiKey, StationCode)).json()
    return pd.DataFrame(station)['Station']['Longitude']
# Station Code to Latitude
def StationLatitude(StationCode):
    station = requests.get("http://indianrailapi.com/api/v2/StationCodeToName/apikey/{}/StationCode/{}".format(apiKey, StationCode)).json()
    return pd.DataFrame(station)['Station']['Latitude']
# Trains Between Stations
def TrainBetweenStations(From, To):
    trains = requests.get("http://indianrailapi.com/api/v2/TrainBetweenStation/apikey/{}/From/{}/To/{}/".format(apiKey, From, To)).json()
    return pd.DataFrame(trains)
# Train Information
def TrainInformation(trainnumber):
    info = requests.get("http://indianrailapi.com/api/v2/TrainInformation/apikey/{}/TrainNumber/{}".format(apiKey , trainnumber)).json()
    return pd.DataFrame(info)
# Fog affected Trains
def FG():
    fg = requests.get("https://indianrailapi.com/api/v2/FogAffectedTrains/apikey/{}".format(apiKey)).json()
    return pd.DataFrame(fg)
# Rescheduled Trains
def RS():
    rs = requests.get("https://indianrailapi.com/api/v2/RescheduledTrains/apikey/{}/Date/{}".format(apiKey,TodayTime())).json()
    return pd.DataFrame(rs)
# Diverted Trains
def DT():
    dt = requests.get("https://indianrailapi.com/api/v2/DivertedTrains/apikey/{}/Date/{}".format(apiKey , TodayTime())).json()
    return pd.DataFrame(dt)
# Original Functions


def SpecialTrain():
    SpecialPanda = SP()
    dayrun = []
    print(f"{'TrainNumber':<15}{'TrainName':<30}{'Source':<20}{'Departure':<15}{'Destination':<20}{'Arrival':<15}{'ValidFrom':<15}{'ValidTo':<15}{'TravelTime':<15}{'Run on':<15}\n")
    for i in range(len(SpecialPanda)):
        if i == 10 :
            break
        days = SpecialPanda['Days'][i]
        for j in range(7):
            if days[j]['Available'] == 'Y':
                dayrun = str(days[j]['Name'])
        print(f"{SpecialPanda['TrainNumber'][i]:<15}{SpecialPanda['TrainName'][i]:<30}{StationCodetoName(SpecialPanda['Source'][i]):<20}{SpecialPanda['Departure'][i]:<15}{StationCodetoName(SpecialPanda['Destination'][i]):<20}{SpecialPanda['Arrival'][i]:<15}{SpecialPanda['ValidFrom'][i]:<15}{SpecialPanda['ValidTo'][i]:<15}{SpecialPanda['TravelTime'][i]:<15}{dayrun:<15}")
    user_Train_search = input("\nEnter the Train number to search for : ")
    print(f"{'TrainNumber':<15}{'TrainName':<30}{'Source':<15}{'Departure':<15}{'Destination':<15}{'Arrival':<15}{'ValidFrom':<15}{'ValidTo':<15}{'TravelTime':<15}{'Running Days':<15}\n")
    for i in range(len(SpecialPanda)):
        if SpecialPanda["TrainNumber"][i] == user_Train_search:
            print(f"{SpecialPanda['TrainNumber'][i]:<15}{SpecialPanda['TrainName'][i]:<30}{StationCodetoName(SpecialPanda['Source'][i]):<15}{SpecialPanda['Departure'][i]:<15}{StationCodetoName(SpecialPanda['Destination'][i]):<15}{SpecialPanda['Arrival'][i]:<15}{SpecialPanda['ValidFrom'][i]:<15}{SpecialPanda['ValidTo'][i]:<15}{SpecialPanda['TravelTime'][i]:<15}{dayrun:<15}")
            break
    else:
        print("Train Not Found Check again...")
def TodayCancelledTrains():
    if len(CancelTrains()) == 0:
        print("No Trains are Cancelled Today")
    else:
        print(f"{'TrainNumber':<15}{'TrainName':<30}{'Source':<15}{'Destination':<15}{'Date':<15}{'Status':<15}\n")
        for i in range(len(CancelTrains())):
            print(f"{CancelTrains()['TrainNumber'][i]:<15}{CancelTrains()['TrainName'][i]:<30}{CancelTrains()['Source'][i]:<15}{CancelTrains()['Destination'][i]:<15}{CancelTrains()['Date'][i]:<15}{CancelTrains()['Status'][i]:<15}")
def CoachPositions():
    user_train_number = int(input("Enter the Train Number for See Coach Position: "))
    coachPositionPanda =  CP(user_train_number)
    Coaches = []
    print("Total number of Coaches in the Train : ", len(coachPositionPanda['Coaches']))
    for i in range(len(coachPositionPanda['Coaches'])):
       Coaches.append(coachPositionPanda['Coaches'][i]['Name'])
    for ch in range(len(Coaches)):
        print(Coaches[ch] , end="--x--")
def TrainData():
    user_Train_number = input("Enter the Train Number: ")
    traindata = TrainInformation(user_Train_number)
    print("TrainName : " ,traindata['TrainName'])
    print("Source : " ,StationCodetoName(traindata['Source']['Code']))
    print("Arrival Time : ",traindata['Source']['Arrival'])
    print("Destination : ",StationCodetoName(traindata['Destination']['Code']))
    print("Destination Time : ",traindata['Destination']['Arrival'])
def TrainSchedules():
    user_train_number = input("Enter the Train Number: ")
    traindata = TS(user_train_number)
    print(f"{'Station Name':<30}{'Arrival Time':<15}{'Departure Time':<15}{'Distance':<15}{'Day':<15}\n")
    for i in range(len(traindata)):
        print(f"{traindata[i]['StationName']:<30}{str(traindata[i]['ArrivalTime']):<15}{str(traindata[i]['DepartureTime']):<15}{str(traindata[i]['Distance']):<15}{str(traindata[i]['Day']):<15}")
    
def TrainProblem():
    fogaffected = FG()
    reschedule = RS()
    Diverted = DT()
    if len(fogaffected['TotalTrain']) > 0 or len(reschedule['TotalTrain']) > 0 or len(Diverted['TotalTrain']) > 0 :
        print("Following issues are affecting your train:")
        if len(fogaffected['TotalTrain']) > 0 :
            print("\nFog Affected Trains:\n")
            print(f"{"Train Number":<15}{"Train Name":<30}{"Source":<20}{"Next Station":<20}{"Destination":<20}{"Expected Arrival":<15}{"Status":<20}")
            for i in range(len(fogaffected['TotalTrain'])):
                if i == 5:
                    break
                print(f"{str(fogaffected['Trains'][i]['TrainNo'])}{fogaffected['TrainName'][i]['TrainName']}{fogaffected['TrainName'][i]['Source']}{fogaffected['TrainName'][i]['NextStation']}{fogaffected['TrainName'][i]['LastStation']}{str(fogaffected['TrainName'][i]['ExpectedArrival'])}{fogaffected['TrainName'][i]['Status']}")
        if len(reschedule['TotalTrain']) > 0 :
            print("\nRescheduled Trains:\n")
            print(f"{"Train Number":<15}{"Train Name":<30}{"Source":<20}{"Destination":<20}{"Reschedule Time":<20}{"Reschedule Date":<20}{"Train Tye":<15}")
            for i in range(len(reschedule['TotalTrain'])):
                if i == 5:
                    break
                print(f"{str(reschedule['Trains'][i]['TrainNumber'])}{reschedule['TrainName'][i]['TrainName']}{reschedule['TrainName'][i]['Source']}{reschedule['TrainName'][i]['Destination']}{str(reschedule['TrainName'][i]['RescheduledTime'])}{str(reschedule['TrainName'][i]['RescheduledDate'])}{reschedule['TrainName'][i]['TrainType']}")
        if len(Diverted['TotalTrain']) > 0 :
            print("\nDiverted Trains:\n")
            print(f"{"Train Number":<15}{"Train Name":<30}{"Source":<20}{"Diverted From":<20}{"New Destination":<20}{"Old Destination":<20}{"Diverted Date":<15}{"Train Type":<20}")

            for i in range(len(Diverted['TotalTrain'])):
                if i == 5:
                    break
                print(f"{str(Diverted['Trains'][i]['TrainNumber'])}{Diverted['TrainName'][i]['TrainName']}{Diverted['TrainName'][i]['Source']}{Diverted['TrainName'][i]['DivertedFrom']}{Diverted['TrainName'][i]['DivertedTo']}{Diverted['TrainName'][i]['Destination']}{str(Diverted['TrainName'][i]['StartDate'])}{Diverted['TrainName'][i]['TrainType']}")
    else:
        print("No issues are affecting your train.")
    user_choice = input("\nDo You want to Check any Trains (Y/N): ").lower()
    if user_choice == 'y':
        user_Train = int(input("Enter Your Train Number: "))
        for i in range(len(fogaffected['TotalTrain'])):
            if fogaffected['Trains'][i]['TrainNo'] == user_Train:
                print("Train Name :", fogaffected['TrainName'][i]['TrainName'])
                print("Source :", fogaffected['TrainName'][i]['Source'])
                print("Next Station :", fogaffected['TrainName'][i]['NextStation'])
                print("Destination :" ,fogaffected['TrainName'][i]['LastStation'])
                print("Expected Arrival :", fogaffected['TrainName'][i]['ExpectedArrival'])
                print("Status :", fogaffected['TrainName'][i]['Status'])
                break
            else:
                continue
        for i in range(len(reschedule['TotalTrain'])):
            if reschedule['Trains'][i]['TrainNumber'] == user_Train:
                print("Train Name :", reschedule['TrainName'][i]['TrainName'])
                print("Source :", reschedule['TrainName'][i]['Source'])
                print("Destination :", reschedule['TrainName'][i]['Destination'])
                print("Reschedule Time :", reschedule['TrainName'][i]['RescheduledTime'])
                print("Reschedule Date :", reschedule['TrainName'][i]['RescheduledDate'])
                print("Train Type :", reschedule['TrainName'][i]['TrainType'])
                break
            else:
                continue
        for i in range(len(Diverted['TotalTrain'])):
            if Diverted['Trains'][i]['TrainNumber'] == user_Train:
                print("Train Name :", Diverted['TrainName'][i]['TrainName'])
                print("Source :", Diverted['TrainName'][i]['Source'])
                print("Destination :", Diverted['TrainName'][i]['Destination'])
                print("Reschedule Time :", Diverted['TrainName'][i]['RescheduledTime'])
                print("Reschedule Date :", Diverted['TrainName'][i]['RescheduledDate'])
                print("Train Type :", Diverted['TrainName'][i]['TrainType'])
                break
            else:
                continue
    else:
        print("Thank You!")
                

def user_input():
    print("\nWelcome to Indian Railway API\n")
    print("Available options:\n")
    user_input = int(
                  input(
                       "Enter the choice:\n"
                       "1. Check For Special Trains\n"
                       "2. Check For Today Cancelled Trains\n"
                       "3. Check Train Coach Position\n"
                       "4. Check Train Between Stations\n"
                       "5. Check Train Schedule\n"
                       "6. Know Your Train\n"
                       "7. All Trains in Your Station\n"
                       "8. Check for Seat \n"
                       "9. Train Fare\n"
                       "10. All Cancelled , Reschedules and Diverted Trains\n"
                       "0. Exit\n"
                       "---------------------------------------\n"
                       "Your Choice : "
                       )
                  )
    return user_input
    
def get_user():
    user_choice = user_input()
    print("Taking Approval from Modiji....")
    time.sleep(2)
    while(user_choice != 0):
        if user_choice == 1:
            SpecialTrain()
        elif user_choice == 2:
            TodayCancelledTrains()
        elif user_choice == 3:
            CoachPositions()
        elif user_choice == 4:
            print('working')
        elif user_choice == 5:
            TrainSchedules()
        elif user_choice == 6:
            TrainData()
        user_choice = user_input()
    print("Thank You!")
# get_user()



