from app import app

# Gunicorn, Waitress, Docker will use this
application = app

# Optional: Run directly for development
if __name__ == "__main__":
   application.run(debug=True)
