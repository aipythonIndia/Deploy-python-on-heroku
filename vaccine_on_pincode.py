
""" 
Developer: aipython on [29-05-2021]
website: www.aipython.in

Sends Notifications on a Telegram channel , whenever the Vaccine(s) is available at the given PINCODE 
"""

import requests
from datetime import datetime, timedelta
import time
import pytz
# from os import environ

# Define all the constants
time_interval = 10 # (in seconds) Specify the frequency of code execution
PINCODE = "110028"

tele_auth_token = "1901486933:AAHed-MGB8hVwrmK4E-gvKTVd63XNkoxvPE" # Authentication token provided by Telegram bot
tel_group_id = "test_Aug_vaccine"          # Telegram group name
IST = pytz.timezone('Asia/Kolkata')        # Indian Standard Time - Timezone
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'} # Header for using cowin api

def update_timestamp_send_Request(PINCODE):
    raw_TS = datetime.now(IST) + timedelta(days=1)      # Tomorrows date
    tomorrow_date = raw_TS.strftime("%d-%m-%Y")         # Formatted Tomorrow's date
    today_date = datetime.now(IST).strftime("%d-%m-%Y") #Current Date
    curr_time = (datetime.now().strftime("%H:%M:%S"))   #Current time
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={tomorrow_date}"
    response = requests.get(request_link, headers = header)
    raw_JSON = response.json()
    return raw_JSON, today_date, curr_time


def get_availability_data():
    slot_found_45 = False
    slot_found_18 = False
    
    raw_JSON, today_date, curr_time = update_timestamp_send_Request(PINCODE)
    print ("raw_JSON :" , raw_JSON)
    
    for cent in raw_JSON['centers']:
        for sess in cent['sessions']:
            sess_date = sess['date']
            if sess['min_age_limit'] == 45 and sess['available_capacity'] > 0:
                slot_found_45 =  True
                msg = f"For age 45+ [Vaccine Available] at {PINCODE} on {sess_date}\n\tCenter : {cent['name']}\n\tVaccine: {sess['vaccine']}\n\tDose_1: {sess['available_capacity_dose1']}\n\tDose_2: {sess['available_capacity_dose2']}"
                send_msg_on_telegram(msg)
                print (f"INFO:[{curr_time}] Vaccine Found for 45+ at {PINCODE} >> Details sent on Telegram")
                
            elif sess['min_age_limit'] == 18 and sess['available_capacity'] > 0:
                slot_found_18 =  True
                msg = f"For age 18+ [Vaccine Available] at {PINCODE} on {sess_date}\n\tCenter : {cent['name']}\n\tVaccine: {sess['vaccine']}\n\tDose_1: {sess['available_capacity_dose1']}\n\tDose_2: {sess['available_capacity_dose2']}"
                send_msg_on_telegram(msg)
                print (f"INFO: [{curr_time}] Vaccine Found for 18+ at {PINCODE} >> Details sent on Telegram")
    
    if slot_found_45 == False and slot_found_18 == False:
        print (f"INFO: [{today_date}-{curr_time}] Vaccine NOT-available for 45+ at {PINCODE}")
        print (f"INFO: [{today_date}-{curr_time}] Vaccine NOT-available for 18+ at {PINCODE}")
    elif slot_found_45 == False:
        print (f"INFO: [{today_date}-{curr_time}] Vaccine NOT-available for 45+ at {PINCODE}")
    else:
        print (f"INFO: [{today_date}-{curr_time}] Vaccine NOT-available for 18+ at {PINCODE}")
    

def send_msg_on_telegram(msg):
    telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id=@{tel_group_id}&text={msg}"
    tel_resp = requests.get(telegram_api_url)

    if tel_resp.status_code == 200:
        print ("Notification has been sent on Telegram")
    else:
        print ("Could not send Message")


if __name__ == "__main__":    
    while True:
        get_availability_data()
        time.sleep(time_interval)

