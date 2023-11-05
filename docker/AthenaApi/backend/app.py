from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from index import handler
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def query_gpt():
  return handler(None, None)


@app.route("/query", methods=['POST'])
@cross_origin()
def query_gpt_post():
  data = request.json
  question = data.get('question')
  context = data.get('context')
  if not question or not context:
    return jsonify({'error': 'Both question and context are required'}), 400
  return handler({
    'question': question,
    'context': context
  }, None)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0',port=80)