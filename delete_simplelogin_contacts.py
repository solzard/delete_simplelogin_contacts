"""Delete a SimpleLogin API user's all contacts.

References:
    https://github.com/simple-login/app/blob/master/docs/api.md
    https://docs.python-requests.org/en/latest/user/quickstart/
"""
import os
import typing

import dotenv
import requests
import tqdm

dotenv.load_dotenv()

API_KEY = os.environ["SIMPLELOGIN_API_KEY"]
HEADERS = {"Authentication": API_KEY}
URL_BASE = "https://app.simplelogin.io/api"

ALIAS_ID = typing.TypeVar("ALIAS_ID", bound=int)
CONTACT_ID = typing.TypeVar("CONTACT_ID", bound=int)


def get_alias_ids() -> set[ALIAS_ID]:
    """Get user aliases.

    Reference:
        https://github.com/simple-login/app/blob/master/docs/api.md#get-apiv2aliases
    """
    url = f"{URL_BASE}/v2/aliases"
    payload = {"page_id": 0}
    alias_ids: set[ALIAS_ID] = set()
    with tqdm.tqdm(desc="get_alias_ids", unit=" ids") as pbar:
        while True:
            response = requests.get(url=url, params=payload, headers=HEADERS)
            aliases = response.json()["aliases"]
            new_ids: set[ALIAS_ID] = {alias["id"] for alias in aliases}
            pbar.update(len(new_ids))
            if new_ids:
                alias_ids.update(new_ids)
                payload["page_id"] += 1
            else:
                break
    return alias_ids


def get_contact_ids(alias_id: ALIAS_ID) -> set[CONTACT_ID]:
    """Get contact ids for a given alias.

    Reference:
        https://github.com/simple-login/app/blob/master/docs/api.md#get-apialiasesalias_idcontacts
    """
    url = f"{URL_BASE}/aliases/{alias_id}/contacts"
    payload = {"page_id": 0}
    contact_ids: set[CONTACT_ID] = set()
    while True:
        response = requests.get(url=url, params=payload, headers=HEADERS)
        contacts = response.json()["contacts"]
        new_ids: set[CONTACT_ID] = {contact["id"] for contact in contacts}
        if new_ids:
            contact_ids.update(new_ids)
            payload["page_id"] += 1
        else:
            break
    return contact_ids


def delete_contact(contact_id: CONTACT_ID):
    """Delete a contact.

    Reference:
        https://github.com/simple-login/app/blob/master/docs/api.md#delete-apicontactscontact_id
    """
    url = f"{URL_BASE}/contacts/{contact_id}"
    requests.delete(url=url, headers=HEADERS)


def main() -> None:
    alias_ids: set[ALIAS_ID] = get_alias_ids()
    contact_ids: set[CONTACT_ID] = set()
    with tqdm.tqdm(total=len(alias_ids), desc="get_contact_ids") as pbar:
        for alias_id in alias_ids:
            contact_ids.update(get_contact_ids(alias_id))
            pbar.update()
    with tqdm.tqdm(total=len(contact_ids), desc="delete_contact") as pbar:
        for contact_id in contact_ids:
            delete_contact(contact_id)
            pbar.update()


if __name__ == "__main__":
    main()
