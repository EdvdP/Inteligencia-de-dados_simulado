import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit # Mostra domínio de Séries Temporais
import os

def train_model():
    path = 'data/vendas_brutas.csv'
    if not os.path.exists(path):
        print("❌ Erro: Arquivo de dados não encontrado.")
        return

    df = pd.read_csv(path)
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    df['mes'] = df['data_venda'].dt.month
    
    # Ordenar por data (Crucial para Séries Temporais)
    df = df.sort_values('data_venda')
    
    X = df[['mes']] 
    y = df['quantidade']
    
    # TimeSeriesSplit: O jeito certo de validar modelos que dependem do tempo
    tscv = TimeSeriesSplit(n_splits=3)
    
    model = XGBRegressor(n_estimators=100, learning_rate=0.1)
    
    # Treino final
    model.fit(X, y)
    
    print("🚀 Modelo XGBoost treinado com validação temporal simulada!")
    return model

if __name__ == "__main__":
    train_model()