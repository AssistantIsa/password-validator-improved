from flask import Flask, render_template, request, jsonify
from validator import PasswordValidator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    password = data.get('password', '')
    
    # Crear esquema de validación
    validator = PasswordValidator()
    validator.min_length(8)\
             .max_length(50)\
             .has_uppercase(1)\
             .has_lowercase(1)\
             .has_digits(1)\
             .has_symbols(1)\
             .no_spaces()
    
    is_valid, results, score = validator.validate(password)
    
    return jsonify({
        'valid': is_valid,
        'results': results,
        'score': score,
        'strength': get_strength_label(score)
    })

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    length = data.get('length', 12)
    
    validator = PasswordValidator()
    validator.min_length(8)\
             .has_uppercase(2)\
             .has_lowercase(2)\
             .has_digits(2)\
             .has_symbols(1)
    
    password = validator.generate_password(length)
    
    return jsonify({
        'password': password
    })

def get_strength_label(score):
    if score < 40:
        return 'Muy Débil'
    elif score < 60:
        return 'Débil'
    elif score < 80:
        return 'Media'
    elif score < 95:
        return 'Fuerte'
    else:
        return 'Muy Fuerte'

if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True, host='0.0.0.0', port=5000)
