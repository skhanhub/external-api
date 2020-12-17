from routes import app

if __name__ == "__main__":
    app.run(host="localhost", port=5000, use_reloader=True, threaded=True)