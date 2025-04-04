# data_loader.py

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def load_weather_data(station):
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "evapotranspiration", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm", "uv_index", "uv_index_clear_sky", "is_day", "sunshine_duration", "wet_bulb_temperature_2m", "cape", "lifted_index", "convective_inhibition", "freezing_level_height", "boundary_layer_height", "shortwave_radiation", "global_tilted_irradiance", "diffuse_radiation", "diffuse_radiation_instant", "shortwave_radiation_instant", "global_tilted_irradiance_instant", "direct_radiation", "direct_normal_irradiance", "terrestrial_radiation", "direct_normal_irradiance_instant", "direct_radiation_instant", "terrestrial_radiation_instant"],
        "models": "best_match"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
    hourly_rain = hourly.Variables(6).ValuesAsNumpy()
    hourly_showers = hourly.Variables(7).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(10).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(11).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(12).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(13).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(17).ValuesAsNumpy()
    hourly_evapotranspiration = hourly.Variables(18).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(19).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(20).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(21).ValuesAsNumpy()
    hourly_wind_speed_80m = hourly.Variables(22).ValuesAsNumpy()
    hourly_wind_speed_120m = hourly.Variables(23).ValuesAsNumpy()
    hourly_wind_speed_180m = hourly.Variables(24).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(25).ValuesAsNumpy()
    hourly_wind_direction_80m = hourly.Variables(26).ValuesAsNumpy()
    hourly_wind_direction_120m = hourly.Variables(27).ValuesAsNumpy()
    hourly_wind_direction_180m = hourly.Variables(28).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(29).ValuesAsNumpy()
    hourly_temperature_80m = hourly.Variables(30).ValuesAsNumpy()
    hourly_temperature_120m = hourly.Variables(31).ValuesAsNumpy()
    hourly_temperature_180m = hourly.Variables(32).ValuesAsNumpy()
    hourly_soil_temperature_0cm = hourly.Variables(33).ValuesAsNumpy()
    hourly_soil_temperature_6cm = hourly.Variables(34).ValuesAsNumpy()
    hourly_soil_temperature_18cm = hourly.Variables(35).ValuesAsNumpy()
    hourly_soil_temperature_54cm = hourly.Variables(36).ValuesAsNumpy()
    hourly_soil_moisture_0_to_1cm = hourly.Variables(37).ValuesAsNumpy()
    hourly_soil_moisture_1_to_3cm = hourly.Variables(38).ValuesAsNumpy()
    hourly_soil_moisture_3_to_9cm = hourly.Variables(39).ValuesAsNumpy()
    hourly_soil_moisture_9_to_27cm = hourly.Variables(40).ValuesAsNumpy()
    hourly_soil_moisture_27_to_81cm = hourly.Variables(41).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(42).ValuesAsNumpy()
    hourly_uv_index_clear_sky = hourly.Variables(43).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(44).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(45).ValuesAsNumpy()
    hourly_wet_bulb_temperature_2m = hourly.Variables(46).ValuesAsNumpy()
    hourly_cape = hourly.Variables(47).ValuesAsNumpy()
    hourly_lifted_index = hourly.Variables(48).ValuesAsNumpy()
    hourly_convective_inhibition = hourly.Variables(49).ValuesAsNumpy()
    hourly_freezing_level_height = hourly.Variables(50).ValuesAsNumpy()
    hourly_boundary_layer_height = hourly.Variables(51).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(52).ValuesAsNumpy()
    hourly_global_tilted_irradiance = hourly.Variables(53).ValuesAsNumpy()
    hourly_diffuse_radiation = hourly.Variables(54).ValuesAsNumpy()
    hourly_diffuse_radiation_instant = hourly.Variables(55).ValuesAsNumpy()
    hourly_shortwave_radiation_instant = hourly.Variables(56).ValuesAsNumpy()
    hourly_global_tilted_irradiance_instant = hourly.Variables(57).ValuesAsNumpy()
    hourly_direct_radiation = hourly.Variables(58).ValuesAsNumpy()
    hourly_direct_normal_irradiance = hourly.Variables(59).ValuesAsNumpy()
    hourly_terrestrial_radiation = hourly.Variables(60).ValuesAsNumpy()
    hourly_direct_normal_irradiance_instant = hourly.Variables(61).ValuesAsNumpy()
    hourly_direct_radiation_instant = hourly.Variables(62).ValuesAsNumpy()
    hourly_terrestrial_radiation_instant = hourly.Variables(63).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["visibility"] = hourly_visibility
    hourly_data["evapotranspiration"] = hourly_evapotranspiration
    hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
    hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
    hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
    hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
    hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
    hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["temperature_80m"] = hourly_temperature_80m
    hourly_data["temperature_120m"] = hourly_temperature_120m
    hourly_data["temperature_180m"] = hourly_temperature_180m
    hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
    hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
    hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
    hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
    hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
    hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
    hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
    hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
    hourly_data["soil_moisture_27_to_81cm"] = hourly_soil_moisture_27_to_81cm
    hourly_data["uv_index"] = hourly_uv_index
    hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
    hourly_data["is_day"] = hourly_is_day
    hourly_data["sunshine_duration"] = hourly_sunshine_duration
    hourly_data["wet_bulb_temperature_2m"] = hourly_wet_bulb_temperature_2m
    hourly_data["cape"] = hourly_cape
    hourly_data["lifted_index"] = hourly_lifted_index
    hourly_data["convective_inhibition"] = hourly_convective_inhibition
    hourly_data["freezing_level_height"] = hourly_freezing_level_height
    hourly_data["boundary_layer_height"] = hourly_boundary_layer_height
    hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
    hourly_data["global_tilted_irradiance"] = hourly_global_tilted_irradiance
    hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
    hourly_data["diffuse_radiation_instant"] = hourly_diffuse_radiation_instant
    hourly_data["shortwave_radiation_instant"] = hourly_shortwave_radiation_instant
    hourly_data["global_tilted_irradiance_instant"] = hourly_global_tilted_irradiance_instant
    hourly_data["direct_radiation"] = hourly_direct_radiation
    hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
    hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation
    hourly_data["direct_normal_irradiance_instant"] = hourly_direct_normal_irradiance_instant
    hourly_data["direct_radiation_instant"] = hourly_direct_radiation_instant
    hourly_data["terrestrial_radiation_instant"] = hourly_terrestrial_radiation_instant

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    print(hourly_dataframe)
    return hourly_dataframe


def get_station_list():
   stations = []
   stations.append("Europe/Rostock")
   stations.append("Europe/Berlin")
   stations.append("Europe/Hamburg")
   return stations