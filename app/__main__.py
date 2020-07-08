"""Web app entry point"""
from app import get_app

app = get_app()

if __name__ == "__main__":
    app.run(port=8080)
