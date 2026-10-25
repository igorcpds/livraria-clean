from flask import Flask, render_template, request, redirect, url_for, flash
from frameworks_drivers.txt_repository import TxtFileRepository
from use_cases.interactors import LivrariaUseCaseInteractor
from interface_adapters.controllers import LivrariaAdapterController

app = Flask(__name__, template_folder='frameworks_drivers/templates')
app.secret_key = "chave_secreta_clean_architecture"

# =====================================================================
# APLICAÇÃO DO DIP (Dependency Inversion Principle):
# O UseCaseInteractor depende apenas da abstração PersistenciaLivrariaPort.
# Aqui injetamos o driver concreto TxtFileRepository("bd_livraria.txt").
# =====================================================================
driver_persistencia_txt = TxtFileRepository("bd_livraria.txt")
use_case_interactor = LivrariaUseCaseInteractor(persistencia_port=driver_persistencia_txt)
controller = LivrariaAdapterController(interactor=use_case_interactor)


@app.route('/', methods=['GET'])
def index():
    termo = request.args.get('q', '')
    view_model = controller.construir_view_model(termo)
    return render_template('index.html', vm=view_model)


@app.route('/adicionar/<int:livro_id>', methods=['POST'])
def adicionar(livro_id):
    livro = controller.adicionar_livro(livro_id)
    if livro:
        flash(f'"{livro.titulo}" adicionado ao carrinho!', 'sucesso')
    return redirect(url_for('index'))


@app.route('/scan', methods=['POST'])
def scan():
    isbn = request.form.get('isbn', '')
    livro = controller.escanear_codigo(isbn)
    if livro:
        flash(f'Scan & Go: "{livro.titulo}" adicionado ao carrinho!', 'sucesso')
    else:
        flash(f'ISBN "{isbn}" não encontrado.', 'erro')
    return redirect(url_for('index'))


@app.route('/remover/<int:indice>', methods=['POST'])
def remover(indice):
    controller.remover_item(indice)
    return redirect(url_for('index'))


@app.route('/avaliar', methods=['POST'])
def avaliar():
    try:
        av = controller.submeter_avaliacao(
            livro_id=request.form.get('livro_id', '1'),
            utilizador=request.form.get('utilizador', ''),
            nota=request.form.get('nota', '5'),
            comentario=request.form.get('comentario', '')
        )
        flash(f'Avaliação para "{av.titulo_livro}" gravada em bd_livraria.txt!', 'sucesso')
    except ValueError as erro:
        flash(str(erro), 'erro')
    return redirect(url_for('index'))


@app.route('/checkout', methods=['POST'])
def checkout():
    cpf = request.form.get('cpf', '')
    recibo = controller.concluir_pagamento(cpf)
    if recibo:
        flash('Compra finalizada e persistida em bd_livraria.txt!', 'sucesso')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
