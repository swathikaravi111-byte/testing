from flask import Flask, render_template_string

app = Flask(__name__)

ABOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 48px 24px;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            font-size: 2.5rem;
            color: #1a1a2e;
            margin-bottom: 8px;
        }
        .tagline {
            font-size: 1.1rem;
            color: #6c757d;
        }
        .card {
            background: #fff;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
            margin-bottom: 24px;
        }
        .card h2 {
            font-size: 1.3rem;
            color: #1a1a2e;
            margin-bottom: 12px;
        }
        .card p { color: #555; }
        ul { list-style: none; }
        ul li { padding: 6px 0; }
        ul li::before {
            content: "\\2022";
            color: #4f7cff;
            font-weight: bold;
            margin-right: 10px;
        }
        footer {
            text-align: center;
            margin-top: 48px;
            color: #999;
            font-size: 0.9rem;
        }
        a { color: #4f7cff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>About Us</h1>
            <p class="tagline">Learn more about who we are and what we do</p>
        </header>

        <div class="card">
            <h2>Our Story</h2>
            <p>
                We are a team of builders passionate about creating simple,
                useful software. This project started as an idea to make
                everyday tasks easier, and it has grown into what you see today.
            </p>
        </div>

        <div class="card">
            <h2>What We Do</h2>
            <ul>
                <li>Build reliable, user-friendly applications</li>
                <li>Focus on clean design and simple experiences</li>
                <li>Listen to feedback and keep improving</li>
            </ul>
        </div>

        <div class="card">
            <h2>Get In Touch</h2>
            <p>
                Have questions or feedback? We'd love to hear from you.
                Reach out any time.
            </p>
        </div>

        <footer>
            <p>&copy; 2025 Our Company. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
"""


@app.route("/about")
def about():
    return render_template_string(ABOUT_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)