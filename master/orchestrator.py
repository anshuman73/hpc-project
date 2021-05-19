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
    nodes[data['node_name']] = [data['node_name'], time.strftime("%H:%M:%S", time.localtime(float(data['alive_since']))), time.strftime("%H:%M:%S", time.localtime()), data['is_computing']]
    print(f"Nodes in sync: {len(nodes)}")
    if queue and not data['is_computing'] == 'True':
        print('Hello')
        return jsonify(queue.pop(0)), 202
    else:
        return f"Ping OK from {data['node_name']}", 200


@app.route('/start', methods=['GET'])
def work():
    for lr in [0.01,0.001,0.0001,0.00001]:
        for bs in [8,16,32,64,128]:
            for ep in [2,5,10,15,20]:
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
    print(len(queue))
    return 'Work queued'


@app.route('/post_results', methods=['POST'])
def accept_result():
    result = request.json
    results.append(result)
    return 'OK', 200


@app.route('/results', methods=['GET'])
def get_results():
    return render_template('results.html', results=results)


@app.route('/nodes', methods=['GET'])
def get_nodes():
    return render_template('nodes.html', nodes=nodes)


@app.route('/reset', methods=['GET'])
def do_reset():
    nodes = {}
    queue = []
    results = []

if __name__ == '__main__':
    app.debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)