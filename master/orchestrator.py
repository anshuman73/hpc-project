from flask import Flask, request, g, jsonify, render_template
import os
import time

app = Flask(__name__)

nodes = {}
queue = []
results = []


@app.route('/ping', methods=['POST'])
def accept_ping():
    data = request.form
    nodes[data['node_name']] = [data['node_name'], data['alive_since'], time.localtime(), data['is_computing']]
    print(f"Nodes in sync: {len(nodes)}")
    if queue and not data['is_computing']:
        return jsonify(queue.pop()), 202
    else:
        return f"Ping OK from {data['node_name']}", 200


@app.route('/start', methods=['GET'])
def work():
    for lr in [0.01,0.001,0.0001,0.00001]:
        for bs in [8,16,32,64,128]:
            for ep in [5,10,15,20,25,30,35]:
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
    return 'Work queued'


@app.route('/post_results', methods=['POST'])
def accept_result():
    result = request.json
    results.append(result)
    return 'OK', 200


@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html', results=results)


@app.route('/nodes', methods=['GET'])
def nodes():
    return render_template('nodes.html', nodes=nodes)


if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)