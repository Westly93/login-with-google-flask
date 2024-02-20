import sys
import os
from google_login import create_app

if __name__ == "__main__":
    app = create_app()
    context = (app.config['SSL_CERTIFICATE'], app.config['SSL_KEY'])
    app.run(debug=True, ssl_context=context)
