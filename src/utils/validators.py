import hashlib
import re

class Validators:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return Validators.hash_password(password) == hashed
    
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_curp(curp: str) -> bool:
        pattern = r'^[A-Z]{4}\d{6}[A-Z]{6}\d{2}$'
        return re.match(pattern, curp) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Valida número de teléfono internacional.
        Acepta formatos:
        - 6861234567 (10 dígitos)
        - 5216861234567 (13 dígitos con código país)
        - +5216861234567 (13 dígitos con +)
        - +1 6861234567 (con espacio)
        - 52-686-123-4567 (con guiones)
        """
        # Eliminar espacios y guiones
        phone_clean = re.sub(r'[\s\-]', '', phone)
        # Validar: puede empezar con + opcional, luego números (10-15 dígitos total)
        pattern = r'^\+?\d{10,15}$'
        return re.match(pattern, phone_clean) is not None