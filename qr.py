from flask import Flask, jsonify, request
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route("/qr_code", methods=["GET"])
def qr_code():
    url = request.args.get("url")
    if url is None:
        return jsonify({"error": "No URL provided"}), 400
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    return buffer.getvalue(), 200, {"Content-Type": "image/png"}

if __name__ == "__main__":
    app.run(debug=True)
