import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    path = Path('frontend/services/supabase_client.py').resolve().parents[2] / 'backend' / '.env'
    print('Trying path:', path)
    print('Exists:', path.exists())
    loaded = load_dotenv(path)
    print('Loaded:', loaded)
except ImportError:
    print('ImportError: python-dotenv not installed')

print('SUPABASE_URL:', bool(os.getenv('SUPABASE_URL')))
