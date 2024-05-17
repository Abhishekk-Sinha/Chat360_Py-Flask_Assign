from flask import Flask, request, render_template, jsonify
import json
import logging
from datetime import datetime
import glob

app = Flask(__name__)

# Function to setup a logger for a specific log file
def setup_logger(log_file):
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

# Initialize loggers for each log file
log_files = ['log1.log', 'log2.log', 'log3.log', 'log4.log', 'log5.log', 'log6.log', 'log7.log', 'log8.log', 'log9.log']
loggers = {log_file: setup_logger(log_file) for log_file in log_files}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_message():
    data = request.form
    api_name = data.get("api_name")
    if not api_name or f"{api_name}.log" not in loggers:
        return jsonify({"error": "Invalid API name"}), 400

    log_entry = {
        "level": data["level"],
        "log_string": data["log_string"],
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "metadata": {"source": f"{api_name}.log"}
    }

    loggers[f"{api_name}.log"].info(json.dumps(log_entry))
    return jsonify({"message": "Log entry added"}), 200

@app.route('/query_logs', methods=['POST'])
def query_logs():
    criteria = request.form.to_dict()
    all_logs = []

    for file in log_files:
        with open(file, 'r') as f:
            for line in f:
                log_entry = json.loads(line.strip())
                match = True
                for key, value in criteria.items():
                    if key in log_entry:
                        if log_entry[key] != value:
                            match = False
                            break
                    elif key in log_entry.get('metadata', {}):
                        if log_entry['metadata'][key] != value:
                            match = False
                            break
                    else:
                        match = False
                        break
                if match:
                    all_logs.append(log_entry)
    
    return render_template('form.html', logs=all_logs)

if __name__ == '__main__':
    app.run(debug=True)
