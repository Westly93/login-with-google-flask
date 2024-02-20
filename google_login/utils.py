import requests


def get_google_provider_cfg():
    from google_login import create_app

    app = create_app()
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
