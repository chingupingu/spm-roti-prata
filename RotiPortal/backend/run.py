from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from Render's environment variable, default to 5000 if not found
    port = int(os.getenv('PORT', 5000))
    # Bind to 0.0.0.0 to allow external access
    app.run(host='0.0.0.0', port=port)