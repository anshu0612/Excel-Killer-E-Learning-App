import boto3
import json
from jinja2 import Template
from uuid import uuid4
from urllib.parse import urlparse, parse_qs

def lambda_handler(event, context):
    method = event.get('httpMethod', {})

    def get_landing_page():
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
        like_count = {
            "basics": 0,
            "understanding": 0,
            "cleaning": 0,
            "visualize": 0
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
        table_likes = client.Table("excel-killer-likes")
        resp_likes = table_likes.scan(
            ProjectionExpression='activity'
        )
        for item in resp_likes['Items']:
            like_count[item["activity"]] += 1
        with open('index.html', encoding='utf8') as file:
            template = Template(file.read())
            index_page = template.render(activity_counts=activity_counts, like_count=like_count)
        return index_page

    if method == 'GET':
        index_page = get_landing_page()
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": index_page
        }
    if method == 'POST':
        body_content = event.get('body', '')
        qs = parse_qs(body_content)
        client = boto3.resource('dynamodb')
        table = client.Table("excel-killer-likes")
        activity = str(qs.get('act', [''])[0])
        table.put_item(Item={'id': str(uuid4()), 'activity': activity})
        index_page = get_landing_page()
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": index_page
        }
