"""
Fantasy Football Dashboard — Flask App
----------------------------------------
Serves the dashboard HTML and proxies ESPN API requests.
Deploy to Railway, Render, or any Python host.

Environment variables (set in Railway dashboard):
  ESPN_S2   — your ESPN espn_s2 cookie value
  SWID      — your ESPN SWID cookie value
  SECRET_KEY — any random string for Flask sessions (optional)
"""

import os
import requests
from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# ── ESPN credentials ──────────────────────────────────────────
# Read from environment variables (set these in Railway/Render dashboard)
# Falls back to hardcoded values for local dev
ESPN_S2 = os.environ.get(
    'ESPN_S2',
    'AEBPKiE8vKWeIYH8704od6IPjj3z101TYRjvH6s1M1FN%2BqTRdyvs%2FsnlLLgaDDrs2qFLNJcpdiRbfX6qhSPSBQBZ8Pk655ZNyiKP0rFD4fzPbky7A0LIq74VEfUCeMX6pf6isDnhUfbY3OsTZ75GCs4DFPNdSR%2BOqHMTZQqige537owaojTR4rA8rNfwhgvgNtKikpkEH5SKHbHpKiNirzBjD%2FpYYGtqqfg4mhkMxZ%2Bq24ismLaXuCR3gJbtjAe5fv6guJvZcfWv9pXg5ZVhWTumIIV9YSJn%2Bn1SHigA6Ig35g%3D%3D'
)
SWID = os.environ.get('SWID', '{B7FC191D-8441-4913-9A81-75BA13AEF6E3}')

# ── ESPN API bases ─────────────────────────────────────────────
MODERN_BASE     = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl'
SCOREBOARD_BASE = 'https://fantasy.espn.com/apis/v3/games/ffl'
LEGACY_BASE     = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leagueHistory'

ESPN_HEADERS = {
    'Cookie':     f'espn_s2={ESPN_S2}; SWID={SWID}',
    'Accept':     'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer':    'https://fantasy.espn.com/',
    'Origin':     'https://fantasy.espn.com',
}


def proxy_espn(espn_url):
    """Forward a request to ESPN and return the response."""
    try:
        print(f'  --> {espn_url}')
        resp = requests.get(espn_url, headers=ESPN_HEADERS, timeout=20)
        print(f'  <-- {resp.status_code} ({len(resp.content):,} bytes)')
        return Response(
            resp.content,
            status=resp.status_code,
            content_type=resp.headers.get('Content-Type', 'application/json'),
        )
    except requests.exceptions.Timeout:
        return jsonify({'error': 'ESPN API timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Routes ─────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the dashboard HTML."""
    return send_from_directory('static', 'fantasy_dashboard.html')


@app.route('/ping')
def ping():
    return jsonify({'status': 'ok', 'proxy': 'ESPN Fantasy Flask v1'})


@app.route('/scoreboard/<path:rest>')
def scoreboard(rest):
    """fantasy.espn.com endpoint — better for live scores."""
    qs  = request.query_string.decode()
    url = f'{SCOREBOARD_BASE}/{rest}' + (f'?{qs}' if qs else '')
    return proxy_espn(url)


@app.route('/legacy/<path:rest>')
def legacy(rest):
    """Pre-2018 leagueHistory endpoint."""
    qs  = request.query_string.decode()
    url = f'{LEGACY_BASE}/{rest}' + (f'?{qs}' if qs else '')
    return proxy_espn(url)


@app.route('/seasons/<path:rest>')
def modern(rest):
    """Modern lm-api-reads endpoint (2018+)."""
    qs  = request.query_string.decode()
    url = f'{MODERN_BASE}/seasons/{rest}' + (f'?{qs}' if qs else '')
    return proxy_espn(url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f'Starting Fantasy Dashboard on port {port}')
    app.run(host='0.0.0.0', port=port, debug=False)
