# FloraBot
## Sistema de cultivo automatizado y remoto

***Autor: Martin Vargas***

Florabot es un sistema de cultivo automatizado y de control/monitoreo remoto, para invernaderos o invernaculos tanto,
interiores como exteriores.
Este repositorio solo contiene el frontend y algo del backend, el resto del codigo se encuentra dentro de un Raspberry
3b+ en donde tiene instalado un servidor que despliega la webapp que tiene esta repo. Ademas, en la rpi estan conectados
los reles, algunos sensores y un arduino UNO (que tambien contiene codigo).
Los reles estan destinados a encender o apagar luz, ventiladores, extractor/intractor y 5 bombas peristalticas que se
encargan del riego, la regulacion del ph y la electroconductividad y el riego o la inyeccion de micro y macro nutrientes
segun sea el modo de cultivo que se elija (por tierra o hidroponico)
En el arduino estan conectados algunos sensores tales como medidor de ph, intensidad de luz, electroconductividad, 
humedad, temperatura, temperatura del agua, humedad del sustrato (tierra) y una pequenia pantalla de lcd.
El sistema se complementa con leds senialadores de informacion, una camara, sistema de proteccion electronica, bateria de 12v-7,5Ah
para su continuo funcionamiento y una fuente conmutada con protecciones hacia los circuitos que componen el hardware.
![image](static)

**Caracteristicas del code**
* Python 3
* Flask
* SQLAlchemy
* Paramiko
* pipenv

