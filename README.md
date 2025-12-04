<a id="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]
[![PyPI][pypi-shield]][pypi-url]
[![Python Version][python-version-shield]][python-version-url]
[![Buy Me A Coffee][buyme-a-coffee]][buyme-a-coffee-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


# WatchMyUPS

A FastAPI application to expose data from UPS devices via NUT (Network UPS Tools).

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <ul>
            <li><a href="#pip">Pip</a></li>
            <li><a href="#docker">Docker</a></li>
        </ul>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#changelog">Changelog</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#donation">Donation</a></li>
  </ol>
</details>

## About The Project
WatchMyUPS is a FastAPI-based application that utilizes NUT (Network UPS Tools) to collect and expose data from UPS devices. It can be easily integrated with monitoring systems, enables the creation of secure shutdown protocols using data obtained via its API, and can be reliably used in applications that automatically take checkpoints during power outages.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

1. Install and configure [NUT (Network UPS Tools)][nut-url] (AYou can also check this for a more detailed [NUT installation guide.][nut-installation-guide])
2. Install [Docker][docker-url] (This step is optional. You can follow it if you want to run WatchMyUPS on a container.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

#### Pip
1. Clone the repo
   ```sh
   git clone https://github.com/murratefe/watchmyups.git
   ```
2. Install the requirements 
    ```sh
    cd watchmyups
    pip install .
    ```
#### Docker
1. Clone the repo
   ```sh
   cd watchmyups
   git clone https://github.com/murratefe/watchmyups.git
   ```
2. Docker up
    ```sh
    docker-compose up
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
1. Run the application
   ```sh
   python watchmyups.py --nut-host 127.0.0.1 --nut-port 3493 --nut-login admin --nut-password password --export-host 127.0.0.1 --export-port 9999
   ```
2. You can access the data at http://`<EXPORTER_BIND_ADDRESS>`:`<EXPORTER_PORT>`/

### Args
- `--nut-host`: IP address of the NUT server. (default: 127.0.0.1)
- `--nut-port`: Port of the NUT server (default: 3493).
- `--nut-login`: Username for NUT authentication. (default: None)
- `--nut-password`: Password for NUT authentication. (default: None)
- `--nut-debug`: Enable debug mode (default: False).
- `--nut-timeout`: Timeout for NUT operations in seconds (default: 5).
- `--export-host`: Bind address for the exporter (default: 0.0.0.0).
- `--export-port`: Port for the exporter service (default: 9999).
- `--docker-mode`: Run the application in Docker mode (default: False). If set to True, it will read environment variables instead of command-line arguments.
- `--version`: Show the version and exit.
- `--license`: Show license information and exit.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Changelog

See the [CHANGELOG](CHANGELOG.md) for a detailed list of changes and updates.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing
See the [CONTRIBUTING](.github/CONTRIBUTING.md) file for contribution guidelines.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This project is licensed under the <b>GNU General Public License v3.0 (GPLv3)</b>.
See the [LICENSE](LICENSE) file for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
<b>Murat EFE</b><br/>
<br/>[![linkedin-shield]][linkedin-url]
<br/>[![github-shield]][github-url]
<br/>[![kaggle-shield]][kaggle-url]
<br/>[![reddit-shield]][reddit-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Donation
If you find this project useful and would like to support its development, consider buying me a coffee!

[![Buy Me A Coffee][buyme-a-coffee]][buyme-a-coffee-url]<br/>
You can also buy me a coffee via ![usdt-shield] 0xba2ea63a519ed0eb4342f410b0a91990244c4308  <br/>

You can also support the project by starring the repository and sharing it with others.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[python-version-shield]: https://img.shields.io/badge/Python-3.12%2B-blue.svg?style=for-the-badge
[python-version-url]: https://www.python.org/downloads/
[contributors-shield]: https://img.shields.io/github/contributors/murratefe/watchmyups.svg?style=for-the-badge
[contributors-url]: https://github.com/murratefe/watchmyups/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/murratefe/watchmyups.svg?style=for-the-badge
[forks-url]: https://github.com/murratefe/watchmyups/network/members
[stars-shield]: https://img.shields.io/github/stars/murratefe/watchmyups.svg?style=for-the-badge
[stars-url]: https://github.com/murratefe/watchmyups/stargazers
[issues-shield]: https://img.shields.io/github/issues/murratefe/watchmyups.svg?style=for-the-badge
[issues-url]: https://github.com/murratefe/watchmyups/issues
[license-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge
[license-url]: LICENSE
[nut-url]:https://networkupstools.org/index.html
[docker-url]: https://docs.docker.com/get-started/
[nut-installation-guide]: https://technotim.live/posts/NUT-server-guide/
[reddit-shield]: https://img.shields.io/badge/Reddit-%23FF4500.svg?style=for-the-badge&logo=reddit&logoColor=white
[reddit-url]: https://www.reddit.com/user/Zestyclose-Fruit9925/
[buyme-a-coffee]: https://img.shields.io/badge/Buy%20Me%20A-Coffee-yellow?style=for-the-badge&logo=buy-me-a-coffee
[github-shield]: https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[kaggle-shield]: https://img.shields.io/badge/Kaggle-%23121011.svg?style=for-the-badge&logo=kaggle&logoColor=white
[kaggle-url]: https://www.kaggle.com/muratefe
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/murratefe/
[pypi-shield]: https://img.shields.io/pypi/v/watchmyups.svg?style=for-the-badge
[pypi-url]: https://pypi.org/project/watchmyups/
[github-url]: https://github.com/murratefe/
[buyme-a-coffee-url]: https://www.buymeacoffee.com/murratefe
[usdt-shield]: https://img.shields.io/badge/USDT(BEP20)-black?style=for-the-badge&logo=tether