from flask import Flask, render_template_string, request
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# List available models automatically
models = genai.list_models()

working_model = None

for m in models:
    if "generateContent" in m.supported_generation_methods:
        working_model = m.name
        break

print("Using model:", working_model)

model = genai.GenerativeModel(working_model)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ReviewGenius AI</title>
<style>
body{
    font-family: Arial;
    background:#f4f4f4;
    padding:40px;
}
.container{
    max-width:700px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:12px;
}
textarea{
    width:100%;
    height:150px;
    padding:10px;
}
button{
    background:#007bff;
    color:white;
    border:none;
    padding:12px 20px;
    margin-top:15px;
    border-radius:6px;
    cursor:pointer;
}
.output{
    margin-top:20px;
    background:#f0f0f0;
    padding:20px;
    border-radius:8px;
    white-space:pre-wrap;
}
</style>
</head>
<body>

<div class="container">
<h1>ReviewGenius AI</h1>

<form method="POST">
<textarea name="review" placeholder="Enter customer review"></textarea>
<br>
<button type="submit">Analyze</button>
</form>

{% if result %}
<div class="output">
{{ result }}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        review = request.form["review"]

        prompt = f'''
Analyze this review and provide:
1. Sentiment
2. Summary
3. Suggestions

Review:
{review}
'''

        try:
            response = model.generate_content(prompt)
            result = response.text
        except Exception as e:
            result = f"Error: {e}"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)