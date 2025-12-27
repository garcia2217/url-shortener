import string
from typing import Final

# Configuration constants
BASE62_ALPHABET: Final[str] = string.digits + string.ascii_lowercase + string.ascii_uppercase

class URLShortenerService:
    """
    Handles the conversion logic between database IDs and short codes.
    """

    @staticmethod
    def encode(identifier: int) -> str:
        """
        Converts a unique integer ID into a Base62 string.
        
        Args:
            identifier: The database primary key (bigint).
            
        Returns:
            A unique short code string.
        """
        if identifier == 0:
            return BASE62_ALPHABET[0]

        arr = []
        base = len(BASE62_ALPHABET)
        while identifier:
            identifier, rem = divmod(identifier, base)
            arr.append(BASE62_ALPHABET[rem])
        
        arr.reverse()
        return "".join(arr)

    @staticmethod
    def decode(short_code: str) -> int:
        """
        Converts a Base62 short code back into its integer ID.
        Useful if you want to query the DB by ID instead of an indexed string.
        """
        base = len(BASE62_ALPHABET)
        strlen = len(short_code)
        num = 0
        
        for i, char in enumerate(short_code):
            power = strlen - i - 1
            num += BASE62_ALPHABET.index(char) * (base ** power)
        return num

# Example Usage & Verification
if __name__ == "__main__":
    service = URLShortenerService()
    test_id = 1001
    encoded = service.encode(test_id)
    decoded = service.decode(encoded)
    
    print(f"ID: {test_id} -> Code: {encoded} -> Decoded: {decoded}")
    assert test_id == decoded, "Encoding/Decoding mismatch!"