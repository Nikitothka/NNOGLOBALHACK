import json
import requests
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from authorizations.src.settings import base_hackathon_settings


def save_authorization_data_and_return_response(
    authorization_data, system_name: str
) -> JSONResponse:
    header = {
        "Authorization": f"Bearer {base_hackathon_settings.user_token_from_tg_bot}"
    }

    data = {
        "system_name": system_name,
        "authorization_data_json": json.dumps(authorization_data),
    }

    try:
        resp = requests.post(
            base_hackathon_settings.save_auth_data_endpoint, json=data, headers=header
        )
        resp.raise_for_status()

        if resp.status_code == 200:
            return JSONResponse(
                status_code=200,
                content={"message": "Authorization successful and data saved."},
            )
        else:
            return JSONResponse(
                status_code=resp.status_code,
                content={"message": f"Unexpected response: {resp.status_code}"},
            )

    except requests.exceptions.HTTPError as e:
        if resp.status_code == 400:
            raise HTTPException(
                status_code=400, detail="Bad request to save authorization data"
            )
        elif resp.status_code == 401:
            raise HTTPException(
                status_code=401, detail="Unauthorized to save authorization data"
            )
        elif resp.status_code == 403:
            raise HTTPException(
                status_code=403, detail="Forbidden to save authorization data"
            )
        elif resp.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Endpoint to save authorization data not found"
            )
        elif resp.status_code >= 500:
            raise HTTPException(
                status_code=502, detail="Server error while saving authorization data"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=500, detail="Error occurred while saving authorization data"
        )
