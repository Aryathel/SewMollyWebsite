from blueprints import App

app = App(__name__)

if __name__ == "__main__":
    app.run(debug=True, port=6894)
