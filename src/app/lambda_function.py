import boto3
from jinja2 import Template


def lambda_handler(event, context):
    method = event.get('httpMethod', {})
    activity_counts = {
        "basics": {1: {"correct": 0, "incorrect": 0}, 2: {"correct": 0, "incorrect": 0},
                   3: {"correct": 0, "incorrect": 0}, 4: {"correct": 0, "incorrect": 0}},
        "understanding": {1: {"correct": 0, "incorrect": 0}, 2: {"correct": 0, "incorrect": 0},
                          3: {"correct": 0, "incorrect": 0}, 4: {"correct": 0, "incorrect": 0}},
        "cleaning": {1: {"correct": 0, "incorrect": 0}, 2: {"correct": 0, "incorrect": 0},
                     3: {"correct": 0, "incorrect": 0}},
        "visualize": {1: {"correct": 0, "incorrect": 0}, 2: {"correct": 0, "incorrect": 0},
                      3: {"correct": 0, "incorrect": 0}}
    }
    client = boto3.resource('dynamodb')
    table = client.Table("excel-killer")
    resp = table.scan(
        ProjectionExpression='activity, question, solved'
    )
    for item in resp['Items']:
        question_type = "incorrect"
        if item["solved"]:
            question_type = "correct"
        activity_counts[item["activity"]][item["question"]][question_type] += 1
    with open('index.html', encoding='utf8') as file:
        template = Template(file.read())
        index_page = template.render(activity_counts=activity_counts)
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": index_page
        }
