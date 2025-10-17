import hashlib
import secrets
import os
import pandas as pd

def get_or_create_salt(salt_file='nhs_pseudonymization_salt.key'):
    """Get existing salt or create new one if it doesn't exist."""
    if not os.path.exists(salt_file):
        salt = secrets.token_bytes(32)
        with open(salt_file, 'wb') as f:
            f.write(salt)
        print(f"Created salt file: {salt_file}")
        print("IMPORTANT: Back up this file and keep it secure!")
        return salt
    else:
        with open(salt_file, 'rb') as f:
            return f.read()

def pseudonymize_nhs_series(nhs_series):
    """
    Pseudonymize a pandas Series of NHS numbers.
    
    Args:
        nhs_series: pandas Series containing NHS numbers
    
    Returns:
        pandas Series of pseudonymized IDs
    """
    salt = get_or_create_salt()
    
    # List comprehension for better performance
    hashed_values = [
        hashlib.sha256(str(nhs).encode('utf-8') + salt).hexdigest() 
        if pd.notna(nhs) else None 
        for nhs in nhs_series
    ]
    
    return pd.Series(hashed_values, index=nhs_series.index)

# Example usage:
# df['pseudonymized_nhs'] = pseudonymize_nhs_series(df['nhs_number'])
