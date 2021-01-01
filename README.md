# SonoffBasic
SonoffBasic allows to control Sonoff switches via the Ewelink cloud, with a very basic features.

### ⚠️ Project was tested on sonoff basic only. Other devices will be tested and adjust in the future. 
## requirements

* Sonoff switch must be connected to ewelink app [SONOFF Basic USER GUIDE](http://ewelink.coolkit.cc/?p=126). 
* Username is email address. 
* Ewelink account region must be one of **'us'**, **'eu'** or **'cn'**.
* install SonoffBasic (https://pypi.org/project/SonoffBasic/)

## How to use ✨
* Create an instance of Sonoff with ewelink. 
available params (all values in string format):
    * username - email address (required) 
    * password (required)
    * region (optional) default *'us'*
    * timezone (optional) default *'US/Pacific'*
    ```python
    >>> from SonoffBasic.sonoff import Sonoff
    >>> sonoff = Sonoff(username='my_name@example.com',
                        password='my_pass',
                        timezone='US/Pacific',
                        region='us')
    ```
* Search the required device

    ```python
    >>> print(sonoff.devices)
    [{'name': 'taco', 'deviceid': '1000157898', 'status': 'on'}, 
    {'name': 'Irrigation', 'deviceid': '100015b23r', 'status': 'off'}]
    ```
* Control the device
    ```python 
    >>> sonoff.change_device_status(statusid = '1000157898',
                                    new_status = 'off')            
    deviceid: 1000157898 status successfully changed to off
    ```

### Special Thanks
Thanks to [@AlexxIT](https://github.com/AlexxIT).
cloud connection to [eWeLink](https://www.ewelink.cc/en/) was inspired by [SonoffLAN](https://github.com/AlexxIT/SonoffLAN) project.
