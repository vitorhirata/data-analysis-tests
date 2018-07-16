from darksky import forecast
from datetime import datetime as dt
from secrets impot API_KEY

lat = -23.496111
lon = -46.619722
key = API_KEY

SP = key, lat, lon
t = dt(2018, 1, 1, 12).isoformat()
sp_forecast = forecast(*SP, time=t)
