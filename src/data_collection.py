import requests
import pandas as pd

def limpiar_datos_fincaraiz(data):
    """
    Limpia y extrae la información relevante de la consulta a la API de FincaRaíz.

    Parámetros:
    - data (dict): Respuesta en formato JSON obtenida desde la API.

    Retorna:
    - list[dict]: Lista de inmuebles con información clave.
    """
    propiedades = []

    # Verificamos si existe la clave correcta para acceder a los inmuebles
    if "hits" in data and "hits" in data["hits"]:
        for item in data["hits"]["hits"]:
            src = item["_source"]["listing"]

            propiedad = {
                "id": src.get("id"),
                "titulo": src.get("title", "Sin título"),
                "descripcion": src.get("description", "Sin descripción"),
                "direccion": src.get("address", "No disponible"),
                "ciudad": src["locations"]["city"][0]["name"] if src["locations"].get("city") else "No disponible",
                "estado": src["locations"]["state"][0]["name"] if src["locations"].get("state") else "No disponible",
                "barrio": src["locations"]["neighbourhood"][0]["name"] if src["locations"].get("neighbourhood") else "No disponible",
                "latitud": src.get("latitude"),
                "longitud": src.get("longitude"),
                "precio": src["price"]["amount"] if src.get("price") else None,
                "moneda": src["price"]["currency"]["name"] if src.get("price") else "No disponible",
                "habitaciones": src.get("bedrooms", 0),
                "baños": src.get("bathrooms", 0),
                "parqueaderos": src.get("garage", 0),
                "area_m2": src.get("m2", 0),
                "imagenes": [img["image"] for img in src.get("images", []) if "image" in img],
                "url_anuncio": f"https://www.fincaraiz.com.co{src.get('link', '')}"
            }

            propiedades.append(propiedad)

    return propiedades



def generar_payload(ciudad, coordenadas,id_ciudad,page):
    """
    Función para generar el payload del request dependiendo de la ciudad.

    :param ciudad: Nombre de la ciudad (Ej: 'Medellín', 'Sabaneta').
    :param coordenadas: Coordenadas de la ciudad (Ej: [-75.57786065131165, 6.249816589298594]).
    :param id_ciudad: Id de la ciudad en la API (Ej: "183f0a11-9452-4160-9089-1b0e7ed45863").   
    :return: Payload del JSON preparado para la API.
    """
    payload = {"variables":
                {"rows":20,
                 "params":
                 {"page":page,
                  "order":2,
                  "operation_type_id":2,
                  "property_type_id":[1,2,14,15,16],
                  "projects":'false',"currencyID":4,
                  "m2Currency":4,
                  "locations":[{"country":[{"name":"Colombia","id":"858656c1-bbb1-4b0d-b569-f61bbdebc8f0","slug":"country-48-colombia"}],
                                "name":ciudad,"location_point":{"coordinates":coordenadas,"type":"point"},
                                "id":id_ciudad,
                                "type":"CITY","slug":["city-colombia-05-001"],
                                "estate":{"name":"Antioquia","id":"2d63ee80-421b-488f-992a-0e07a3264c3e","slug":"state-colombia-05-antioquia"}}]},
                                "page":page,"source":10},
                                "query":""
                                }
    return payload

def obtener_todas_las_propiedades():
    # Inicializar variables
    todas_las_propiedades = []
    # URL de la API de Fincaraiz
    url = "https://search-service.fincaraiz.com.co/api/v1/properties/search"
    # Código de estado de la respuesta JSON
    requests_json = 200
    
    # Definir las ciudades, sus coordenadas y sus IDs
    ciudades = ["Medellín", "Sabaneta", "Envigado", "Itagüí", "Bello", "La estrella", "Caldas", "Copacabana", "Girardota", "Barbosa"]
    coordenadas_ciudades = {
        "Medellín": [-75.57786065131165, 6.249816589298594],
        "Sabaneta": [-75.615552, 6.150848],
        "Envigado": [-75.582766,6.166891],
        "Itagüí": [-75.61224929212936,6.175069444446771],
        "Bello": [-75.554813,6.333991],
        "La estrella": [-75.637076,6.145162],
        "Caldas": [-75.63279850494914,6.092031757719933],
        "Copacabana": [-75.509309,6.348654],
        "Girardota": [-75.444235,6.379487],
        "Barbosa": [-75.331627,6.439195]
    }
    ids = {"Medellín": "183f0a11-9452-4160-9089-1b0e7ed45863","Sabaneta": "241a17ef-3aa0-485c-93aa-689fc2f2d114",
           "Envigado": "596f30cb-3582-416e-a071-71634190a703","Itagüí": "cf5dc27a-9e05-4b0a-b98a-0715fe4e5d2b",
           "Bello": "9feb0402-fc35-4538-8ca1-d53c0fec2c35","La estrella": "c19b4e81-f003-408a-b7db-4bbcb9b3b6d5",
           "Caldas": "5499b608-1002-43a3-9215-01c40ffae22b","Copacabana": "b8f0f380-18c4-49ee-a6b3-92b454846718",
           "Girardota": "0affff3e-ec6a-421e-a2d4-8b198493cff9","Barbosa": "1041113c-cced-48fc-a1d5-c10002214f67"}
    
    for ciudad in ciudades:
        pagina = 1
        while requests_json == 200 and pagina <= 500:  # Número máximo de páginas a obtener 500 # Mil propiedades por ciudad
            coordenadas = coordenadas_ciudades.get(ciudad)
            id_ciudad = ids.get(ciudad)
            print(f"Obteniendo página {pagina} de la cuidad {ciudad}..")  # Para ver el progreso     

            # Hacer la solicitud a la API
            request_json = generar_payload(ciudad, coordenadas,id_ciudad,pagina)
            response = requests.post(url, json=request_json)           
            requests_json = response.status_code
            if requests_json != 200:
                print(f"Error al obtener datos para {ciudad}. Código de estado: {requests_json}")
                break  # Si hay un error con el código de estado, terminamos el bucle
            response_body = response.json()

            # Extraer propiedades de la respuesta
            propiedades = limpiar_datos_fincaraiz(response_body)
            
            # Si no hay más propiedades o no se obtienen datos, terminamos el bucle
            if not propiedades:
                print(f"No hay más propiedades para {ciudad} o los datos no están disponibles.")
                break

            # Agregar propiedades a la lista final
            todas_las_propiedades.extend(propiedades)

            # Pasar a la siguiente página
            pagina += 1

    return todas_las_propiedades

