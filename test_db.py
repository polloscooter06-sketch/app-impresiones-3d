import os
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://pollo:Sebassmx12@localhost:5432/3dimpresiones"

print("DATABASE_URL:", DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Conexión exitosa a PostgreSQL")
except Exception as e:
    print("❌ Error de conexión:")
    print(e)
