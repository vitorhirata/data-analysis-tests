from darksky import forecast
from datetime import datetime as dt

lat = -23.496111
lon = -46.619722
#key =

SP = key, lat, lon

days = list(range(1,31))
data = []

for day in days:
    t = dt(2018, 1, day, 12).isoformat()
    sp_forecast = forecast(*SP, time=t)

    historic_temperature = sp_forecast.temperature
    forecast_temperature = sp_forecast.daily[1].temperature

    historic_data = [day, false, historic_temperature]
    forecast_data = [day+1, true, forecast_temperature]
    data.append()


# criar um hash com as chaves sendo todas as measure_date's (31 dias) e valores sendo um array vazio
# itera sobre esse array e cria um objeto forecast passando a data de medida daquele dia como parametro
# fazendo forecast.hourly[12].temperature pegamos a temperatura daque

    # add uma linha com dia atual, forecast = false, temperatura atual
    # add uma linha com dia seguinte, forecast = true, temperatura do dia seguinte (usando daily[1])
    # formato da linha: 'dia': [true/false, temperatura]

# data_frame = pd.DataFrame(data=hash)

