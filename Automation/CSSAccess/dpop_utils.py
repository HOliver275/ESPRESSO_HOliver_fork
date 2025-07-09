# datetime: https://docs.python.org/3/library/datetime.html
import datetime
# math: https://docs.python.org/3/library/math.html
import math
# typing.Optional: https://docs.python.org/3/library/typing.html#typing.Optional
from typing import Optional
# uuid.uuid4: https://docs.python.org/3/library/uuid.html#uuid.uuid4
from uuid import uuid4

# jwt: https://pyjwt.readthedocs.io/en/latest/
import jwt
# requests: https://pypi.org/project/requests/
import requests
# jwcrypto.jwk: https://jwcrypto.readthedocs.io/en/latest/jwk.html
from jwcrypto import jwk

# signing algorithm for the JSON Web Token
SIGNING_ALG = "ES256"

def generate_dpop_key_pair() -> jwk.JWK:
    """
    Generates the DPOP key pair.
    
    return: a JSON Web Key.
    """
    # generate a P-256 EC key pair 
    key = jwk.JWK.generate(kty="EC", crv="P-256")
    # return the P-256 EC key pair
    return key

"""
Creates the DPOP authorization header.

param: url, a string
param: method, a string
param: key, a JSON Web Key
return: a string representing the encoded JSON Web Token
"""
def create_dpop_header(url: str, method: str, key: jwk.JWK) -> str:
    # construct the DPOP header payload from the given URL
    # construct the DPOP headers, exporting the public key in the standard JSON format
    payload = {
        "htu": url,
        "htm": method.upper(),
        "jti": str(uuid4()),
        "iat": math.floor(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()),
    }
    headers = {
        "typ": "dpop+jwt",
        "jwk": key.export_public(as_dict=True),
    }
    # encode the payload, headers and key as a JSON Web Token
    token = jwt_encode(payload, key, headers=headers)
    # return the encoded JSON Web Token
    return token

"""
Encodes a JSON Web Token.

param: payload, a dictionary
param: key, a JSON Web Key
param: headers, optional, a dictionary
return: a string representing an encoded JSON Web Token
"""
def jwt_encode(payload: dict, key: jwk.JWK, headers: Optional[dict]) -> str:
    # if there are no headers, create an empty header dictionary
    headers = headers or {}
    # export keys to a data buffer that can be stored as a PEM file
    key_pem = key.export_to_pem(private_key=True, password=None).decode("utf-8")
    # encodes the payload and headers, the serialized bytes buffer containing the PEM formatted key,
    # according to the specified signing algorithm
    encoded_jwt = jwt.encode(
        payload, key=key_pem, algorithm=SIGNING_ALG, headers=headers
    )
    # return the encoded JSON Web Token
    return encoded_jwt


def jwt_decode_without_verification(encoded_jwt: str) -> dict:
    return jwt.api_jwt.decode_complete(
        encoded_jwt,
        options={
            "verify_signature": False,
        },
    )["payload"]
