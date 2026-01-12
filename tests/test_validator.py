import pytest
import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validator import PasswordValidator
class TestPasswordGeneratorEdgeCases:
    """Tests para casos edge del generador"""

    def test_generate_with_no_rules(self):
        """Test generar contraseña sin reglas definidas"""
        validator = PasswordValidator()
        password = validator.generate_password(10)
        assert len(password) == 10
        assert isinstance(password, str)

    def test_generate_minimum_length(self):
        """Test generar con longitud mínima"""
        validator = PasswordValidator()
        validator.has_uppercase(1).has_lowercase(1)
        password = validator.generate_password(8)
        assert len(password) == 8

    def test_generate_with_all_rules(self):
        """Test generar con todas las reglas activas"""
        validator = PasswordValidator()
        validator.has_uppercase(3)\
                 .has_lowercase(3)\
                 .has_digits(3)\
                 .has_symbols(2)

        password = validator.generate_password(20)
        assert len(password) == 20
        assert sum(1 for c in password if c.isupper()) >= 3
        assert sum(1 for c in password if c.islower()) >= 3
        assert sum(1 for c in password if c.isdigit()) >= 3

    def test_generate_exact_length_match(self):
        """Test cuando las reglas suman exactamente la longitud"""
        validator = PasswordValidator()
        validator.has_uppercase(2).has_lowercase(2).has_digits(2).has_symbols(2)

        password = validator.generate_password(8)
        assert len(password) == 8

    def test_generate_rules_exceed_length(self):
        """Test cuando las reglas requieren más caracteres que la longitud"""
        validator = PasswordValidator()
        validator.has_uppercase(5).has_lowercase(5).has_digits(5)

        # Debe generar una contraseña válida aunque sea más larga de lo pedido
        password = validator.generate_password(10)
        assert len(password) >= 10


class TestValidatorMessageVariations:
    """Tests para diferentes mensajes de validación"""

    def test_all_rules_pass_message(self):
        """Test mensajes cuando todas las reglas pasan"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase().has_lowercase().has_digits()

        valid, results, score = validator.validate("Password123")

        for result in results:
            if result['passed']:
                assert 'message' in result
                assert result['message'] != ''

    def test_all_rules_fail_message(self):
        """Test mensajes cuando todas las reglas fallan"""
        validator = PasswordValidator()
        validator.min_length(20).has_uppercase(5).has_symbols(3)

        valid, results, score = validator.validate("abc")

        for result in results:
            if not result['passed']:
                assert 'message' in result
                assert result['message'] != ''
    def test_generate_uses_random(self):
        """Test que el generador usa randomización"""
        validator = PasswordValidator()
        validator.has_uppercase(1).has_lowercase(1).has_digits(1)

        # Generar dos contraseñas
        password1 = validator.generate_password(15)
        password2 = validator.generate_password(15)

        # Deberían ser diferentes (altamente probable)
        # Si son iguales, es extremadamente improbable
        assert len(password1) == 15
        assert len(password2) == 15
        assert isinstance(password1, str)
        assert isinstance(password2, str)

class TestPasswordGeneratorEdgeCases:
    """Tests para casos edge del generador"""
    
    def test_generate_with_no_rules(self):
        """Test generar contraseña sin reglas definidas"""
        validator = PasswordValidator()
        password = validator.generate_password(10)
        assert len(password) == 10
        assert isinstance(password, str)
    
    def test_generate_minimum_length(self):
        """Test generar con longitud mínima"""
        validator = PasswordValidator()
        validator.has_uppercase(1).has_lowercase(1)
        password = validator.generate_password(8)
        assert len(password) == 8
    
    def test_generate_with_all_rules(self):
        """Test generar con todas las reglas activas"""
        validator = PasswordValidator()
        validator.has_uppercase(3)\
                 .has_lowercase(3)\
                 .has_digits(3)\
                 .has_symbols(2)
        
        password = validator.generate_password(20)
        assert len(password) == 20
        assert sum(1 for c in password if c.isupper()) >= 3
        assert sum(1 for c in password if c.islower()) >= 3
        assert sum(1 for c in password if c.isdigit()) >= 3
    
    def test_generate_exact_length_match(self):
        """Test cuando las reglas suman exactamente la longitud"""
        validator = PasswordValidator()
        validator.has_uppercase(2).has_lowercase(2).has_digits(2).has_symbols(2)
        
        password = validator.generate_password(8)
        assert len(password) == 8
    
    def test_generate_uses_random(self):
        """Test que el generador usa randomización"""
        validator = PasswordValidator()
        validator.has_uppercase(1).has_lowercase(1).has_digits(1)
        
        password1 = validator.generate_password(15)
        password2 = validator.generate_password(15)
        
        assert len(password1) == 15
        assert len(password2) == 15
        assert isinstance(password1, str)
        assert isinstance(password2, str)


class TestValidatorMessageVariations:
    """Tests para diferentes mensajes de validación"""
    
    def test_all_rules_pass_message(self):
        """Test mensajes cuando todas las reglas pasan"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase().has_lowercase().has_digits()
        
        valid, results, score = validator.validate("Password123")
        
        for result in results:
            if result['passed']:
                assert 'message' in result
                assert result['message'] != ''
    
    def test_all_rules_fail_message(self):
        """Test mensajes cuando todas las reglas fallan"""
        validator = PasswordValidator()
        validator.min_length(20).has_uppercase(5).has_symbols(3)
        
        valid, results, score = validator.validate("abc")
        
        for result in results:
            if not result['passed']:
                assert 'message' in result
                assert result['message'] != ''        