# Llamar a la función para obtener todas las propiedades
todas_propiedades = obtener_todas_las_propiedades()

# Mostrar cuántas propiedades se obtuvieron
print(f"Total de propiedades obtenidas: {len(todas_propiedades)}")

#Guadar en un DataFrame
todas_propiedades = pd.DataFrame(todas_propiedades)
todas_propiedades.to_csv('../data/raw/propiedades_fincaraiz.csv' , index=False, encoding='utf-8')

def extraer_detalles_completos(data):
    """
    Extrae todos los detalles posibles de una propiedad obtenida desde la API de FincaRaíz.

    Parámetros:
    - data (dict): Respuesta en formato JSON obtenida desde la API.

    Retorna:
    - dict: Diccionario con todos los detalles de la propiedad.
    """
    propiedad = {}

    if "hits" in data and "hits" in data["hits"] and data["hits"]["hits"]:
        item = data["hits"]["hits"][0]["_source"]["listing"]

        propiedad = {
            "id": item.get("id"),
            "titulo": item.get("title", "Sin título"),
            "descripcion": item.get("description", "Sin descripción"),
            "direccion": item.get("address", "No disponible"),
            "ciudad": item["locations"]["city"][0]["name"] if item["locations"].get("city") else "No disponible",
            "departamento": item["locations"]["state"][0]["name"] if item["locations"].get("state") else "No disponible",
            "barrio": item["locations"]["neighbourhood"][0]["name"] if item["locations"].get("neighbourhood") else "No disponible",
            "Zona": item["locations"]["zone"][0]["name"] if item["locations"].get("zone") else "No disponible",
            "Comuna": item["locations"]["commune"][0]["name"] if item["locations"].get("commune") else "No disponible",
            "latitud": item.get("latitude"),
            "longitud": item.get("longitude"),
            "precio": item["price"]["amount"] if "price" in item else None,
            "moneda": item["price"]["currency"]["name"] if "price" in item else "No disponible",
            "tipo_de_inmueble": item["technicalSheet"][1]["value"],
            "estado":item["technicalSheet"][2]["value"],
            #"area_m2": item.get("m2", 0),
            "habitaciones": item.get("bedrooms", 0),
            "baños": item.get("bathrooms", 0),
            "area_construida_m2": item["technicalSheet"][4]["value"],
            "area_privada_m2": item["technicalSheet"][5]["value"],
            "estrato": item.get("stratum", "No disponible"),
            "pisos_edificio": item.get("floorsCount", None),
            "piso_ubicacion": item.get("floor", None),
            "parqueaderos": item.get("garage", 0),
            "antigüedad": item["technicalSheet"][6]["value"],
            "gastos_comunes": item["commonExpenses"]["amount"] if "commonExpenses" in item else None,
            "imagenes": [img["image"] for img in item.get("images", [])],
            "url_anuncio": f"https://www.fincaraiz.com.co{item.get('link', '')}",
            "propietario": item["owner"]["name"] if "owner" in item else "No disponible",
            "telefono": item["owner"].get("masked_phone", "No disponible") if "owner" in item else "No disponible",
            "tipo_propietario": item["owner"].get("type", "No disponible") if "owner" in item else "No disponible",
            "direccion_propietario": item["owner"].get("address", "No disponible") if "owner" in item else "No disponible",
            "fecha_publicacion": item.get("created_at", "No disponible"),
            "fecha_actualizacion": item.get("updated_at", "No disponible"),
            "facilidades": [fac["name"] for fac in item.get("facilities", [])],
            "video": item.get("youtube", "No disponible"),
            "redes_sociales": {red["name"]: red["url"] for red in item.get("socialMediaLinks", [])}
        }

    return propiedad

# Obtener detalle de todas las propiedades obtenidas

def extraer_todas_propiedades(data):
    """
    Extrae todos los detalles posibles de una propiedad obtenida desde la API de FincaRaíz."""
    propiedades = []
    url = "https://search-service.fincaraiz.com.co/api/v1/properties/search"
    for id in data['id']:

        # Inicializar variables
        
        # Modificar el JSON de la solicitud para cambiar la página
        request_json = {"variables":{"rows":100,"params":{"id":id},"page":1,"source":10},"query":""}
        # Hacer la solicitud a la API
        response = requests.post(url, json=request_json)

        # Convertir la respuesta a JSON
        response_body = response.json()
        # Extraer detalles completos de la propiedad
        detalles_propiedad = extraer_detalles_completos(response_body)
        # Agregar propiedades a la lista final
        propiedades.append(detalles_propiedad)
    return propiedades

propiedades = pd.DataFrame(extraer_todas_propiedades(todas_propiedades))
propiedades.to_csv('../data/raw/propiedades_fincaraiz_completas.csv' , sep=';', index=False, encoding='utf-8-sig')