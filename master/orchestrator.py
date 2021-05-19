from flask import Flask, request, g
import os

app = Flask(__name__)

nodes = set()
queue = []


@app.route('/ping', methods=['POST'])
def accept_ping():
    data = request.form
    nodes.add(data['node_name'])
    print(f"Nodes in sync: {len(nodes)}")
    if queue:
        return queue[0]
    else:
        return f"Ping OK from {data['node_name']}", 200

@app.route('/work', methods=['GET'])
def work():
    queue.append('work')
    return 'Work queued'


if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)