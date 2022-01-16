import hashlib
import uuid

class StrUtil:
    """
    Utility class for string operations like string hashing, UUID generation and 
    all
    """

    @staticmethod
    def gen_hash(str):
        """
        Generates bare hash of a string using sha256
        """
        hash_object = hashlib.sha256(str)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    @staticmethod
    def uuid_hex():
        # using uuid 1 as it has 0 chance of collision 
        # because it uses date-time into generation
        return str(uuid.uuid1().hex)
    
    @staticmethod
    def uuid():
        return str(uuid.uuid4())

    @staticmethod
    def strip_key_headers(key_string: str) -> str:
        trimmed_head = key_string.replace('-----BEGIN PUBLIC KEY-----\n', '')
        trimmed_tail = trimmed_head.replace('\n-----END PUBLIC KEY-----', '')
        return trimmed_tail


    
