# This activity requires Python 3.7 runtime
# -*- coding: utf-8 -*-
import json
import traceback
import doctest
import io
import sys
import boto3
from uuid import uuid4


def lambda_handler(event, context):
    def run_local(requestDict):

        byteCodeChecker = "\ndef byteCodeChecker(function, field, value):\n import dis\n byteCode = dis.Bytecode(function)\n fields = {'OPNAME':0, 'ARGREPR':3} \n for instruction in byteCode:\n  if instruction[fields[field]] == value:\n   return f'found {value}'\n else:\n  return f'{value} not found'"
        codeInfoChecker = "\ndef codeInfoChecker(function, value):\n import dis\n codeInfo = dis.code_info(function)\n if value in codeInfo:\n  return f'found {value}'\n else:\n  return f'{value} not found'"
        solution = requestDict['solution'] + codeInfoChecker + byteCodeChecker
        tests = requestDict['tests']
        output = io.StringIO()
        sys.stdout = output
        try:
            namespace = {}
            compiled = compile('import json', 'submitted code', 'exec')
            exec(compiled, namespace)
            compiled = compile(solution, 'submitted code', 'exec')
            exec(compiled, namespace)
            namespace['YOUR_SOLUTION'] = solution.strip()
            namespace['LINES_IN_YOUR_SOLUTION'] = len(solution.strip().splitlines())
            test_cases = doctest.DocTestParser().get_examples(tests)
            execute_test_cases(test_cases, namespace)
            results, solved = execute_test_cases(test_cases, namespace)
            printed = output.getvalue()
            responseDict = {"solved": solved, "results": results, "printed": printed}
            responseJSON = json.dumps(responseDict)
            return responseJSON
        except Exception as e:
            errors = traceback.format_exc()
            responseDict = {'errors': '%s' % errors}
            responseJSON = json.dumps(responseDict)
            return responseJSON

    def execute_test_cases(testCases, namespace):
        resultList = []
        solved = True
        for e in testCases:
            if not e.want:
                exec(e.source) in namespace
                continue
            call = e.source.strip()
            got = eval(call, namespace)
            expected = eval(e.want, namespace)
            correct = True
            if got == expected:
                correct = True
            else:
                correct = solved = False
            resultDict = {'call': call, 'expected': expected, 'received': "%(got)s" % {'got': got}, 'correct': correct}
            resultList.append(resultDict)
        return resultList, solved

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

    if method == 'POST':
        solved = False
        question = 0
        import re
        bodyContent = event.get('body', {})
        parsedBodyContent = json.loads(bodyContent)
        testCases = re.sub('&zwnj;.*&zwnj;', '', parsedBodyContent["shown"]["0"], flags=re.DOTALL)
        solution = parsedBodyContent["editable"]["0"]
        graph_url = ''
        if 'Practise 1' in solution:
            graph_url = 'https://excel-killer-images.s3.amazonaws.com/g6.png'
            question = 1
        if 'Practise 2' in solution:
            graph_url = 'https://excel-killer-images.s3.amazonaws.com/g7.png'
            question = 2
        if 'Practise 3' in solution:
            graph_url = 'https://excel-killer-images.s3.amazonaws.com/g8.png'
            question = 3
        timeout = False

        # handler function that tell the signal module to execute
        # our own function when SIGALRM signal received.
        def timeout_handler(num, stack):
            print("Received SIGALRM")
            raise Exception("processTooLong")

        # register this with the SIGALRM signal
        # signal.signal(signal.SIGALRM, timeout_handler)

        # signal.alarm(10) tells the OS to send a SIGALRM after 10 seconds from this point onwards.
        # signal.alarm(10)

        # After setting the alarm clock we invoke the long running function.
        try:
            jsonResponse = run_local({"solution": solution, "tests": testCases})
        except Exception as ex:
            if "processTooLong" in ex:
                timeout = True
                print("processTooLong triggered")
        # set the alarm to 0 seconds after all is done
        finally:
            # signal.alarm(0)
            pass
        jsonResponseData = json.loads(jsonResponse)
        solvedStatusText = expectedText = receivedText = callText = textResults = tableContents = ""
        overallResults = """<span class="md-subheading">All tests passed: {0}</span><br/>""".format(
            str(jsonResponseData.get("solved")))
        numTestCases = len(re.findall('>>>', testCases))
        resultContent = jsonResponseData.get('results')
        textBackgroundColor = "#ffffff"

        if resultContent:
            for i in range(len(resultContent)):
                expectedText = resultContent[i]["expected"]
                receivedText = resultContent[i]["received"]
                correctText = resultContent[i]["correct"]
                callText = resultContent[i]["call"]
                if str(expectedText) == str(receivedText):
                    solved = True
                    textResults = textResults + "\nHurray! You have passed the test case. You called {0} and received {1} against the expected value of {2}.\n".format(
                        callText, receivedText, expectedText)
                    textBackgroundColor = "#b2d8b2"
                else:
                    textResults = textResults + "\nThe test case eludes your code so far but try again! You called {0} and received {1} against the expected value of {2}.\n".format(
                        callText, receivedText, expectedText)
                    textBackgroundColor = "#ff9999"
                tableContents = tableContents + """
                <tr bgcolor={4}>
                    <td>{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                    <td>{3}</td>
                </tr>
                """.format(callText, expectedText, receivedText, correctText, textBackgroundColor)
        solvedStatusText = str(jsonResponseData.get("solved")) or "error"
        textResults = """All tests passed: {0}\n""".format(solvedStatusText) + textResults
        if not resultContent:
            textResults = "Your test is passing but something is incorrect..."

        if timeout or jsonResponseData.get("errors"):
            textResults = "An error - probably related to code syntax - has occured. Do look through the JSON results to understand the cause."
            tableContents = """
                <tr>
                    <td></td>
                    <td></td>
                    <td>error</td>
                    <td></td>
                </tr>
                """
        htmlResults = """
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
                </head>
                <body>
                    <div>
                        {0}
                        <span class="md-subheading tableTitle">Tests</span>
                        <table>
                             <thead>
                                <tr>
                                    <th>Called</th>
                                    <th>Expected</th>
                                    <th>Received</th>
                                    <th>Correct</th>
                                </tr>
                            </thead>
                            <tbody>
                                {1}
                            </tbody>
                        </table>
                        <img src="{2}" alt="graph/>
                    </div>
                </body>
                <style>
                br {{
                    display:block;
                    content:"";
                    margin:1rem
                }}
                table{{
                    text-align:center
                }}
                .tableTitle{{
                    text-decoration:underline
                }}
                </style>
            </html>
            """.format(overallResults, tableContents, graph_url)
        try:
            client = boto3.resource('dynamodb')
            table = client.Table("excel-killer")
            table.put_item(Item={'id': str(uuid4()), 'activity': 'visualize', 'question': question, 'solved': solved})
        except Exception as e:
            print(e)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "isComplete": jsonResponseData.get("solved"),
                "jsonFeedback": jsonResponseData,
                "htmlFeedback": htmlResults,
                "textFeedback": textResults,
                "graph": graph_url
            })
        }