import pandas as pd

def finde_gueltige_datumsbereiche(start_jahr, end_jahr, history):
    start_date = None
    end_date = None

    # Suche nach gültigem start_date
    for i in range(10):
        potential_start_date = (pd.Timestamp(f"{start_jahr}-01-02") + pd.Timedelta(days=i)).strftime('%Y-%m-%d')
        if not pd.isna(history['Close'].get(potential_start_date)):
            start_date = potential_start_date
            break

    # Suche nach gültigem end_date
    for i in range(10):
        potential_end_date = (pd.Timestamp(f"{end_jahr}-12-31") - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
        if not pd.isna(history['Close'].get(potential_end_date)):
            end_date = potential_end_date
            break

    return start_date, end_date
