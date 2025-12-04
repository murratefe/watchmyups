#!/usr/bin/env python3

"""
WatchMyUPS.

Author: Murat EFE
License: GNU General Public License v3.0
Copyright (c) 2025 Murat EFE

Description:
A FastAPI application to expose data from UPS devices via NUT (Network UPS Tools).

Usecases include retrieving UPS status, battery health, and power events, which can be used for safe shutdowns, alerts, or checkpoints for your applications.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from fastapi import FastAPI, HTTPException, Query
import argparse
import uvicorn
import logging
import os

from nut2 import PyNUTClient


__version__ = "1.0.0"



# Logging Configuration
logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WatchMyUPS")

# --- Configuration Loading ---
app = FastAPI()
default_config = {
    'nut_host': '127.0.0.1', # Default NUT server host
    'nut_port': 3493, # Default NUT server port
    'nut_login': None, # Default NUT server login
    'nut_password': None, # Default NUT server password
    'nut_debug': False, # Default debug mode for NUT client
    'nut_timeout': 5, # Default timeout for NUT client connections
    'export_host': '0.0.0.0', # Default host for FastAPI export
    'export_port': 9999 # Default port for FastAPI export
}
config = {}


def docker_mode_config():
    """Loads configuration from environment variables for Docker mode.
    
    Env Variables:
        NUT_HOST: Hostname or IP address of the NUT server. Default: 127.0.0.1
        NUT_PORT: Port number of the NUT server. Default: 3493
        NUT_LOGIN: Login username for the NUT server. Default: None
        NUT_PASSWORD: Password for the NUT server. Default: None
        NUT_DEBUG: Enable debug mode for the NUT client (True/False). Default: False
        NUT_TIMEOUT: Timeout for NUT client connections. Default: 5
        EXPORT_HOST: Host for FastAPI export. Default is 0.0.0.0
        EXPORT_PORT: Port for FastAPI export. Default is 9999
    Returns:
        dict: Configuration dictionary with the above parameters.
    
    """
    
    nut_host = os.getenv('NUT_HOST', default_config['nut_host']) 
    nut_port = int(os.getenv('NUT_PORT', default_config['nut_port']))
    nut_login = os.getenv('NUT_LOGIN', default_config['nut_login'])
    nut_password = os.getenv('NUT_PASSWORD', default_config['nut_password'])
    nut_debug_str = os.getenv('NUT_DEBUG', default_config['nut_debug'])
    nut_debug = nut_debug_str in ('true', '1', 't')
    nut_timeout = int(os.getenv('NUT_TIMEOUT', default_config['nut_timeout']))
    export_host = os.getenv('EXPORT_HOST', default_config['export_host'])
    export_port = int(os.getenv('EXPORT_PORT', default_config['export_port']))
    return {
        'nut_host': nut_host,
        'nut_port': nut_port,
        'nut_login': nut_login,
        'nut_password': nut_password,
        'nut_debug': nut_debug,
        'nut_timeout': nut_timeout,
        'export_host': export_host,
        'export_port': export_port
    }

def load_config():
    """
    Parses arguments and updates the global config.
    """    
    
    parser = argparse.ArgumentParser(
    description=(
        "WatchMyUPS\n\n"
        "A FastAPI application to expose data from UPS devices via NUT (Network UPS Tools).\n\n"
        "Author: Murat EFE\n\n"
        "Copyright (c) 2025 Murat EFE\n\n"
        f"Version: {__version__}\n\n"
        "License: GNU General Public License v3.0\n\n"
        "Github: https://github.com/murratefe/watchmyups\n\n"
        "Usecases include retriving UPS status, battery health, and power events,\n"
        "and you can use that data for safe shutdowns, alerts or checkpoints for your applications."
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter
)
    parser.add_argument('--nut_host', default=default_config['nut_host'], help='Hostname or IP address of the NUT server. Default: 127.0.0.1')
    parser.add_argument('--nut_port', default=default_config['nut_port'], type=int, help='Port number of the NUT server. Default: 3493')
    parser.add_argument('--nut_login', default=default_config['nut_login'], help='Login username for NUT server. Default: None')
    parser.add_argument('--nut_password', default=default_config['nut_password'], help='Password for NUT server. Default: None')
    parser.add_argument('--nut_debug', action='store_true', help='Enable NUT debug mode. Default: False')
    parser.add_argument('--nut_timeout', default=default_config['nut_timeout'], type=int, help='Timeout for NUT client connections in seconds. Default: 5')
    parser.add_argument('--docker_mode', action='store_true', help='Enable Docker mode settings, loading config from environment variables if set. Default: False')
    parser.add_argument('--export_host', default=default_config['export_host'], help='Host for FastAPI export. Default: 0.0.0.0')
    parser.add_argument('--export_port', default=default_config['export_port'], type=int, help='Port for FastAPI export. Default: 9999')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--license', action='version', version='GNU General Public License v3.0')
    # Use parse_known_args() to avoid issues if uvicorn or other tools add arguments
    args, unknown = parser.parse_known_args()
    
    if args.docker_mode:
        docker_args = docker_mode_config()
        config.update(docker_args)
    else:
        # Convert args to a dictionary and update config
        config.update(vars(args))

# -- WatchMyUPS Class--
class WatchMyUPS:
    def __init__(self, nut_host, nut_port, nut_login=None, nut_password=None, nut_debug=False, nut_timeout=5):
        """
        Initialize the UPS checker with NUT client parameters.
        Args:
            nut_host: Hostname or IP address of the NUT server.
            nut_port: Port number of the NUT server.
            nut_login: Login username for the NUT server. (defaults to None)
            nut_password: Password for the NUT server. (defaults to None)
            nut_debug: Enable debug mode for the NUT client. (defaults to False)
            nut_timeout: Timeout for NUT client connections. (defaults to 5)
        Raises:
            ConnectionError: If unable to connect to the NUT server.
        """
        self.nut_client = PyNUTClient(login=nut_login, password=nut_password, host=nut_host, port=nut_port, timeout=nut_timeout, debug=nut_debug)
        
        if not self.nut_client:
            logger.error(f"PyNUTClient initialization returned None for {nut_host}:{nut_port}")
            raise ConnectionError(f"Failed to connect to NUT server at {nut_host}:{nut_port}")

    def __get_ups_list(self):
        """
        Retrieve the list of UPS devices from the NUT server.
        Returns:
            list: A list of UPS device names.
        """
        logger.debug("Retrieving UPS list from NUT server")
        return self.nut_client.list_ups()

    def get_ups_info(self):
        """
        Retrieve detailed information for each UPS device.
        Returns:
            dict: A dictionary containing UPS device information.
        Raises:
            ValueError: If no UPS devices are found.
        """
        logger.info("Getting UPS info")
        ups_list = self.__get_ups_list()
        if not ups_list:
            logger.warning("No UPS devices found on the NUT server.")
            raise ValueError("No UPS devices found on the NUT server.")

        ups_info = {}
        for ups in ups_list:
            ups_info[ups] = {'info': {}}
            ups_vars = self.nut_client.list_vars(ups)
            for var in ups_vars:
                ups_info[ups]['info'][var] = self.nut_client.get_var(ups, var)

        logger.info(f"Retrieved info for UPS devices: {list(ups_info.keys())}")
        return ups_info


# --- FastAPI Endpoints ---

def main():
    load_config()
    export_host = config.get('export_host')
    export_port = config.get('export_port')
    logger.info(f"Starting WatchMyUPS FastAPI on {export_host}:{export_port}")
    uvicorn.run(app, host=export_host, port=export_port, log_level="info")

@app.get("/")
async def read_ups():
    """Endpoint to retrieve UPS information. and expose it via REST API."""
    try:
        ups_watcher = WatchMyUPS(nut_host=config['nut_host'], nut_port=config['nut_port'], 
        nut_login=config['nut_login'], nut_password=config['nut_password'], 
        nut_debug=config['nut_debug'], nut_timeout=config['nut_timeout'])
        data = ups_watcher.get_ups_info()
        return data
    except Exception as e:
        logger.error(f"Error in read_ups endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    main()



