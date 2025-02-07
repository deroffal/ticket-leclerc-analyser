import json
import logging
import os
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

from src.utils.raw_files import save_to_raw, raw_file_exists

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


def _ticket_request(path, data):
    """
    Execute a api request to Leclerc ticket api
    :param path: path of the api (rechercher|detail)
    :param data: the json body of the request
    :return: the json response
    """
    ticket_api_url = "https://www.e.leclerc/api/rest/infomil-bridge/tdm/ticket"
    id_token = os.getenv('ID_TOKEN')
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'cookie': f'id_token={id_token};',
        'user-agent': 'ticket-leclerc-analyse'
    }
    response = requests.request("POST", f"{ticket_api_url}/{path}", headers=headers, data=data)
    if response.status_code == 201:
        return response.json()
    else:
        logger.error(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    payload = json.dumps({
        "size": 10,
        "startDate": "2025-01-01",
        "endDate": "2025-01-31"
    })

    tickets = _ticket_request("rechercher", payload)

    if tickets is None:
        logger.error("Can't get tickets. Terminating ...")
        sys.exit(1)

    for ticket in tickets:
        logger.info(f"ticket: {ticket}")
        detail = _ticket_request("detail", json.dumps({
            "ticketId": ticket['identifiant'],
            "ticketDate": datetime.strptime(ticket['date'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
            "emitterCode": ticket['noEmetteur']}
        ))

        name = f"{detail['identifiant']}.html"

        if not raw_file_exists(name):
            save_to_raw(name, detail['html'])
            logger.info(f"done for {detail['identifiant']}")
        else:
            logger.warning(f'file {name} already exists')
