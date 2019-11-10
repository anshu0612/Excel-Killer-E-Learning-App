from flask import Flask, render_template_string
from cleaning_act.lambda_function import lambda_handler
from flask import request
app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    str = lambda_handler({"httpMethod": "GET"}, '')
    str = "{% raw %}" + str["body"] + "{% endraw %}"
    return render_template_string(str)


@app.route('/', methods=["POST"])
def post_method():
    a = """
    {"shown":{"0":">>> solution()\\n62.33"},"editable":{"0":"import pandas as pd\\nimport numpy as np\\nfrom random import randint\\n\\ndef solution():\\n\\t# Do not remove the below line, it is used for testing your solution\\n\\tnp.random.seed(0)\\n\\n\\tdf = pd.DataFrame(data= {\\n\\t\\t'player': ['Matt', 'Sylvia', 'Javier'],\\n\\t\\t'round1': [90, 80, 82],\\n\\t\\t'round2': [76, 66,  75]\\n\\t})\\n\\tdef new_round(prev_score):\\n\\t\\treturn prev_score - np.random.randint(1,20)\\n\\n\\t# Let’s play a game, every player starts with 100 points and in round 1 loses random amount of points.\\n\\t# Apply the above given function and generate the scores for round 3, remember to use scores for round 2 for this.\\n\\n\\tdf['round3'] = df['round2'].apply(lambda curr_score: new_round(curr_score))\\n\\n\\t# Compute the average of the round 3\\n\\tround3_avg = df['round3'].mean()\\n\\treturn round(round3_avg,2)"}}
    """
    print ("HEY")
    print(request.body)
    str = lambda_handler({"httpMethod": "POST", "body": a}, '')
    return str["body"]


if __name__ == '__main__':
    app.run(debug=True)


