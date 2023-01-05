## Home Assistant Custom Component: Temperatur.nu

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
[![issues-shield]](issues)
[![License][license-shield]](LICENSE.md)
[![hacs_badge][hacs-custom-shield]][hacs]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

This custom component includes a sensor for temperatur.nu as well as a service for reporting your current temperature

**Sensor**\
This sensor will show the current temperature on the set location
|Parameter| What to put |
|--|--|
| name | What do you want to call the sensor|
| location | This is the name of the station on temperatur.nu. You will find it at the end of the url for the station. In the example we are using https://www.temperatur.nu/ekholmen |
```  
- platform: temperatur_nu
  name: Temperatur Ekholmen
  location: ekholmen

```  
**Reporting service**\
This service will send your current temperature to temperatur.nu.\
You will need the hash/token that you get when [setting up](https://www.temperatur.nu/info/rapportera-till-temperatur-nu/) your station. If you have a station set up already but don't know your token you can find it [here](https://www.temperatur.nu/egenadmin)
|Parameter| What to put |
|--|--|
| hash | Your private hash |
| sensor | The sensor that contains your current temperature |

```
service: temperatur_nu.send_temperature
data:
  sensor: sensor.temperature_outdoor_lowest
  hash: 3d8dummy32c18dummye2d87adummy63f


```

[releases-shield]: https://img.shields.io/github/release/popeen/Home-Assistant-Custom-Component-Temperatur-Nu.svg
[releases]: https://github.com/popeen/Home-Assistant-Custom-Component-Temperatur-Nu/releases
[project-stage-shield]: https://img.shields.io/badge/project%20stage-ready%20for%20use-green.svg
[issues-shield]: https://img.shields.io/github/issues-raw/popeen/Home-Assistant-Custom-Component-Temperatur-Nu.svg
[license-shield]: https://img.shields.io/github/license/popeen/Home-Assistant-Custom-Component-Temperatur-Nu.svg
[hacs-custom-shield]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs]: https://github.com/custom-components/hacs
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/popeen
