# System packages
import logging
from os import uname

# Third part packages
from flask import Flask, jsonify

api = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

@api.route("/api")
def apiHome():
    log.info("No Approov Token protection for request: /api")
    return _hostnameResponse("NOT_APPROOV_TOKEN_PROTECTED")

@api.route("/api/approov-token-protected")
def apiApproovTokenProtected():
    log.info("Approov Token protected request for: /api/approov-token-protected")
    return _hostnameResponse("APPROOV_TOKEN_PROTECTED")

@api.route("/api/approov-token-binding-protected")
def apiApproovTokenBindingProtected():
    log.info("Approov Token Binding protected request for: /api/approov-token-binding/protected")
    return _hostnameResponse("APPROOV_TOKEN_BINDING_PROTECTED")

def _hostnameResponse(status):
    hostname = uname()[1]
    log.info(uname())
    return jsonify(
        status=status,
        hostname=hostname
    )
