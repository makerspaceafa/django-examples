import requests
from django.shortcuts import render

# lat e long globais para ele se lembrar quais foram as ultimas inseridas
lat: str = '38.8369'
long: str = '-9.3464'


# Create your views here.
def index(request):
    # indicar que ao usar estes nomes dentro da função index, estamo-nos a referir ao lat e long globais.
    # Se não fizermos isto, o python vai pensar que são variáveis diferentes que só existem dentro da função index.
    global lat, long

    ############################################################
    # ### Fazer render da página (tanto no POST com no GET)  ###
    ############################################################

    if request.method == 'POST':
        lat = request.POST['lat']
        long = request.POST['long']
        # todo: use lat.isnumeric() and long.isnumeric() to enforce proper input

    ############################################################
    # ### Fazer render da página (tanto no POST com no GET)  ###
    ############################################################

    # ------ Reverse Geolocation API -> get location data --------------------------------------------------------------

    # Estamos a usar o API do OpenStreetMap, que não requer registo para obter uma API key.
    geo_url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={long}&format=jsonv2&accept-language=pt_pt'

    # Com o módulo requests, fazemos um GET ao endpoint do API e extraímos o json
    place: dict = requests.get(geo_url).json()

    # ----- Esta secção tem a ver com a extração dos dados que queremos do json obtido acima
    # Documentação do API -> https://nominatim.org/release-docs/develop/api/Reverse/

    # Esta variável "location" vai guardar a informação sobre o local que queremos que apareça no website.
    # Se vier um erro dentro do json, passamos um aviso.
    # A causa mais comum é não haver dados de morada para as coordenadas inseridas -> oceano
    if 'error' in place.keys():
        location = 'Reverse geocode failed. Possivelmente oceano?'
    else:
        # Aqui, caso não haja erro, vamos extrair a informação que queremos mostrar e gerar uma string.
        # Começamos por inicializar "location" com um array vazio, e adicionamos os elementos que pretendemos extrair...
        # ... se eles existirem no json.
        location = []
        # Raramente, 'name' vem com o valor None, mas é um campo que existe sempre.
        # Por isso não é necessário testar a sua existência mas.
        # ↓ Este if é porque não o queremos adicionar à string final se for None, e "if None" dá falso 👍
        if place['name']:
            location.append(place['name'])

        # Estes dois campos, às vezes não aparecem no json, por isso temos que testar a sua existência.
        # Escolhi estes dois após testar algumas coordenadas diferentes e ver que gostava da informação que davam.
        if 'county' in place['address'].keys():
            location.append(place['address']['county'])
        if 'country' in place['address'].keys():
            location.append(place['address']['country'])

        # Aqui usamos o método join() para juntar todos os elementos do array com um ', ' no meio deles
        # e metemos o resultado dentro da variável "location", que passou de ser do tipo "list" para o tipo "str"
        location = ', '.join(location)
        # No website, o display vai ser algo do género "Pontão do Tamariz, Lisboa, Portugal".
        # No entanto pode ser muito menos específico, até mesmo apenas "Portugal, Portugal"
        # caso as coordenadas correspondam a terras sem nome perdidas no interior.
    # ------------------------------------------------------------------------------------------------------------------

    # ------ Weather API -> get weather data ---------------------------------------------------------------------------

    # Estamos a usar o API da 7Timer, por ser grátis e não ser necessária uma API key
    weather_url = f'http://www.7timer.info/bin/api.pl?lon={long}&lat={lat}&product=civillight&output=json'

    # Com o módulo requests, fazemos um GET ao endpoint do API e extraímos o json
    weather: dict = requests.get(weather_url).json()
    '''
    ############################################################################################
    ### Detalhes sobre o processamento deste JSON: que informação e como estamos a extraí-la ###
    ############################################################################################

    weather['dataseries'] is a list of 7 dicts for today and the next 6 days. Ex:
    [
      {'date': 20210209, 'weather': 'clear', 'temp2m': {'max': 13, 'min': 13}, 'wind10m_max': 5},
      {'date': 20210210, 'weather': 'lightrain', 'temp2m': {'max': 14, 'min': 13}, 'wind10m_max': 4},
      {'date': 20210211, 'weather': 'lightrain', 'temp2m': {'max': 15, 'min': 13}, 'wind10m_max': 4},
      {'date': 20210212, 'weather': 'clear', 'temp2m': {'max': 15, 'min': 12}, 'wind10m_max': 3},
      {'date': 20210213, 'weather': 'clear', 'temp2m': {'max': 16, 'min': 11}, 'wind10m_max': 3},
      {'date': 20210214, 'weather': 'cloudy', 'temp2m': {'max': 16, 'min': 13}, 'wind10m_max': 3},
      {'date': 20210215, 'weather': 'cloudy', 'temp2m': {'max': 15, 'min': 13}, 'wind10m_max': 3}
    ]

    weather['dataseries'][0] gives the data for today.

    We can understand what will come out of this by studying the API reference:
    >>> http://www.7timer.info/doc.php?lang=en#civillight <<<

    The possible values and meanings of the 'weather' field are as follows:
      - 'clear'     Total cloud cover less than 20%
      - 'pcloudy'   Total cloud cover between 20%-60%
      - 'mcloudy'   Total cloud cover between 60%-80%
      - 'cloudy'    Total cloud cover over over 80%
      - 'humid'     Relative humidity over 90% with total cloud cover less than 60%
      - 'lightrain' Precipitation rate less than 4mm/hr with total cloud cover more than 80%
      - 'oshower'   Precipitation rate less than 4mm/hr with total cloud cover between 60%-80%
      - 'ishower'   Precipitation rate less than 4mm/hr with total cloud cover less than 60%
      - 'lightsnow' Precipitation rate less than 4mm/hr
      - 'rain'      Precipitation rate over 4mm/hr
      - 'snow'      Precipitation rate over 4mm/hr
      - 'rainsnow'  Precipitation type to be ice pellets or freezing rain

    First we will map these weather states to a combination of our images: cloudy, rain, and sunny

    clear           -> sunny

    pcloudy, humid  -> cloudy1
    mcloudy         -> cloudy2
    cloudy          -> cloudy3

    ishower         -> rain1
    oshower         -> cloudy1, rain1
    lightrain       -> cloudy2, rain1
    rain            -> rain3

    any snow        -> snow

    So basically the weather info we have to pass to the template is a combination of these keywords:
        cloudy1, cloudy2, cloudy3, rain1, rain3, noimg
    '''
    # Variable to para extrair o tempo de hoje
    api_weather = weather['dataseries'][0]['weather']

    # Variável para guardar os nossos estados.
    # É um "set" porque cada estado nosso só deve aparecer uma vez no máximo. Não queremos estados repetidos.
    our_weather_status = set()

    # Se está clear, vai ser só 'sunny'.
    if 'clear' in api_weather:
        our_weather_status.add('sunny')

    # Se não está clear, pode ter mais do que um estado (ex: lightrain = cloudy2 + rain1).
    # Nesta sequência de ifs lidamos com os outros casos e juntamos a combinação certa de estados nossos.
    else:
        if 'humid' in api_weather or 'pcloudy' in api_weather or 'oshower' in api_weather:
            our_weather_status.add('cloudy1')
        elif 'mcloudy' in api_weather or 'lightrain' in api_weather:
            our_weather_status.add('cloudy2')
        elif 'cloudy' in api_weather:
            our_weather_status.add('cloudy3')

        if 'shower' in api_weather or 'lightrain' in api_weather:
            our_weather_status.add('rain1')
        elif 'rain' in api_weather:
            our_weather_status.add('rain3')

        if 'snow' in api_weather:
            our_weather_status.add('snow')

    # ------------------------------------------------------------------------------------------------------------------

    # ------ Render do template ----------------------------------------------------------------------------------------
    # Agora que já temos a 'location' do Geolocation API e o weather status do Weather API...
    # ... é só chamar o render com o nosso template e passar essa informação!

    return render(request, 'simple_weather/index.html',
                  {'weather_api': api_weather, 'weather_today': our_weather_status,
                   'lat': lat, 'long': long, 'location': location})
