from openai import OpenAI
from dotenv import dotenv_values
from flask import Flask, render_template, request
import json

config = dotenv_values(".env")
client = OpenAI(api_key=config["OPENAI_API_KEY"])

message=[
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Give me the top 10 most watched movies of all time" }
]

def get_colors(msg):    
    prompt=f"""
    You are a color palette generating assistant that responds to text prompts for color palettes. You should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color paletter into a list of colors: The mediterranean sea.
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Desired format: A JSON array of hex colors

    Q: Convert the following verbal description of a color paletter into a list of colors: {msg}
    A:

    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
            messages = [
                {
                    'role': 'user',
                    "content": prompt
                }
            ],
            stream=False
        )
    
    colors = json.loads(response.choices[0].message.content)
    return colors

    # print(response.choices[0].message.content)




app = Flask(__name__, 
            template_folder='templates', 
            static_url_path='',
            static_folder='static')

@app.route("/palette", methods=["POST"])
def promt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@app.route("/")
def index():
    return render_template("index.html")

if __name__ ==  "__main__":
    app.run(debug=True)