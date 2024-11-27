from flask import Flask, request,  render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about-project.html')

@app.route('/zakat-emas', methods=['GET', 'POST'])
def zakat_emas():
    if request.method == 'POST':
        quantity_emas = float(request.form['quantity_emas'])
        nilai_zakat = 0.025 * quantity_emas
        nilai_zakat = int(nilai_zakat)
        nilai_zakat = f"{nilai_zakat:,}".replace(",", ".")
        return render_template('zakat_emas.html', nilai_zakat=nilai_zakat)
    return render_template('zakat_emas.html')

@app.route('/zakat-perdagangan', methods=['GET', 'POST'])
def zakat_perdagangan():
    if request.method == 'POST':
        try:
            modal = float(request.form['modal'])
            keuntungan = float(request.form['keuntungan'])
            piutang = float(request.form['piutang'])
            hutang = float(request.form['hutang'])
            kerugian = float(request.form['kerugian'])
            harga_emas_per_gram = float(request.form['harga_emas_per_gram'])

            nisab = 85 * harga_emas_per_gram
            nilai = (modal + keuntungan + piutang) - (kerugian + hutang)
            zakat = 0.025 * nilai if nilai >= nisab else 0

            return render_template('perdagangan.html', 
                                   modal=modal, keuntungan=keuntungan, 
                                   piutang=piutang, hutang=hutang, 
                                   kerugian=kerugian, nilai=nilai,
                                   harga_emas_per_gram=harga_emas_per_gram,
                                   nisab=nisab, zakat=zakat,
                                   keterangan="Wajib zakat" if zakat > 0 else "Tidak wajib zakat")
        except ValueError:
            return render_template('perdagangan.html', error="Input tidak valid.")
    return render_template('perdagangan.html')

@app.route('/zakat-pertanian', methods=['GET', 'POST'])
def zakat_pertanian():
    if request.method == 'POST':
        try:
            hasil_panen = float(request.form['hasil_panen'])
            sistem_pengairan = request.form['sistem_pengairan']

            if sistem_pengairan not in ['irigasi', 'alami']:
                return render_template('zakat_pertanian.html', error="Sistem pengairan harus 'irigasi' atau 'alami'.")

            nisab = 653  # dalam kg padi
            zakat_percentage = 0.05 if sistem_pengairan == 'irigasi' else 0.10
            zakat = hasil_panen * zakat_percentage if hasil_panen >= nisab else 0

            return render_template('zakat_pertanian.html',
                                   hasil_panen=hasil_panen,
                                   sistem_pengairan=sistem_pengairan,
                                   nisab=nisab, zakat=zakat,
                                   keterangan="Wajib zakat" if zakat > 0 else "Tidak wajib zakat")
        except ValueError:
            return render_template('zakat_pertanian.html', error="Input tidak valid.")
    return render_template('zakat_pertanian.html')

@app.route('/zakat-penghasilan', methods=['GET', 'POST'])
def zakat_penghasilan():
    if request.method == 'POST':
        try:
            hasil_penghasilan = float(request.form['hasil_penghasilan'])
            harga_emas_per_gram = float(request.form['harga_emas_per_gram'])

            nisab = 85 * harga_emas_per_gram
            zakat = 0.025 * hasil_penghasilan if hasil_penghasilan >= nisab else 0

            return render_template('zakat_penghasilan.html',
                                   hasil_penghasilan=hasil_penghasilan,
                                   harga_emas_per_gram=harga_emas_per_gram,
                                   nisab=nisab, zakat=zakat,
                                   keterangan="Wajib zakat" if zakat > 0 else "Tidak wajib zakat")
        except ValueError:
            return render_template('zakat_penghasilan.html', error="Input tidak valid.")
    return render_template('zakat_penghasilan.html')

if __name__ == '__main__':
    app.run(debug=True)