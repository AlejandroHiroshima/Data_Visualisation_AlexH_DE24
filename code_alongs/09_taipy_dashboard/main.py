# Importerar nödvändiga bibliotek
import taipy.gui.builder as tgb  # Taipy's GUI-byggverktyg
from taipy.gui import Gui        # Huvudklassen för Taipy's GUI
import pandas as pd              # För datahantering
from utils.constants import DATA_DIRECTORY  # Sökväg till datakatalogen
from frontend.charts import create_municipality_bar  # Funktion för att skapa stapeldiagram

# Läser in Excel-filen, hoppar över de första 5 raderna och väljer fliken "Tabell 3"
df = pd.read_excel(
    DATA_DIRECTORY / "resultat-ansokningsomgang-2024.xlsx",
    sheet_name="Tabell 3",
    skiprows=5,
)

# Funktion som filtrerar dataframe baserat på utbildningsområde
# Returnerar en ny dataframe med antal utbildningar per kommun
def filter_df_municipality(df, educational_area="Data/IT"):
    return (
        df.query("Utbildningsområde == @educational_area")["Kommun"]  # Filtrerar på utbildningsområde
        .value_counts()                                               # Räknar förekomster per kommun
        .reset_index()                                               # Gör index till en kolumn
        .rename({"count": "Ansökta utbildningar"}, axis=1)          # Byter namn på kolumnen
    )

# Callback-funktion som uppdaterar diagrammet när användaren ändrar filter
def filter_data(state):
    print(state)  # Debugutskrift av aktuellt state
    # Skapar ny filtrerad dataframe baserat på valt utbildningsområde
    df_municipality = filter_df_municipality(state.df, state.selected_educational_area)

    # Uppdaterar diagrammet med nya data
    state.municipality_chart = create_municipality_bar(
        df_municipality.head(state.number_municipalities),
        xlabel="# ANSÖKTA UTBILDNINGAR",
        ylabel="KOMMUN",
    )

# Initiala värden för filter
number_municipalities = 5
selected_educational_area = "Data/IT"

# Skapar initial filtrerad dataframe
df_municipality = filter_df_municipality(df, selected_educational_area).head(
    number_municipalities
)

# Skapar initialt diagram
municipality_chart = create_municipality_bar(
    df_municipality, xlabel="# ANSÖKTA UTBILDNINGAR", ylabel="KOMMUN"
)

# Bygger upp GUI:t med Taipy
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# MYH dashboard 2024", mode="md")  # Huvudrubrik

        with tgb.layout(columns="2 1"):  # Skapar 2-kolumns layout
            with tgb.part(class_name="card"):
                tgb.text("Graph")
                tgb.chart(figure="{municipality_chart}")  # Visar diagrammet

            with tgb.part(class_name="card"):
                tgb.text("## Filtrera data", mode="md")
                tgb.text("Filtrera antalet kommuner", mode="md")

                # Slider för att välja antal kommuner
                tgb.slider(
                    "{number_municipalities}",
                    min=5,
                    max=len(df_municipality),
                    continuous=False,
                )

                # Dropdown för att välja utbildningsområde
                tgb.text("Välj utbildningsområde", mode="md")
                tgb.selector(
                    "{selected_educational_area}",
                    lov=df["Utbildningsområde"].unique(),
                    dropdown=True,
                )

                # Knapp för att uppdatera data
                tgb.button("FILTRERA DATA", class_name="plain", on_action=filter_data)

        # Visar rå data i en tabell
        with tgb.part(class_name="card"):
            tgb.text("Raw data")
            tgb.table("{df}")

# Startar GUI:t om scriptet körs direkt
if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)