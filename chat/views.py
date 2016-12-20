import json
from django.http import HttpResponse

from django_auth0.auth_backend import login_required
from twilio.access_token import AccessToken, IpMessagingGrant


@login_required
def tokens(request):
    identity = request.user['sub']
    endpoint_id = request.GET["endpoint_id"]

    print("identity: {}\nendpoint: {}".format(identity, endpoint_id))

    account_sid = "ACd3a83bf4c0646baaba77cdc355567d1f"
    api_key = "SK4949cc25487c7bd8001f3e0f21165064"
    api_secret = "keQ3hukqsJ8PP9WNLs2g6Fels5umPCzM"
    token = AccessToken(account_sid, api_key, api_secret, identity, ttl=40000)

    ipm_service_sid = "IS3ba6938016464f7cbcba3d2fea297dca"
    endpoint_id = ipm_service_sid + identity + endpoint_id
    push_credential_sid = "CRe9c5eff29e744709d7df875f8a797bf0"
    ipm_grant = IpMessagingGrant(endpoint_id=endpoint_id, service_sid=ipm_service_sid, push_credential_sid=push_credential_sid)
    token.add_grant(ipm_grant)

    return HttpResponse(json.dumps({
        'identity': identity,
        'token': token.to_jwt()
    }))
