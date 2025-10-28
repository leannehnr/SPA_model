"""
Robot Sense Module
Read cured sensors value and produces perception
"""

import json
import requests

def sense():
    traitement = ""
    # requête
    response = requests.get("http://localhost:8001/read_sensor/distance")
    # Lecture de l'info + exception
    js = response.text
    ds1_value=json.loads(js)
    assert isinstance(ds1_value, float), f"Value is not a float -- {ds1_value}"
    #print(ds1_value)
    # Traitement de l'info - proche - ok tiers - loin
    if ds1_value < 0.5:
        traitement = "NEAR"
    elif ds1_value < 1.0:
        traitement = "NORMAL"
    else :
        traitement = "FAR AWAY"
    # return perception as a json object
    response.content_type = 'application/json'
    return {'perception': traitement}


if __name__ == "__main__":
    print(sense())
