from darksky import forecast
from datetime import datetime as dt

lat = -23.496111
lon = -46.619722
key = "e47af14366cf19af277cfdbf17288458"

SP = key, lat, lon
t = dt(2018, 1, 1, 12).isoformat()
sp_forecast = forecast(*SP, time=t)
