import re
import string
from typing import List, Dict, Tuple

class PasswordValidator:
    def __init__(self):
        self.rules = []
        self.common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
            'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
            'bailey', 'passw0rd', 'shadow', '123123', '654321'
        ]
    
    def min_length(self, length: int):
        self.rules.append(('min_length', length))
        return self
    
    def max_length(self, length: int):
        self.rules.append(('max_length', length))
        return self
    
    def has_uppercase(self, count: int = 1):
        self.rules.append(('uppercase', count))
        return self
    
    def has_lowercase(self, count: int = 1):
        self.rules.append(('lowercase', count))
        return self
    
    def has_digits(self, count: int = 1):
        self.rules.append(('digits', count))
        return self
    
    def has_symbols(self, count: int = 1):
        self.rules.append(('symbols', count))
        return self
    
    def no_spaces(self):
        self.rules.append(('no_spaces', None))
        return self
    
    def validate(self, password: str) -> Tuple[bool, List[Dict], int]:
        results = []
        score = 0
        max_score = len(self.rules) * 10
        
        for rule, value in self.rules:
            if rule == 'min_length':
                passed = len(password) >= value
                results.append({
                    'rule': f'Mínimo {value} caracteres',
                    'passed': passed,
                    'message': f'Longitud actual: {len(password)}'
                })
                if passed:
                    score += 10
            
            elif rule == 'max_length':
                passed = len(password) <= value
                results.append({
                    'rule': f'Máximo {value} caracteres',
                    'passed': passed,
                    'message': f'Longitud actual: {len(password)}'
                })
                if passed:
                    score += 10
            
            elif rule == 'uppercase':
                count = sum(1 for c in password if c.isupper())
                passed = count >= value
                results.append({
                    'rule': f'Al menos {value} mayúscula(s)',
                    'passed': passed,
                    'message': f'Encontradas: {count}'
                })
                if passed:
                    score += 10
            
            elif rule == 'lowercase':
                count = sum(1 for c in password if c.islower())
                passed = count >= value
                results.append({
                    'rule': f'Al menos {value} minúscula(s)',
                    'passed': passed,
                    'message': f'Encontradas: {count}'
                })
                if passed:
                    score += 10
            
            elif rule == 'digits':
                count = sum(1 for c in password if c.isdigit())
                passed = count >= value
                results.append({
                    'rule': f'Al menos {value} número(s)',
                    'passed': passed,
                    'message': f'Encontrados: {count}'
                })
                if passed:
                    score += 10
            
            elif rule == 'symbols':
                count = sum(1 for c in password if c in string.punctuation)
                passed = count >= value
                results.append({
                    'rule': f'Al menos {value} símbolo(s)',
                    'passed': passed,
                    'message': f'Encontrados: {count}'
                })
                if passed:
                    score += 10
            
            elif rule == 'no_spaces':
                passed = ' ' not in password
                results.append({
                    'rule': 'Sin espacios',
                    'passed': passed,
                    'message': 'Espacios encontrados' if not passed else 'OK'
                })
                if passed:
                    score += 10
        
        # Validaciones adicionales
        if password.lower() in self.common_passwords:
            results.append({
                'rule': 'No usar contraseñas comunes',
                'passed': False,
                'message': 'Esta es una contraseña muy común'
            })
            score = max(0, score - 20)
        
        # Detectar secuencias
        sequences = ['abc', '123', 'qwe', 'asd', 'zxc']
        has_sequence = any(seq in password.lower() for seq in sequences)
        if has_sequence:
            results.append({
                'rule': 'Sin secuencias obvias',
                'passed': False,
                'message': 'Contiene secuencias como abc, 123, etc.'
            })
            score = max(0, score - 10)
        
        # Detectar repeticiones
        has_repetition = bool(re.search(r'(.)\1{2,}', password))
        if has_repetition:
            results.append({
                'rule': 'Sin caracteres repetidos',
                'passed': False,
                'message': 'Contiene 3+ caracteres repetidos'
            })
            score = max(0, score - 10)
        
        all_passed = all(r['passed'] for r in results)
        score_percentage = int((score / max(max_score, 1)) * 100) if max_score > 0 else 0
        
        return all_passed, results, score_percentage
    
    def generate_password(self, length: int = 12) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        import random   #pragma: no cover
        
        password = []
        
        # Asegurar que cumple las reglas
        for rule, value in self.rules:
            if rule == 'uppercase':
                password.extend(random.choices(string.ascii_uppercase, k=value))
            elif rule == 'lowercase':
                password.extend(random.choices(string.ascii_lowercase, k=value))
            elif rule == 'digits':
                password.extend(random.choices(string.digits, k=value))
            elif rule == 'symbols':
                password.extend(random.choices(string.punctuation, k=value))
        
        # Completar hasta la longitud deseada
        remaining = length - len(password)
        if remaining > 0:
            password.extend(random.choices(chars, k=remaining))
        
        # Mezclar
        random.shuffle(password)
        return ''.join(password)
