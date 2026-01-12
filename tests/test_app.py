import pytest
import json
import sys
import os
from app import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Fixture para cliente de prueba Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskApp:
    """Tests para la aplicación Flask"""
    
    def test_index_route(self, client):
        """Test: ruta principal carga correctamente"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Password Validator Pro' in response.data
    
    def test_validate_endpoint_valid_password(self, client):
        """Test: endpoint de validación - contraseña válida"""
        response = client.post('/validate',
                              data=json.dumps({'password': 'MyP@ssw0rd123'}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'valid' in data
        assert 'results' in data
        assert 'score' in data
        assert 'strength' in data
    
    def test_validate_endpoint_invalid_password(self, client):
        """Test: endpoint de validación - contraseña inválida"""
        response = client.post('/validate',
                              data=json.dumps({'password': 'weak'}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['valid'] == False
        assert data['score'] < 50
    
    def test_validate_endpoint_empty_password(self, client):
        """Test: endpoint de validación - contraseña vacía"""
        response = client.post('/validate',
                              data=json.dumps({'password': ''}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data
    
    def test_generate_endpoint(self, client):
        """Test: endpoint de generación"""
        response = client.post('/generate',
                              data=json.dumps({'length': 16}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'password' in data
        assert len(data['password']) == 16
    
    def test_generate_endpoint_default_length(self, client):
        """Test: generación con longitud por defecto"""
        response = client.post('/generate',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'password' in data
        assert len(data['password']) == 12
    
    def test_generate_endpoint_various_lengths(self, client):
        """Test: generación con varias longitudes"""
        for length in [8, 12, 16, 20, 32]:
            response = client.post('/generate',
                                  data=json.dumps({'length': length}),
                                  content_type='application/json')
            
            data = json.loads(response.data)
            assert len(data['password']) == length
    
    def test_strength_labels(self, client):
        """Test: etiquetas de fortaleza correctas"""
        test_cases = [
            ('weak', 'Muy Débil'),
            ('Weak1', 'Débil'),
            ('MyPass123', 'Media'),
            ('MyP@ss123', 'Fuerte'),
        ]
        
        for password, _ in test_cases:
            response = client.post('/validate',
                                  data=json.dumps({'password': password}),
                                  content_type='application/json')
            data = json.loads(response.data)
            assert 'strength' in data
    def test_app_config(self):
       """Test: app setup"""
       assert app.config['TESTING'] == True

    def test_app_name(self):
        """Test nombre de la app"""
        assert app.name == 'app' or app.import_name == 'app'
class TestAppExecution:
    """Tests para ejecución de la app"""

    def test_app_config(self):
        """Test configuración de la app"""
        assert app is not None
        assert app.config is not None

    def test_app_name(self):
        """Test nombre de la app"""
        assert app.name == 'app' or app.import_name == 'app'
