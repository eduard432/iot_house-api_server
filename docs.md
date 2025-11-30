Caso 1: Arduino envía sensor

Topico MQTT:
`iot_house_tec/casa/sensor/<device_id>`

``` JSON
{
  "source": "arduino",
  "type": "sensor",
  "device_id": "<device_id>",
  "payload": {
    "<device_sensor_id>": 24.8,
    "<device_sensor_id>": 70
  }
}

```


Caso 1: Ejemplo:

Sensor BMP280: id -> 1
Humedad: id -> 1
Temperatura: id -> 2

``` JSON
{
  "source": "arduino",
  "type": "sensor",
  "device_id": "1",
  "payload": {
    "1": 24.8,
    "2": 70
  }
}

```

Caso 2: Frontend activa un actuador

Topico MQTT:
`iot_house_tec/casa/actuator/command/<device_id>`

``` JSON
{
  "source": "frontend",
  "type": "command",
  "device_id": "<device_id>",
  "payload": {
    "action": "<action>",
  }
}

```


Caso 2: Ejemplo:

Servo: id -> 1


``` JSON
{
  "source": "frontend",
  "type": "command",
  "device_id": "2",
  "payload": {
    "action": "on",
  }
}

```



Caso 3: Arduino envía actualización del actuador

Topico MQTT:
`iot_house_tec/casa/actuator/state/<device_id>`

``` JSON
{
  "source": "arduino",
  "type": "state",
  "device_id": "<device_id>",
  "payload": {
    "state": "<state>",
  }
}

```


Caso 3: Ejemplo:

Servo: id -> 1


``` JSON
{
  "source": "arduino",
  "type": "state",
  "device_id": "2",
  "payload": {
    "state": "on",
  }
}

```

