import requests
import json

# url de l'API
#url = "http://127.0.0.1:8000/userpost/"
url = "http://127.0.0.1:8000/userpost/?format=api"


def pretty_print_request(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def test_get_user():

    req = requests.Request('GET', url, headers={})
    prepared = req.prepare()
    pretty_print_request(prepared)

    s = requests.Session()
    response = s.send(prepared)

    # réaliser une requête POST avec le contenu du fichier json d'entré
    #response = requests.get(url)
    # validation du code de la réponse. Le status_code de tout s'est bien
    # passé est 200
    assert response.status_code == 200


def test_post_user():
    # lecture du fichier json d'entré
    file = open("fichier.json", "r")
    json_input = file.read()
    request_json = json.loads(json_input)
    # réaliser une requête POST avec le contenu du fichier json d'entré
    #req = requests.Request('POST',url,headers={}, json=json.dumps(request_json))
    #prepared = req.prepare()
    # pretty_print_request(prepared)

    #s = requests.Session()
    #response = s.send(prepared)
    response = requests.post(url, json=request_json)
    # validation du code de la réponse
    assert response.status_code == 201
