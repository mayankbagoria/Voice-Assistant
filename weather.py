"""
# **module auther : Mayank Bagoria**
"""

import requests

directions = {
    "N": "North",
    "NNE": "North-Northeast",
    "NE": "Northeast",
    "ENE": "East-Northeast",
    "E": "East",
    "ESE": "East-Southeast",
    "SE": "Southeast",
    "SSE": "South-Southeast",
    "S": "South",
    "SSW": "South-Southwest",
    "SW": "Southwest",
    "WSW": "West-Southwest",
    "W": "West",
    "WNW": "West-Northwest",
    "NW": "Northwest",
    "NNW": "North-Northwest"
}

air_quality ={
    "1": "Good",
    "2": "Moderate",
    "3": "Unhealthy for sensitive group",
    "4": "Unhealthy",
    "5": "Very Unhealthy",
    "6": "Hazardous"
}

def aqi_report(city,aqi_api):
    url = "https://api.waqi.info/search/"

    params = {
        'keyword': city,
        'token': aqi_api
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()["data"]

        aqi = []
        name =[]

        for ar in data:
            aqi.append(int(ar["aqi"]))
            name.append(ar["station"]["name"])
            
        return int(sum(aqi)/len(aqi))
    except :
        pass

def weatherf(city,weather_api,aqi_api):
    url = "http://api.weatherapi.com/v1/forecast.json"

    params = {
        'key': weather_api,
        'q': f"{city}-india",
        'days': 1,
        'aqi': "yes",
        'alerts': "yes"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    aqi = aqi_report(city,aqi_api)

    report = f"""
-------------------------
Weateher Report
Location                :   {data["location"]["name"]}, {data["location"]["region"]}, {data["location"]["country"]}
Current Temperature     :   {data["current"]["temp_c"]}°C
Maximum Temperature     :   {data["forecast"]["forecastday"][0]["day"]["maxtemp_c"]}°C
Minimum Temperature     :   {data["forecast"]["forecastday"][0]["day"]["mintemp_c"]}°C
Avgerage Temperature    :   {data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]}°C
Condition               :   {data["current"]["condition"]["text"]}
Wind                    :   {data["current"]["wind_kph"]} Km/h
Wind direction          :   {directions[f"{data["current"]["wind_dir"]}"]}
Air Quality             :   {air_quality[f"{data["forecast"]["forecastday"][0]["day"]["air_quality"]["us-epa-index"]}"]}
Avgerage Humidity       :   {data["forecast"]["forecastday"][0]["day"]["avghumidity"]}%
Chance Of Rain          :   {data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]}%
Sunrise                 :   {data["forecast"]["forecastday"][0]["astro"]["sunrise"]}
Sunset                  :   {data["forecast"]["forecastday"][0]["astro"]["sunset"]}
Moon Phase              :   {data["forecast"]["forecastday"][0]["astro"]["moon_phase"]}

{data["alerts"]["alert"]["headline"] if data["alerts"]["alert"] else "-------------------------"}"""

    aqi_rep = f"""Air Quality Index (AQI)
AQI         :   {aqi}
Quality     :   {air_quality[f"{data["forecast"]["forecastday"][0]["day"]["air_quality"]["us-epa-index"]}"]}
co          :   {data["forecast"]["forecastday"][0]["day"]["air_quality"]["co"]:.2f} μg/m3
no2         :   {data["forecast"]["forecastday"][0]["day"]["air_quality"]["no2"]:.2f} μg/m3
o3          :   {data["forecast"]["forecastday"][0]["day"]["air_quality"]["o3"]:.2f} μg/m3
so2         :   {data["forecast"]["forecastday"][0]["day"]["air_quality"]["so2"]:.2f} μg/m3
pm2.5       :   {data["forecast"]["forecastday"][0]["day"]["air_quality"]["pm2_5"]:.2f} μg/m3
pm10        :   {data["forecast"]["forecastday"][0]["day"]["air_quality"]["pm10"]:.2f} μg/m3
"""

    ert = f"Today in {data["location"]["name"]}, {data["location"]["region"]}, it'll be mostly {data["current"]["condition"]["text"]} with a temperature of {data["current"]["temp_c"]} degree celcius. winds at {data["current"]["wind_kph"]} kilometer per hour in {directions[f"{data["current"]["wind_dir"]}"]} direction. AQI is {aqi} and air quality is {air_quality[f"{data["forecast"]["forecastday"][0]["day"]["air_quality"]["us-epa-index"]}"]}. further details is printing below"
    return (
        ert,
        report,
        aqi_rep,
    )