from flask import Flask, render_template_string
from lambda_function import lambda_handler

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    str = lambda_handler({"httpMethod": "GET"}, '')
    str = "{% raw %}" + str["body"] + "{% endraw %}"
    return render_template_string(str)


@app.route('/', methods=["POST"])
def post_method():
    # df = solution()\\n\\ndf1 = pd.DataFrame(
    #     data={'player': ['Matt', 'Sylvia', 'Javier'], 'score': [10.1, 15.0, 20.0]})\\npd.testing.assert_frame_equal(df,
    #                                                                                                                 df1)
    a = """
    {"shown":{"0":">>> solution()\\n{'Item': {0: 'Apple ', 1: 'Peach', 2: 'Lemon', 3: 'Pineapple', 4: 'Watermelon', 5: 'Starfruit'}, 'Price per item, SG$': {0: 0.2, 1: 0.4, 2: 0.3, 3: 2.0, 4: 3.0, 5: 0.3}, 'Quantity': {0: 6, 1: 25, 2: 8, 3: 14, 4: 5, 5: 14}}"},"editable":{"0":"import pandas as pd\\n\\ndef solution():\\n\\t#read the csv ('https://excelkiller-data.s3.amazonaws.com/Fruits.csv') and save data in DataFrame df\\n\\tdf = pd.read_csv('https://excelkiller-data.s3.amazonaws.com/Fruits.csv')\n\n\t# Start Coding from here\n\t# TODO: Select items and their quantity from df and save it into new DataFrame - 'df2'\n\t#Hint: If you want to check exact column names use .columns function\n\tdf2 = df[['Item', 'Quantity']]\n\t# End Coding from here\n\n\t#Return new DataFrame\n\tdf2.to_dict()"}}
    """
    # json.loads(a)
    str = lambda_handler({"httpMethod": "POST", "body": a}, '')
    return str["body"]


if __name__ == '__main__':
    app.run(debug=True)


