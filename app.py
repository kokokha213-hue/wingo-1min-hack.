from flask import Flask, request, jsonify, send_from_directory
from collections import Counter
import os

app = Flask(__name__, static_folder='static', static_url_path='')

COLORS = { 'red':[0,2,4,6,8], 'green':[1,3,5,7,9], 'violet':[0,5] }

def size_of(n): return 'BIG' if n>=5 else 'SMALL'

def combine_predictors(last_results):
    scores = {i:1.0 for i in range(10)}
    cnt = Counter(last_results)
    for n,c in cnt.items():
        scores[n] += c*1.5
    # recency bias
    for i,n in enumerate(reversed(last_results)):
        scores[n] += (i+1)*0.3
    best = max(scores.items(), key=lambda x: x[1])[0]
    avg = sum(scores.values())/10.0
    confidence = min(98, int(50 + (scores[best]-avg)*10))
    color = '🟢' if best in COLORS['green'] else '🔴'
    if best in COLORS['violet']: color='🟣'
    return {'number': best, 'color': color, 'size': size_of(best), 'confidence': confidence}

# Simple in-memory memory per-demo (not persistent across restarts for free-tier)
AI_MEMORY = {
    'current_level': 1,
    'total_invested': 10,
    'last_10_results': [3,3,8,2,3,9,0,3,7,5],
    'last_top_logic': 'Frequency+Recency Heuristic',
    'last_result': 'N/A'
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    last10 = data.get('last_10_results') or AI_MEMORY.get('last_10_results')
    if not isinstance(last10, list) or len(last10)==0:
        return jsonify({'error':'Provide last_10_results as a list of digits 0-9'}), 400
    last10 = [int(x) for x in last10][:10]
    AI_MEMORY['last_10_results'] = last10
    pred = combine_predictors(last10)
    # return block similar to UI
    response = {
        'analysis':'COMPLETE',
        'pid':'PID-' + str(abs(hash(''.join(map(str,last10))))%1000000),
        'prediction': pred,
        'ai_memory_state': AI_MEMORY
    }
    return jsonify(response), 200

@app.route('/')
def root():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:p>')
def static_files(p):
    return send_from_directory('static', p)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
