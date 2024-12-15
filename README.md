## Home Assistant Custom Component: Temperatur.nu

[![GitHub Release][releases-shield]][releases]
[![downloads-shield]][release-link]
![Project Stage][project-stage-shield]
[![issues-shield]](issues)
[![License][license-shield]](LICENSE.md)
[![hacs_badge][hacs-shield]][hacs]
[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

This custom component includes a sensor for temperatur.nu as well as a service for reporting your current temperature

After installing the integration using HACS and restarting your server you simply add it by clicking the button below or by going to Devices & Services and adding it from there.

[![add-integration-shield]][add-integration]

If you only want to use the service for reporting but are not interested in getting any sensors check the box for "Only register service". 

If you want a sensor you enter the id of the sensor you want to add. You will find the id at the end of the url. For example the id is ekholmen in this url https://www.temperatur.nu/ekholmen

Once a sensor is added there is no need to register the service separately as they will be automatically registered along with the sensor.

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

[downloads-shield]: https://img.shields.io/github/downloads/popeen/Home-Assistant-Custom-Component-Temperatur-Nu/total
[release-link]: https://github.com/popeen/Home-Assistant-Custom-Component-Temperatur-Nu/releases
[releases-shield]: https://img.shields.io/github/release/popeen/Home-Assistant-Custom-Component-Temperatur-Nu.svg
[releases]: https://github.com/popeen/Home-Assistant-Custom-Component-Temperatur-Nu/releases
[project-stage-shield]: https://img.shields.io/badge/project%20stage-ready%20for%20use-green.svg
[issues-shield]: https://img.shields.io/github/issues-raw/popeen/Home-Assistant-Custom-Component-Temperatur-Nu.svg
[license-shield]: https://img.shields.io/github/license/popeen/Home-Assistant-Custom-Component-Temperatur-Nu.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Default-41BDF5.svg
[hacs]: https://github.com/custom-components/hacs
[buymeacoffee-shield]: https://img.shields.io/badge/donation-Buy%20me%20a%20coffee-orange
[buymeacoffee]: https://www.buymeacoffee.com/popeen
[add-integration-shield]: https://my.home-assistant.io/badges/config_flow_start.svg
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start/?domain=temperatur_nu
