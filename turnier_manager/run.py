#!/usr/bin/env python3
"""
TurnierManager - Application Entry Point
"""
import os
from app import create_app
from app.config import config

# Get config from environment or default to development
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config.get(config_name, config['default']))

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')

    print(f"\n{'='*50}")
    print(f"  TurnierManager")
    print(f"  Running on http://{host}:{port}")
    print(f"  Environment: {config_name}")
    print(f"{'='*50}\n")

    app.run(host=host, port=port, debug=app.config['DEBUG'])
