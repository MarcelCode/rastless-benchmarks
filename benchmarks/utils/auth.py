from keycloak import KeycloakOpenID


def get_keycloak_bearer_token(settings) -> str:
    keycloak_openid = KeycloakOpenID(server_url=settings.keycloak_url,
                                     client_id=settings.keycloak_client_id,
                                     realm_name=settings.keycloak_realm_name,
                                     client_secret_key=settings.keycloak_client_secret)

    token = keycloak_openid.token(settings.username, settings.password)

    return f"Bearer {token['access_token']}"
