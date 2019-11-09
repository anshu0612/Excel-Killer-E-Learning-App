
def lambda_handler(event, context):
    method = event.get('httpMethod', {})

    with open('index.html', encoding='utf8') as file:
        indexPage = file.read()

    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": indexPage
        }