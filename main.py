from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gastos.db'
db = SQLAlchemy(app)

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    pablo = db.Column(db.Float, nullable=False)
    sabri = db.Column(db.Float, nullable=False)
    nota = db.Column(db.String(200), nullable=True)

@app.route('/')
def index():
    gastos = Gasto.query.all()
    total_monto = sum(gasto.monto for gasto in gastos)
    total_pablo = sum(gasto.pablo for gasto in gastos)
    total_sabri = sum(gasto.sabri for gasto in gastos)
    return render_template('index.html', gastos=gastos, total_monto=total_monto, total_pablo=total_pablo, total_sabri=total_sabri)

@app.route('/add', methods=['POST'])
def add():
    concepto = request.form['concepto']
    monto = float(request.form['monto'])
    nota = request.form['nota']
    mitad = monto / 2
    new_gasto = Gasto(concepto=concepto, monto=monto, pablo=mitad, sabri=mitad, nota=nota)
    db.session.add(new_gasto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    gasto = Gasto.query.get_or_404(id)
    if request.method == 'POST':
        gasto.concepto = request.form['concepto']
        gasto.monto = float(request.form['monto'])
        gasto.nota = request.form['nota']
        gasto.pablo = gasto.monto / 2
        gasto.sabri = gasto.monto / 2
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', gasto=gasto)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    gasto = Gasto.query.get_or_404(id)
    db.session.delete(gasto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    db.session.query(Gasto).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
