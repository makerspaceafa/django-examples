## Django Examples
Este projeto tem como objetivo agregar várias apps para exemplificar / demonstrar 
capacidades do django.

Muitas delas incluem desafios para melhorar a sua funcionalidade / performance que podem usar para desenvolver e praticar as vossas capacidades de **Python** e **Django**.

### Organização

Existe uma `main_app` que gera a página de entrada no _website_ com ligações para as apps existentes.  
Isto é automático, desde que adicionem as vossas apps da maneira correta no `urls.py` do projeto.

À partida não devem modificar esta aplicação.

### Demo Apps:

- **Simple Weather**  
  ![](readme_images/simple_weather.png)  
  Esta app mostra uma visualização simples do estado de tempo nas coordenadas GPS especificadas.  
  Desafios:
    - Garantir o input de coordenadas certas (input validation).
    - A página demora 4-5s segundos a carregar! Fix it!
    - Completar a app com mais casos de tempo (imagens já estão incluídas).
