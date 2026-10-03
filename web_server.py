import json
import sys
import http.server
import socketserver
import urllib.parse
from generator import SmartNotesGenerator

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 5000
generator = None

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Study Notes Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem;
        }

        .container {
            max-width: 1100px;
            width: 100%;
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #a78bfa, #38bdf8, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        header p {
            color: var(--text-muted);
            font-size: 1.1rem;
        }

        .badge {
            display: inline-block;
            background: rgba(139, 92, 246, 0.15);
            color: #c084fc;
            border: 1px solid rgba(139, 92, 246, 0.3);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            margin-top: 0.75rem;
            font-weight: 500;
        }

        .grid-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 768px) {
            .grid-layout {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .card-title {
            font-size: 1.2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        textarea {
            width: 100%;
            height: 220px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 1rem;
            color: #f1f5f9;
            font-size: 0.95rem;
            line-height: 1.6;
            resize: none;
            outline: none;
            transition: border-color 0.2s;
        }

        textarea:focus {
            border-color: var(--accent-purple);
        }

        .sample-buttons {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }

        .btn-sample {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 0.4rem 0.8rem;
            border-radius: 0.5rem;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-sample:hover {
            background: rgba(139, 92, 246, 0.2);
            color: #e2e8f0;
            border-color: var(--accent-purple);
        }

        .btn-submit {
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            color: #fff;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 0.75rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 1rem;
            transition: transform 0.1s, opacity 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .btn-submit:hover {
            opacity: 0.95;
            transform: translateY(-1px);
        }

        .btn-submit:active {
            transform: translateY(0);
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 1rem;
            text-align: center;
        }

        .stat-val {
            font-size: 1.6rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-cyan);
        }

        .stat-val.reduction {
            color: var(--accent-emerald);
        }

        .stat-lbl {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .output-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 1.25rem;
            min-height: 140px;
            font-size: 0.95rem;
            line-height: 1.6;
            color: #e2e8f0;
            white-space: pre-wrap;
            margin-bottom: 1.5rem;
        }

        .key-points-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .key-points-list li {
            background: rgba(139, 92, 246, 0.08);
            border-left: 3px solid var(--accent-purple);
            padding: 0.6rem 0.8rem;
            border-radius: 0 0.5rem 0.5rem 0;
            font-size: 0.9rem;
        }

        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .progress-bar-container {
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }

        .progress-bar-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #10b981, #06b6d4);
            transition: width 0.5s ease-out;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Smart Study Notes Generator</h1>
            <p>Summarize complex text paragraphs & compute text reduction metrics in real-time</p>
            <div class="badge">Model: Hugging Face Pre-trained Generative AI</div>
        </header>

        <div class="grid-layout">
            <!-- Left Card: Input -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Input Paragraph</div>
                    <span id="char-count" style="font-size:0.85rem; color:var(--text-muted)">0 words</span>
                </div>
                <textarea id="input-text" placeholder="Paste your study paragraph here..."></textarea>
                
                <div style="margin-top: 0.75rem;">
                    <span style="font-size: 0.85rem; color: var(--text-muted);">Quick Samples:</span>
                    <div class="sample-buttons">
                        <button class="btn-sample" onclick="loadSample(1)">AI Healthcare</button>
                        <button class="btn-sample" onclick="loadSample(2)">Renewable Energy</button>
                        <button class="btn-sample" onclick="loadSample(3)">Social Media</button>
                    </div>
                </div>

                <button class="btn-submit" onclick="generateNotes()">
                    <div class="spinner" id="btn-spinner"></div>
                    <span id="btn-text">Generate Notes</span>
                </button>
            </div>

            <!-- Right Card: Output & Metrics -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">Generated Summary & Metrics</div>
                </div>

                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-val" id="orig-count">0</div>
                        <div class="stat-lbl">Original Words</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val" id="summ-count">0</div>
                        <div class="stat-lbl">Summary Words</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val reduction" id="red-pct">0%</div>
                        <div class="stat-lbl">Reduction</div>
                    </div>
                </div>

                <div>
                    <span style="font-size:0.85rem; color:var(--text-muted)">Reduction Progress</span>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" id="progress-bar"></div>
                    </div>
                </div>

                <div style="margin-top: 1.25rem;">
                    <div style="font-size:0.9rem; font-weight:600; margin-bottom:0.4rem; color:var(--accent-cyan);">Summary Text</div>
                    <div class="output-box" id="summary-output">Generated study summary will appear here...</div>
                </div>

                <div>
                    <div style="font-size:0.9rem; font-weight:600; margin-bottom:0.4rem; color:#a78bfa;">Key Study Bullet Points</div>
                    <ul class="key-points-list" id="key-points-output">
                        <li>Key points will be extracted here...</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        const SAMPLES = {
            1: "Artificial intelligence is rapidly revolutionizing the healthcare industry by enhancing diagnostic precision, optimizing patient treatment plans, and streamlining administrative workflows. Machine learning algorithms can analyze vast amounts of medical imaging data, such as MRI scans and X-rays, to detect anomalies like tumors much faster and often more accurately than human radiologists. Furthermore, AI-powered predictive analytics enable hospitals to forecast patient admission rates, allocate critical resources efficiently, and customize personalized therapy regimens based on a patient's unique genetic profile. However, despite these overwhelming technological benefits, challenges regarding data privacy, algorythmic bias, and the necessity of human oversight remain crucial areas that require rigorous ethical standards and regulations.",
            2: "The global transition toward renewable energy sources has become one of the most critical imperatives of the 21st century. As fossil fuels continue to contribute significantly to greenhouse gas emissions and global warming, nations worldwide are investing heavily in solar, wind, and hydroelectric power infrastructure. Recent technological breakthroughs have dramatically reduced the manufacturing costs of photovoltaic solar panels and high-capacity battery storage systems, making clean energy economically competitive with traditional power grids. Nevertheless, integrating intermittent renewable sources into legacy energy infrastructure requires massive grid modernization, grid-scale storage solutions, and proactive international policy collaboration to achieve zero-carbon targets.",
            3: "Social media platforms have fundamentally altered contemporary human communication, social interaction, and information sharing. While these digital networks foster unprecedented global connectivity, allow instant knowledge access, and empower community building, extensive psychological studies highlight emerging concerns regarding mental health. Continuous exposure to curated digital lifestyles frequently leads to social comparison, anxiety, reduced self-esteem, and sleep disruption among adolescents and young adults. To mitigate these negative psychological side effects, experts strongly recommend implementing digital wellness practices, setting daily screen time limits, and cultivating mindful online engagement habits."
        };

        const inputText = document.getElementById('input-text');
        const charCount = document.getElementById('char-count');

        inputText.addEventListener('input', () => {
            const words = inputText.value.trim() ? inputText.value.trim().split(/\\s+/).length : 0;
            charCount.textContent = words + ' words';
        });

        function loadSample(num) {
            inputText.value = SAMPLES[num];
            inputText.dispatchEvent(new Event('input'));
        }

        async function generateNotes() {
            const text = inputText.value.trim();
            if (!text) {
                alert('Please enter or select a paragraph first!');
                return;
            }

            const btnSpinner = document.getElementById('btn-spinner');
            const btnText = document.getElementById('btn-text');
            btnSpinner.style.display = 'inline-block';
            btnText.textContent = ' Processing...';

            try {
                const response = await fetch('/api/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });

                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('orig-count').textContent = data.metrics.original_word_count;
                    document.getElementById('summ-count').textContent = data.metrics.summary_word_count;
                    document.getElementById('red-pct').textContent = data.metrics.reduction_percentage + '%';
                    document.getElementById('progress-bar').style.width = Math.min(100, data.metrics.reduction_percentage) + '%';
                    
                    document.getElementById('summary-output').textContent = data.summary;
                    
                    const kpList = document.getElementById('key-points-output');
                    kpList.innerHTML = '';
                    data.key_points.forEach(pt => {
                        const li = document.createElement('li');
                        li.textContent = pt;
                        kpList.appendChild(li);
                    });
                }
            } catch (err) {
                alert('Failed to communicate with generator backend: ' + err);
            } finally {
                btnSpinner.style.display = 'none';
                btnText.textContent = 'Generate Notes';
            }
        }
    </script>
</body>
</html>
"""

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == '/api/summarize':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                input_text = payload.get('text', '')
                
                global generator
                if generator is None:
                    generator = SmartNotesGenerator()
                    
                result = generator.generate_notes(input_text)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Not Found")

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server():
    global generator
    print("Initializing Smart Notes Generator Model...")
    model_name = os.environ.get("MODEL_NAME", "t5-small")
    generator = SmartNotesGenerator(model_name=model_name)
    
    env_port = os.environ.get("PORT")
    ports_to_try = [int(env_port)] if env_port else [5000, 8000, 8081, 8888, 10000]
    httpd = None
    active_port = None

    for port in ports_to_try:
        try:
            httpd = ReusableTCPServer(("0.0.0.0", port), RequestHandler)
            active_port = port
            break
        except Exception as err:
            print(f"Port {port} unavailable: {err}. Trying next port...")

    if httpd is None:
        print("Error: Could not bind server to any available port.")
        return

    print(f"\n[SUCCESS] Smart Study Notes Generator Web App running at http://0.0.0.0:{active_port}")
    print("Press Ctrl+C to stop the server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down web server.")

if __name__ == "__main__":
    start_server()
