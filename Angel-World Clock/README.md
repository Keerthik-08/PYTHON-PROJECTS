from flask import Flask, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>World Clock</title>

    <style>
        body{
            background:black;
            color:white;
            font-family:Arial;
            text-align:center;
            padding-top:50px;
        }

        h1{
            color:cyan;
        }

        .clock-box{
            background:#222;
            width:300px;
            margin:auto;
            padding:20px;
            border-radius:15px;
            box-shadow:0px 0px 10px cyan;
        }

        select{
            padding:10px;
            font-size:16px;
            border-radius:10px;
        }

        .time{
            margin-top:20px;
            font-size:35px;
            color:yellow;
        }
    </style>
</head>

<body>

    <h1>🌍 World Clock</h1>

    <div class="clock-box">

        <form method="GET">

            <select name="zone" onchange="this.form.submit()">

                {% for z in zones %}

                <option value="{{z}}" {% if z == current_zone %}selected{% endif %}>
                    {{z}}
                </option>

                {% endfor %}

            </select>

        </form>

        <div class="time">
            {{time}}
        </div>

    </div>

</body>
</html>
"""

@app.route("/")
def home():

    from flask import request

    zones = [
        "Asia/Kolkata",
        "Europe/London",
        "America/New_York",
        "Asia/Tokyo",
        "Australia/Sydney"
    ]

    current_zone = request.args.get("zone", "Asia/Kolkata")

    tz = pytz.timezone(current_zone)

    current_time = datetime.now(tz).strftime("%H:%M:%S")

    return render_template_string(
        HTML,
        time=current_time,
        zones=zones,
        current_zone=current_zone
    )

if __name__ == "__main__":
    app.run(debug=True)
