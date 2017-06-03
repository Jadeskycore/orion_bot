def get_current_weather(data):
    return f"""
    `Current weather for {data['country']} {data['tz_id']}`
    `Localtime {data['localtime']}`
        *Outside - {data['condition']['text']}*
        *Temperature - {data['temp_c']} °C*
        *Wind speed - {data['wind_kph']} km/h*
        *Humidity - {data['humidity']}%*
    """