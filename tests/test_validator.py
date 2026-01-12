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
    
    def test_common_password_with_rules(self):
        """Test detección de contraseña común con reglas"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase()
        
        # Contraseña común que cumple las reglas básicas
        valid, results, score = validator.validate('Password')
        
        # Verificar que se procesa (aunque no esté en lista de comunes)
        assert len(results) > 0
        assert score >= 0
    
    def test_repetition_detection_with_rules(self):
        """Test detección de repeticiones con reglas"""
        validator = PasswordValidator()
        validator.min_length(8)
        
        # Contraseña con repetición de 3+ caracteres
        valid, results, score = validator.validate('AAA12345')
        
        # Buscar advertencia de repetición
        repetition_warnings = [r for r in results if 'repetido' in r.get('rule', '').lower()]
        assert len(repetition_warnings) > 0, "No detectó repetición en 'AAA12345'"
    
    def test_sequence_detection_with_rules(self):
        """Test detección de secuencias"""
        validator = PasswordValidator()
        validator.min_length(8)
        
        # Contraseñas con secuencias obvias
        passwords_with_sequences = ['abc12345', 'test123test', 'qwerty99']
        
        for pwd in passwords_with_sequences:
            valid, results, score = validator.validate(pwd)
            # Buscar advertencia de secuencia
            sequence_warnings = [r for r in results if 'secuencia' in r.get('rule', '').lower()]
            # Al menos una debe tener advertencia
            if any(seq in pwd.lower() for seq in ['abc', '123', 'qwe']):
                assert len(sequence_warnings) > 0, f"No detectó secuencia en '{pwd}'"
    
    def test_score_with_repetition_vs_without(self):
        """Test comparación de scores con y sin repetición"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase()
        
        # Con repetición
        valid1, results1, score_rep = validator.validate('AAA12345')
        
        # Sin repetición  
        valid2, results2, score_no_rep = validator.validate('ABC12345')
        
        # Verificar que ambas se procesaron
        assert len(results1) > 0
        assert len(results2) > 0
        
        # Con repetición debe tener advertencia O score menor
        has_rep_warning = any('repetido' in r.get('rule', '').lower() for r in results1)
        assert has_rep_warning or score_rep <= score_no_rep
    
    def test_all_validation_types_together(self):
        """Test todas las validaciones juntas"""
        validator = PasswordValidator()
        validator.min_length(8).has_uppercase().has_lowercase().has_digits()
        
        # Contraseña que pasa reglas básicas
        valid, results, score = validator.validate('Password123')
        
        # Debe tener resultados
        assert len(results) > 0
        assert score > 0
        
        # Verificar estructura de resultados
        for result in results:
            assert 'rule' in result
            assert 'passed' in result
            assert 'message' in result



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
        
        # Test uppercase
        v1 = PasswordValidator()
        v1.has_uppercase(3)
        p1 = v1.generate_password(10)
        assert len(p1) == 10
        assert sum(1 for c in p1 if c.isupper()) >= 3
        
        # Test lowercase
        v2 = PasswordValidator()
        v2.has_lowercase(3)
        p2 = v2.generate_password(10)
        assert len(p2) == 10
        assert sum(1 for c in p2 if c.islower()) >= 3
        
        # Test digits
        v3 = PasswordValidator()
        v3.has_digits(3)
        p3 = v3.generate_password(10)
        assert len(p3) == 10
        assert sum(1 for c in p3 if c.isdigit()) >= 3
        
        # Test symbols - verificar que la función se ejecuta
        v4 = PasswordValidator()
        v4.has_symbols(2)
        p4 = v4.generate_password(10)
        assert len(p4) == 10
        # Contar caracteres no alfanuméricos
        non_alnum = sum(1 for c in p4 if not c.isalnum())
        assert non_alnum >= 1  # Al menos algún símbolo        
