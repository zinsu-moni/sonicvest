from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Work</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #4A90E2 0%, #357ABD 50%, #1E5F99 100%);
            min-height: 100vh;
            color: white;
            padding: 20px 16px 100px 16px;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 24px; font-weight: 600; }
        .invitation-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        .invitation-label { color: rgba(255, 255, 255, 0.8); font-size: 14px; margin-bottom: 8px; }
        .invitation-code-container { display: flex; justify-content: space-between; align-items: center; }
        .invitation-code { font-size: 18px; font-weight: 600; color: white; }
        .copy-btn {
            background: #FF8C00;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
        }
        .level-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            backdrop-filter: blur(10px);
        }
        .level-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .level-info { display: flex; align-items: center; gap: 12px; }
        .level-icon {
            width: 32px; height: 32px; border-radius: 8px;
            display: flex; align-items: center; justify-content: center; font-size: 18px;
        }
        .level-1 .level-icon { background: #FFD700; }
        .level-2 .level-icon { background: #87CEEB; }
        .level-3 .level-icon { background: #87CEEB; }
        .level-title { font-size: 16px; font-weight: 600; color: white; }
        .reward-badge { background: #FFD700; color: #333; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .view-btn { background: #333; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
        .stats-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; text-align: center; }
        .stat-item { display: flex; flex-direction: column; gap: 4px; }
        .stat-value { font-size: 20px; font-weight: 700; color: white; }
        .stat-label { font-size: 12px; color: rgba(255, 255, 255, 0.7); }
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px); padding: 12px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
        .nav-container { display: flex; justify-content: space-around; align-items: center; max-width: 600px; margin: 0 auto; }
        .nav-item { display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #666; }
        .nav-item.active { color: #4A90E2; }
        .nav-icon { width: 24px; height: 24px; margin-bottom: 4px; fill: currentColor; }
        .nav-text { font-size: 12px; font-weight: 500; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Team Work</h1>
    </div>

    <div class="invitation-card">
        <div class="invitation-label">Invitation Code</div>
        <div class="invitation-code-container">
            <span class="invitation-code">YSVCSV50</span>
            <button class="copy-btn" onclick="copyCode()">Copy</button>
        </div>
    </div>

    <div class="level-card level-1">
        <div class="level-header">
            <div class="level-info">
                <div class="level-icon">🥇</div>
                <span class="level-title">1st Level</span>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="reward-badge">Reward 10%</span>
                <button class="view-btn">View</button>
            </div>
        </div>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">3</div>
                <div class="stat-label">Total People</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">₹0</div>
                <div class="stat-label">Total Recharge</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">₹0</div>
                <div class="stat-label">Total Commission</div>
            </div>
        </div>
    </div>

    <div class="level-card level-2">
        <div class="level-header">
            <div class="level-info">
                <div class="level-icon">🥈</div>
                <span class="level-title">2nd Level</span>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="reward-badge">Reward 0%</span>
                <button class="view-btn">View</button>
            </div>
        </div>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">0</div>
                <div class="stat-label">Total People</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">₹0</div>
                <div class="stat-label">Total Recharge</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">₹0</div>
                <div class="stat-label">Total Commission</div>
            </div>
        </div>
    </div>

    <div class="level-card level-3">
        <div class="level-header">
            <div class="level-info">
                <div class="level-icon">🥉</div>
                <span class="level-title">3rd Level</span>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="reward-badge">Reward 0%</span>
                <button class="view-btn">View</button>
            </div>
        </div>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">0</div>
                <div class="stat-label">Total People</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">₹0</div>
                <div class="stat-label">Total Recharge</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">₹0</div>
                <div class="stat-label">Total Commission</div>
            </div>
        </div>
    </div>

    <div class="bottom-nav">
        <div class="nav-container">
            <a href="#" class="nav-item">
                <svg class="nav-icon" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                <span class="nav-text">Home</span>
            </a>
            <a href="#" class="nav-item">
                <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                <span class="nav-text">Plans</span>
            </a>
            <a href="#" class="nav-item active">
                <svg class="nav-icon" viewBox="0 0 24 24"><path d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2zm4 18v-6h2.5l-2.54-7.63A1.5 1.5 0 0 0 18.54 8H16.5c-.54 0-1.04.31-1.28.8L12.5 14 10 11.5c-.28-.28-.65-.5-1.05-.5H6c-.83 0-1.5.67-1.5 1.5S5.17 14 6 14h2.5l3 3 2.5-5.5L16 18v4h4z"/></svg>
                <span class="nav-text">Team</span>
            </a>
            <a href="#" class="nav-item">
                <svg class="nav-icon" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                <span class="nav-text">Profile</span>
            </a>
        </div>
    </div>

    <script>
        function copyCode() {
            navigator.clipboard.writeText('YSVCSV50').then(() => {
                alert('Referral code copied!');
            });
        }
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    print("Starting app at http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