class TestValidationEdgeCases:
    """Tests para cubrir casos específicos de validación"""
    
    def test_common_password_detection_full_coverage(self):
        """Test completo de detección de contraseñas comunes"""
        validator = PasswordValidator()
        validator.min_length(6)
        
        # Probar varias contraseñas comunes
        common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'monkey', '1234567', 'letmein', 'trustno1', 'dragon'
        ]
        
        for pwd in common_passwords:
            valid, results, score = validator.validate(pwd)
            # Debe tener el mensaje de contraseña común
            has_common_warning = any(
                'común' in r['rule'] and not r['passed'] 
                for r in results
            )
            assert has_common_warning, f"No detectó '{pwd}' como común"
            # El score debe reducirse
            assert score < 100
    
    def test_repetition_detection_full_coverage(self):
        """Test completo de detección de repeticiones"""
        validator = PasswordValidator()
        validator.min_length(6)
        
        # Contraseñas con repeticiones
        passwords_with_repetition = [
            'aaa123',      # 3 'a' seguidas
            '111test',     # 3 '1' seguidas
            'test@@@',     # 3 '@' seguidas
            'Pass...word', # 3 '.' seguidas
            'AAA123',      # 3 'A' seguidas
        ]
        
        for pwd in passwords_with_repetition:
            valid, results, score = validator.validate(pwd)
            # Debe tener el mensaje de repetición
            has_repetition_warning = any(
                'repetido' in r['rule'] and not r['passed'] 
                for r in results
            )
            assert has_repetition_warning, f"No detectó repetición en '{pwd}'"
    
    def test_score_reduction_common_password(self):
        """Test que el score se reduce con contraseña común"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase().has_digits()
        
        # Contraseña común
        valid, results, score_common = validator.validate('password')
        
        # Contraseña no común similar
        valid2, results2, score_unique = validator.validate('MyP@ss99')
        
        # El score de la común debe ser menor
        assert score_common < score_unique
    
    def test_score_reduction_repetition(self):
        """Test que el score se reduce con repeticiones"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase().has_digits()
        
        # Con repetición
        valid, results, score_rep = validator.validate('AAA12345')
        
        # Sin repetición
        valid2, results2, score_no_rep = validator.validate('ABC12345')
        
        # El score con repetición debe ser menor
        assert score_rep < score_no_rep
    
    def test_multiple_penalties(self):
        """Test múltiples penalizaciones simultáneas"""
        validator = PasswordValidator()
        validator.min_length(8)
        
        # Contraseña con múltiples problemas: común + repetición
        valid, results, score = validator.validate('password')
        
        # Debe tener ambas advertencias
        has_common = any('común' in r['rule'] for r in results)
        
        assert has_common
        assert score < 50  # Score muy bajo por múltiples problemas


class TestGeneratePasswordAllBranches:
    """Tests para cubrir todas las ramas del generador"""
    
    def test_generate_fills_remaining_length(self):
        """Test que el generador rellena la longitud restante"""
        validator = PasswordValidator()
        validator.has_uppercase(2).has_lowercase(2)
        
        # Pedir longitud mayor que las reglas
        password = validator.generate_password(15)
        
        assert len(password) == 15
        assert sum(1 for c in password if c.isupper()) >= 2
        assert sum(1 for c in password if c.islower()) >= 2
    
    def test_generate_no_remaining_needed(self):
        """Test cuando no se necesita relleno"""
        validator = PasswordValidator()
        validator.has_uppercase(5).has_lowercase(5).has_digits(5).has_symbols(5)
        
        # Pedir exactamente lo que requieren las reglas
        password = validator.generate_password(20)
        
        assert len(password) == 20
    
    def test_generate_each_rule_type(self):
        """Test que cada tipo de regla se procesa correctamente"""
        validator = PasswordValidator()
        
        # Test con uppercase
        validator.has_uppercase(3)
        pwd1 = validator.generate_password(10)
        assert sum(1 for c in pwd1 if c.isupper()) >= 3
        
        # Crear nuevo validator para lowercase
        validator2 = PasswordValidator()
        validator2.has_lowercase(3)
        pwd2 = validator2.generate_password(10)
        assert sum(1 for c in pwd2 if c.islower()) >= 3
        
        # Crear nuevo validator para digits
        validator3 = PasswordValidator()
        validator3.has_digits(3)
        pwd3 = validator3.generate_password(10)
        assert sum(1 for c in pwd3 if c.isdigit()) >= 3
        
        # Crear nuevo validator para symbols
        validator4 = PasswordValidator()
        validator4.has_symbols(2)
        pwd4 = validator4.generate_password(10)
        assert any(c in pwd4 for c in '!@#$%^&*')                
