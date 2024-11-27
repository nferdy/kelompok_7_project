from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/zakat-emas', methods=['POST'])
def zakat_emas():
    try:
        data = request.get_json()
        total_nilai_emas = float(data['total_nilai_emas'])  
        harga_emas_per_gram = float(data['harga_emas_per_gram'])  

        nisab = 85 * harga_emas_per_gram

        if total_nilai_emas >= nisab:
            zakat = 0.025 * total_nilai_emas  
        else:
            zakat = 0  

       
        return jsonify({
            "total_nilai_emas": total_nilai_emas,
            "harga_emas_per_gram": harga_emas_per_gram,
            "nisab": nisab,
            "zakat": zakat,
            "keterangan": "Wajib zakat" if zakat > 0 else "Tidak wajib zakat"
        })

    except (ValueError, KeyError):
        return jsonify({"error": "Input tidak valid. Pastikan mengirim 'total_nilai_emas' dan 'harga_emas_per_gram'."}), 400

@app.route('/zakat-perdagangan', methods=['POST'])
def zakat_perdagangan():
    try:
        # comment: 
        data = request.get_json()
        modal = float(data['modal'])  
        keuntungan = float(data['keuntungan']) 
        piutang = float(data['piutang'])
        hutang= float(data['hutang'])
        kerugian = float(data['kerugian'])
        harga_emas_per_gram = float(data['harga_emas_per_gram'])  

        nisab = 85 * harga_emas_per_gram
        nilai = (modal + keuntungan + piutang) - (kerugian + hutang)

        if nilai >= nisab:
            zakat = 0.025 * nilai  
        else:
            zakat = 0 

        return jsonify({
            "total harta": nilai,
            "harga_emas_per_gram": harga_emas_per_gram,
            "nisab": nisab,
            "zakat": zakat,
            "keterangan": "Wajib zakat" if zakat > 0 else "Tidak wajib zakat"
        })
    except (ValueError, KeyError):
        return jsonify({"error": "Input tidak valid. Pastikan mengirim 'total_nilai_emas' dan 'harga_emas_per_gram'."}), 400
    # end try

@app.route('/zakat-pertanian', methods=['POST'])
def zakat_pertanian():
    try:
        data = request.get_json()
        hasil_panen = float(data['hasil_panen'])  
        sistem_pengairan = data['sistem_pengairan']

        if sistem_pengairan not in ['irigasi', 'alami']:
            return jsonify({"error": "Sistem_pengairan harus 'irigasi' atau 'alami'"}), 400
        
        nisab = 653 #dalam kg padi
        zakat_percentage = 0.05 if sistem_pengairan == 'irigasi' else 0.10

        if hasil_panen >= nisab:
            zakat = hasil_panen * zakat_percentage  
        else:
            zakat = 0  

       
        return jsonify({
            "hasil_panen": hasil_panen,
            "sistem_pengairan": sistem_pengairan,
            "nisab": nisab,
            "zakat": zakat,
            "keterangan": "Wajib zakat" if zakat > 0 else "Tidak wajib zakat"
        })

    except (ValueError, KeyError):
        return jsonify({"error": "Input tidak valid. Pastikan mengirim 'hasil_panen' dan 'sistem_pengairan'."}), 400

@app.route('/zakat-penghasilan', methods=['POST'])
def zakat_penghasilan():
    try:
        data = request.get_json()
        hasil_penghasilan = float(data['hasil_penghasilan'])  
        harga_emas_per_gram = float(data['harga_emas_per_gram'])

        nisab = 85 * harga_emas_per_gram

        if hasil_penghasilan >= nisab:
            zakat = 0.025 * hasil_penghasilan  
        else:
            zakat = 0  

        return jsonify({
            "hasil_penghasilan": hasil_penghasilan,
            "harga_emas_per_gram": harga_emas_per_gram,
            "nisab": nisab,
            "zakat": zakat,
            "keterangan": "Wajib zakat" if zakat > 0 else "Tidak wajib zakat"
        })

    except (ValueError, KeyError):
        return jsonify({"error": "Input tidak valid. Pastikan mengirim 'hasil_penghasilan' dan 'harga_emas_per_gram'."}), 400


if __name__ == '__main__':
    app.run(debug=True)
