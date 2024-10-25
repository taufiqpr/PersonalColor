from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/produk')
def produk():
    return render_template('produk.html')

@app.route('/deteksi')
def deteksi():
    return render_template('deteksi.html')

if __name__ == '__main__':
    app.run(debug=True)