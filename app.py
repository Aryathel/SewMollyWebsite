from dotenv import load_dotenv

from blueprints import App

# 199.34.228.168

load_dotenv()

app = App(__name__)


if __name__ == "__main__":
    app.run(debug=True, port=6894)
