import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: The plain text password to hash.

    Returns: 
        str: The hashed password.
    """

    hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10))

    return hash_password.decode("utf-8")



def verify_password(stored_password: str, input_password: str) -> bool:
    """
    Verify if the provided password matches the stored hashed password.
    
    Args:
        stored_password: The hashed password from the database.
        input_password: The password provided by the user to check.
        
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_password.encode("utf-8"))