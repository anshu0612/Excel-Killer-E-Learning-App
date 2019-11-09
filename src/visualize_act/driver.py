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
    # df = solution()\\\\n\\\\ndf1 = pd.DataFrame(
    #     data={'player': ['Matt', 'Sylvia', 'Javier'], 'score': [10.1, 15.0, 20.0]})\\\\npd.testing.assert_frame_equal(df,
    #                                                                                                                 df1)
    a = """
    {"shown":{"0":""},"editable":{"0":"import pandas as pd\\nimport numpy as np\\n\\ndef solution():\\n\\t# Start Coding from here\\n\\t# TODO: Read csv file ('https://excelkiller-data.s3.amazonaws.com/Fruits1.csv') and save it into DataFrame 'df'\\n\\tdf = pd.read_csv('https://excelkiller-data.s3.amazonaws.com/Fruits1.csv')\\n\\t# End Coding from here\\n\\n\\t#Return created DataFrame\\n\\treturn df.to_dict()"}}
    """
    # json.loads(a)
    str = lambda_handler({"httpMethod": "POST", "body": a}, '')
    return str["body"]


if __name__ == '__main__':
    app.run(debug=True)


