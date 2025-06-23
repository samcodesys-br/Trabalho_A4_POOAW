from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from controller.FieldController import FieldController
from flask_caching import Cache
from model.MineField import MineField
from model.Cell import Cell
import uuid

app = Flask(__name__)
app.secret_key = 'key'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Game(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fakeBombsFound=db.Column(db.Integer, nullable=False, default=0) 
    timeInSeconds=db.Column(db.Integer, nullable=False)

cont = FieldController()

def get_or_create_session_id():

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def serialize_field(field):
    # Converter classe MineField em dict do campo
    matrix_data = []
    for row in field.matrix:
        row_data = []
        for cell in row:
            cell_data = {
                'valor': cell.valor,
                'isRevealed': cell.isRevealed,
                'coord': cell.coord,
                'isMine': cell.isMine,
                'isFake': cell.isFake,
                'flagged': cell.flagged,
                'is_fake_bomb_neighbor': getattr(cell, 'is_fake_bomb_neighbor')
            }
            row_data.append(cell_data)
        matrix_data.append(row_data)
    
    return {
        'matrix': matrix_data,
        'row': field.row,
        'col': field.col,
        'flags': field.flags,
        'score': field.score,
        'time': field.time,
        'mines': field.mines
    }

def deserialize_field(field_data):
    # Converter dict do campo em classe MineField
    matrix = []
    for row_data in field_data['matrix']:
        row = []
        for cell_data in row_data:
            cell = Cell(
                valor=cell_data['valor'],
                isRevealed=cell_data['isRevealed'],
                coord=cell_data['coord'],
                isMine=cell_data['isMine'],
                isFake=cell_data['isFake'],
                flagged=cell_data['flagged']
            )

            if 'is_fake_bomb_neighbor' in cell_data:
                cell.is_fake_bomb_neighbor = cell_data['is_fake_bomb_neighbor']
            row.append(cell)
        matrix.append(row)
    
    return MineField(
        matrix=matrix,
        row=field_data['row'],
        col=field_data['col'],
        flags=field_data['flags'],
        score=field_data['score'],
        time=field_data['time'],
        mines=field_data['mines']
    )

def get_cached_game_state(session_id):
    cached_data = cache.get(f'game_state_{session_id}')
    if cached_data:
        return deserialize_field(cached_data)
    return None

def save_game_state_to_cache(session_id, game_state):
    serialized_data = serialize_field(game_state)
    cache.set(f'game_state_{session_id}', serialized_data, timeout=3600)  # Duração de 1 hora

@app.route("/")
def index():
    session_id = get_or_create_session_id()
    
    # Recupera jogo existente em cache
    field = get_cached_game_state(session_id)
    
    if not field:
        # Cria novo jogo se não existir
        field = cont.initGame()
        save_game_state_to_cache(session_id, field)
    
    return render_template('index.html', field=field, session_id=session_id)

@app.route("/restart", methods=["POST"])
def restart():
    session_id = get_or_create_session_id()
    
    # Limpar estado do cache
    cache.delete(f'game_state_{session_id}')
    
    # Criar novo jogo
    field = cont.initGame()
    save_game_state_to_cache(session_id, field)
    
    return jsonify({
        'success': True,
        'field': serialize_field(field)
    })

@app.route("/score")
def score():
    # Buscar dados do banco
    total_fake_bombs = db.session.query(db.func.sum(Game.fakeBombsFound)).scalar() or 0
    total_time = db.session.query(db.func.sum(Game.timeInSeconds)).scalar() or 0

    games = Game.query.order_by(
        Game.timeInSeconds.asc(),  # Ordem crescente por tempo
        Game.fakeBombsFound.desc()  # Ordem decrescente por bombas falsas
    ).limit(10).all()
    
    return render_template('score.html', 
                         total_fake_bombs=total_fake_bombs,
                         total_time=total_time,
                         games=games)

@app.route("/reveal", methods=["POST"])
def reveal():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    session_id = get_or_create_session_id()
    field = get_cached_game_state(session_id)
    
    if not field:
        return jsonify({'error': 'No game state found'}), 400
    
    result = cont.reveal_cell(field, row, col)
    
    # Atualiza o estado do cache
    save_game_state_to_cache(session_id, field)
    
    # Adiciona pontuação quando existir
    if hasattr(field, 'score'):
        result['score'] = field.score
    
    
    return jsonify(result)

@app.route("/flag", methods=["POST"])
def flag():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    session_id = get_or_create_session_id()
    field = get_cached_game_state(session_id)
    
    if not field:
        return jsonify({'error': 'No game state found'}), 400
    
    result = cont.toggle_flag(field, row, col)
    
    # Atualiza o estado do cache
    save_game_state_to_cache(session_id, field)
    
    return jsonify(result)

@app.route("/end_game", methods=["POST"])
def end_game():

    data = request.get_json()
    fake_bombs_found = data.get('fakeBombsFound', 0)
    time_in_seconds = data.get('timeInSeconds', 0)
    
    # Cria novo registro
    game = Game(
        fakeBombsFound=fake_bombs_found,
        timeInSeconds=time_in_seconds
    )
    
    db.session.add(game)
    db.session.commit()
    
    return jsonify({'success': True, 'game_id': game.id})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
