import Configuration
import pandas as pd
import time
import requests
import json

df = pd.read_csv('Pin_code.csv');

# def getAPIKey():
#     if(Configuration.INDEX >= len(Configuration.API_KEY)): Configuration.INDEX = 0;
#     KEY = Configuration.API_KEY[Configuration.INDEX];
#     Configuration.INDEX += 1;
#     Configuration.API_KEY_COUNT[Configuration.INDEX] += 1;
#     print(f"Using API Key: {KEY}. Use Count: {Configuration.API_KEY_COUNT[Configuration.INDEX]}")
#     return KEY;

def getAPIKey():
    if Configuration.INDEX >= len(Configuration.API_KEY): Configuration.INDEX = 0;
    KEY = Configuration.API_KEY[Configuration.INDEX];
    Configuration.API_KEY_COUNT[Configuration.INDEX] += 1;

    print(f"Using API Key: {KEY}. Use Count: {Configuration.API_KEY_COUNT[Configuration.INDEX]}")
    Configuration.INDEX += 1;
    return KEY;

def getLatLong(PIN , COUNTRY = 'India'):
    API_KEY = getAPIKey();
    API = f'https://us1.locationiq.com/v1/search?key={API_KEY}&q={PIN}%2C%20{COUNTRY}&format=json&'
    # count += 1;

    print(f"Running code for PIN {PIN}")
    try:
        response = requests.get(API)

        if response.status_code == 200:
            API_DATA = response.json()

            if API_DATA:
                INFO = {
                    "LAT": API_DATA[0]['lat'],
                    "LONG": API_DATA[0]['lon']
                }

                return INFO;
            else:
                print(f"Empty response for {PIN}")
                return {};
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        print(f"Exception: {e}")
        return {}
    # finally:
        # Introduce a delay of 1 second to comply with the rate limit
        # time.sleep(1)

# print(getLatLong(110063));
 
# sample_df = df.sample(n=10);
start_time = time.time()
location_info_df = df['PIN Code'].apply(getLatLong).apply(pd.Series)
print("--- %s seconds ---" % (time.time() - start_time))

# # Concatenation of the requested data and the PIN Codes
df = pd.concat([df, location_info_df], axis=1)
df = df.rename(columns={0: 'Latitude', 1: 'Longitude', 2: 'Display Name'})
print(df)

df.to_csv('PinLatLong.csv')