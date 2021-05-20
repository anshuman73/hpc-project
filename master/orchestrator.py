from flask import Flask, request, g, jsonify, render_template, redirect
import os
import time

app = Flask(__name__)

nodes = {}
queue = []
results = []


@app.route('/ping', methods=['POST'])
def accept_ping():
    data = request.form
    ip_address = request.remote_addr
    nodes[data['node_name']] = [data['node_name'], time.strftime("%H:%M:%S", time.localtime(float(data['alive_since']))), time.strftime("%H:%M:%S", time.localtime()), data['is_computing'], ip_address]
    print(f"Nodes in sync: {len(nodes)}")
    if queue and not data['is_computing'] == 'True':
        return jsonify(queue.pop(0)), 202
    else:
        return f"Ping OK from {data['node_name']}", 200


@app.route('/start', methods=['POST'])
def queue_work():
    data = request.form
    epochs = [int(x) for x in data['epochs'].split(',')]
    batch_sizes = [int(x) for x in data['batchsize'].split(',')]
    learning_rate = [float(x) for x in data['learningrate'].split(',')]
    for ep in epochs:
        for bs in batch_sizes:
            for lr in learning_rate:
                data={
                    "configuration":{
                        "learning_rate":lr,
                        "batch_size":bs,
                        "epoch":ep
                    },
                    "results":{
                        
                    }
                }
                queue.append(data)
    return redirect('results')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post_results', methods=['POST'])
def accept_result():
    result = request.json
    results.append(result)
    return 'OK', 200


@app.route('/results', methods=['GET'])
def get_results():
    return render_template('results.html', processed = len(results), results=results, queue=queue)


@app.route('/nodes', methods=['GET'])
def get_nodes():
    return render_template('nodes.html', nodes=nodes)


@app.route('/reset', methods=['GET'])
def do_reset():
    nodes = {}
    queue = []
    results = []
    return 'OK'


if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)