import polars as pl
import os

def process_with_polars():
    # Caminho do arquivo
    path = 'data/vendas_brutas.csv'
    if not os.path.exists(path):
        print("❌ Erro: Execute data_ingestion.py primeiro!")
        return

    # Lazy evaluation: Carrega e define o pipeline
    df = (
        pl.scan_csv(path)
        .with_columns(pl.col("data_venda").str.to_date()) # Converte para data
        .sort("data_venda") # Ordena para que o LAG e Média Móvel façam sentido
        .with_columns([
            pl.col("quantidade").shift(1).over("produto").alias("venda_lag_1d"),
            pl.col("quantidade").rolling_mean(window_size=7).over("produto").alias("media_movel_7d")
        ])
    )
    
    # Agregação final para o print
    result = (
        df.group_by("produto")
        .agg([
            pl.col("quantidade").sum().alias("total_unidades"),
            pl.col("faturamento").sum().alias("receita_total")
        ])
        .sort("receita_total", descending=True)
        .collect() # Só aqui o processamento acontece de fato
    )
    
    print("📊 Pipeline Polars (Engenharia de Features) concluído:")
    print(result.head())
    return result

if __name__ == "__main__":
    process_with_polars()