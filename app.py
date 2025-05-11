from flask import Flask, render_template, request, send_file
import xmltodict
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['JSON_FOLDER'] = 'downloads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['JSON_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    json_data = None
    json_filename = None

    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.xml'):
            xml_content = uploaded_file.read()
            try:
                dict_data = xmltodict.parse(xml_content)
                json_data = dict_data

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                json_filename = f"converted_{timestamp}.json"
                json_path = os.path.join(app.config['JSON_FOLDER'], json_filename)

                with open(json_path, 'w') as f:
                    json.dump(dict_data, f, indent=4)

            except Exception as e:
                return f"Error parsing XML: {e}"
        else:
            return "Please upload a valid XML file."

    return render_template('index.html', json_data=json_data, json_filename=json_filename)

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['JSON_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

