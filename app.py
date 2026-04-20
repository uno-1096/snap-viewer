from flask import Flask, render_template, jsonify, request, Response
import requests
import re
import json

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
}

@app.route('/timeline/<username>')
def timeline(username):
    return render_template('timeline.html', username=username)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stories/<username>')
def get_stories(username):
    try:
        url = f'https://story.snapchat.com/s/{username}'
        r = requests.get(url, headers=HEADERS, allow_redirects=True)
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', r.text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            return jsonify(data)
        else:
            return jsonify({'error': 'Could not find story data'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url or url == 'undefined':
        return 'No URL', 400
    r = requests.get(url, headers=HEADERS, stream=True)
    return Response(r.content, content_type=r.headers.get('Content-Type', 'image/jpeg'))

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url or url == 'undefined':
        return 'No URL provided', 400
    r = requests.get(url, headers=HEADERS, stream=True)
    content_type = r.headers.get('Content-Type', 'video/mp4')
    ext = 'mp4' if 'video' in content_type else 'jpg'
    username = request.args.get('username', 'snap')
    index = request.args.get('index', '0')
    filename = f'{username}_snap_{index}.{ext}'
    return Response(
        r.content,
        content_type=content_type,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
