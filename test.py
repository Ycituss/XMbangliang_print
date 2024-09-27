from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_ip = request.remote_addr
    return render_template('test.html', ip_address=user_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)