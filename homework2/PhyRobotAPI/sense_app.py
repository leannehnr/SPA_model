"""
Physical Sensor API Process
Input from the real world 
Output: cured sensor signals 
"""
import glob
import random
from typing import Any
import json
from bottle import route, run

class PhySensor:
    """
    Abstract Physical Sensor Class
    """

    def __init__(self, name:str, work_range, config_file : str):
        # [WARNING] : absolute path of the config file
        assert isinstance(name, str) and len(name)>0
        assert isinstance(work_range, tuple) and len(work_range)==2
        assert isinstance(config_file, str) and glob.glob(config_file), \
             f"Configuration file {config_file} is not found" # fail if config_file doesnt exist in the system
        self._id = name
        self._range = work_range
        config_js = open(config_file, encoding="utf-8").read()
        self._config = json.loads(config_js)

    def read(self) -> Any:
        """
        Read the sensor value
        Output : cured sensor value 
        """
        pass

    def __repr__(self) -> str: 
        return f"Sensor : {self._id}, range {self._range}"
    

class DistanceSensor(PhySensor):
    """
    Proximity distance sensor monodimensional 
    """
    def read(self) -> float:
        """
        Read the distance sensor fromthe hardware layer 
        skip all physical issues
        """
        return 1.5*random.random() # any value
    
    def simple_test(self):
        ds1=DistanceSensor("test_sensor", (-1, 1), "test.json")
        print(ds1.read())
    
sensors = {}
@route ('/read_sensor/<name>')
def read_sensor(name:str)-> str:
    if name in sensors:
        out_js = json.dumps(sensors[name].read())
        return out_js
    return json.dumps({"error": f"Sensor '{name}' not found"})


if __name__ == "__main__":
    sensors['distance']=DistanceSensor("test_sensor", (-1, 1), "test.json")
    run(host='localhost', port=8001)
    
