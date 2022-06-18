import pandas as pd

from .utils import load_dataframe, save_dataframe


def load_rainfall_data(dag_run=None, **kwargs):
    df = pd.read_csv(dag_run.conf.get("rainfall_data_path"))
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["mes"] = df["date"].apply(lambda x: x.month)
    df["ano"] = df["date"].apply(lambda x: x.year)
    df = df.sort_values(by="date", ascending=True).reset_index(drop=True)
    df = df.dropna()
    df = df.drop_duplicates()
    df.name = "rainfall_data"
    save_dataframe(df, dst=dag_run.conf.get("tmp_path"))


def load_macroeconomic_data(dag_run=None, **kwargs):
    df = pd.read_csv(dag_run.conf.get("macroeconomic_data_path"))
    df["Periodo"] = df["Periodo"].apply(lambda x: x[0:10])
    df["Periodo"] = pd.to_datetime(df["Periodo"], format="%Y-%m-%d", errors="coerce")
    df = df.drop_duplicates(subset="Periodo")
    df = df[~df["Periodo"].isna()]

    # df_pib
    def convert_int(x):
        return int(x.replace(".", ""))

    cols_pib = [col for col in df.columns if "PIB" in col]
    df_pib = df[cols_pib + ["Periodo"]].copy()
    df_pib = df_pib.dropna(how="any", axis=0)
    df_pib[cols_pib] = df_pib[cols_pib].applymap(convert_int)
    df_pib = df_pib.sort_values(by="Periodo", ascending=True)

    # df_imacec
    def to_100(x):
        x = x.split(".")
        if x[0].startswith("1"):
            if len(x[0]) >2:
                return float(x[0] + "." + x[1])
            else:
                x = x[0]+x[1]
                return float(x[0:3] + "." + x[3:])
        else:
            if len(x[0])>2:
                return float(x[0][0:2] + "." + x[0][-1])
            else:
                x = x[0] + x[1]
                return float(x[0:2] + "." + x[2:])

    cols_imacec = [col for col in df.columns if "Imacec" in col]
    df_imacec = df[cols_imacec + ["Periodo"]].copy()
    df_imacec = df_imacec.dropna(how="any", axis=0)
    df_imacec[cols_imacec] = df_imacec[cols_imacec].applymap(to_100)
    assert (df_imacec[cols_imacec].max() > 100).all()
    assert (df_imacec[cols_imacec].min() > 30).all()
    df_imacec = df_imacec.sort_values(by="Periodo", ascending=True)

    # df_iv
    df_iv = df[["Indice_de_ventas_comercio_real_no_durables_IVCM", "Periodo"]].copy()
    df_iv = df_iv.dropna()
    df_iv["num"] = df_iv["Indice_de_ventas_comercio_real_no_durables_IVCM"].apply(to_100)
    df_iv = df_iv.sort_values(by="Periodo", ascending=True)

    # df_num
    df_num = pd.merge(df_pib, df_imacec, on="Periodo", how="inner")
    df_num = pd.merge(df_num, df_iv, on="Periodo", how="inner")
    df_num["mes"] = df_num["Periodo"].apply(lambda x: x.month)
    df_num["ano"] = df_num["Periodo"].apply(lambda x: x.year)

    df_num.name = "macroeconomic_data"
    save_dataframe(df_num, dst=dag_run.conf.get("tmp_path"))


def load_milk_price_data(dag_run=None, **kwargs):
    df = pd.read_csv(dag_run.conf.get("milk_price_data_path"))
    df = df.rename(columns={"Anio": "ano", "Mes": "mes_pal"})
    df["mes_pal"] = df["mes_pal"].map({"Ene": "Jan", "Abr": "Apr", "Ago": "Aug", "Dic": "Dec"})
    df["mes"] = pd.to_datetime(df["mes_pal"], format="%b")
    df["mes"] = df["mes"].apply(lambda x: x.month)
    df["mes-ano"] = df.apply(lambda x: f"{x.mes}-{x.ano}", axis=1)

    df_rainfall, df_macroeconomic = load_dataframe("rainfall_data", "macroeconomic_data", src=dag_run.conf.get("tmp_path"))

    # df_pp
    df_pp = pd.merge(df, df_rainfall, on=["mes", "ano"], how="inner")
    df_pp = df_pp.drop("date", axis=1)

    # df_pp_pib
    df_pp_pib = pd.merge(df_pp, df_macroeconomic, on=["mes", "ano"], how="inner")
    df_pp_pib = df_pp_pib.drop(["Periodo", "Indice_de_ventas_comercio_real_no_durables_IVCM", "mes-ano", "mes_pal"], axis=1)

    df_pp_pib.name = "df"
    save_dataframe(df_pp_pib, dst=dag_run.conf.get("tmp_path"))
