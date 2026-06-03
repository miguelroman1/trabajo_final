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