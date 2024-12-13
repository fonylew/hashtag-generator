import datetime
import json
import os

import functions_framework
from google import genai
from google.cloud import pubsub


@functions_framework.http
def publish(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    request_json = request.get_json(silent=True)
    request_args = request.args

    publisher = pubsub.PublisherClient()
    topic_path = os.getenv("TOPIC")

    client = genai.Client(api_key=os.getenv("API_KEY"))

    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = None

    if request_json and "message" in request_json:
        message = request_json["message"]
    elif request_args and "message" in request_args:
        message = request_args["message"]
    else:
        message = None

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f'Please classify the message "{message}" into array of appropriate hashtags without hash symbol as concise as possible, no more than five. If the message is a question, please put "question" in the hashtag . The response should be strings delimited by comma without any other special character except comma, do not put new line symbol. Strictly as follow hashtag1,hashtag2,..',
    )

    data = {
        "timestamp": str(datetime.datetime.now()),
        "name": name,
        "message": message,
        "response": response.text,
    }
    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))

    return (data, 200, headers)
