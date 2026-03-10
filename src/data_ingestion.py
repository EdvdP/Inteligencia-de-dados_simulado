# TODO: No ambiente de produção, substituir generate_mock_data 
# por uma conexão via SQLAlchemy com BigQuery ou Snowflake.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_data(n_rows=1000):
    if not os.path.exists('data'): os.makedirs('data')
    np.random.seed(42)
    dates = [datetime(2024, 1, 1) + timedelta(days=i%365) for i in range(n_rows)]
    products = ['Notebook', 'Monitor', 'Teclado', 'Mouse']
    data = {
        'data_venda': dates,
        'produto': np.random.choice(products, n_rows),
        'quantidade': np.random.randint(1, 10, n_rows),
        'preco_unitario': np.random.uniform(100, 3000, n_rows)
    }
    df = pd.DataFrame(data)
    df['faturamento'] = df['quantidade'] * df['preco_unitario']
    df.to_csv('data/vendas_brutas.csv', index=False)
    print("✅ Arquivo data/vendas_brutas.csv gerado com sucesso!")

if __name__ == "__main__":
    generate_mock_data()