import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

uploaded_file = st.file_uploader("Scegli un file CSV", type="xlsx")

if uploaded_file is not None:

    # CHART 1

    # Supponiamo di avere un DataFrame con le colonne specificate
    df = pd.read_excel(uploaded_file)

    # Titolo della dashboard
    st.title('Dashboard Autodeterminazione')

    # Mostra le prime righe del DataFrame
    st.write("Prime 5 righe del dataset.")
    st.dataframe(df.head())

    # CHART 2

    sedi = df['Sede'].unique().tolist()
    sedi.insert(0, "Tutte le sedi")

    # Titolo dell'app
    st.subheader("Frequenze Seniority per Sede")

    # Menù a tendina per selezionare la sede
    sede_selezionata = st.selectbox("Seleziona una sede", sedi)

    # Filtriamo il DataFrame in base alla sede selezionata
    if sede_selezionata == "Tutte le sedi":
        df_filtrato = df
    else:
        df_filtrato = df[df['Sede'] == sede_selezionata]

    # Istogramma della seniority per la sede selezionata
    st.subheader(f"Frequenza di Seniority per la sede: {sede_selezionata}")
    fig, ax = plt.subplots()
    ax.set_xlabel('Seniority')
    ax.set_ylabel('Frequenza')
    df_filtrato['Seniority'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # CHART 3

    st.subheader("Presenza Autodeterminazione e Importanza Autodeterminazione Seniority e Sede")

    # Dizionari per etichette personalizzate
    # x_axis_labels = {
    #     'Indica la tua seniority': 'Seniority',
    #     'Indica la tua sede': 'Sede'
    # }

    # y_axis_labels = {
    #     "Tra i valori di Maize, quanto ritieni presente l'autodeterminazione? \n": "Presenza Autodeterminazione",
    #     "Tra i valori di Maize, quanto ritieni importante per te l’autodeterminazione?": "Importanza Autodeterminazione"
    # }

    # Inizializzazione dello stato
    if 'submit' not in st.session_state:
        st.session_state.submit = False

    col1, col2, col3 = st.columns(3)
    with col1:
        x_axis = st.selectbox('Seleziona la colonna per l\'asse X:', ["Sede", "Seniority"])

    with col2:
        y_axis = st.selectbox('Seleziona la colonna per l\'asse Y:', ["Presenza Autodeterminazione", "Importanza Autodeterminazione"])

    with col3:
        st.write("")
        st.write("")
        if st.button('Visualizza grafico'):
            st.session_state.submit = True

    if st.session_state.submit:
        # Creazione del primo istogramma
        fig, ax = plt.subplots()
        grouped_data = df.groupby(x_axis)[y_axis].mean()
        bars = ax.bar(grouped_data.index, grouped_data.values)

        # Aggiunta delle etichette alle barre
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

        # ax.set_xlabel(x_axis_labels[x_axis])
        # ax.set_ylabel(y_axis_labels[y_axis])
        # ax.set_title(f'{y_axis_labels[y_axis]} vs {x_axis_labels[x_axis]}')

        # Visualizzazione del grafico
        st.pyplot(fig)

        # Creazione del secondo grafico con filtro sulla seniority o sede
        st.subheader("Distribuzione di Y-Axis filtrata per Seniority o Sede")
        
        if x_axis == 'Seniority':
            filter_label = 'Seniority'
            filter_options = ['Tutte'] + list(df['Seniority'].unique())
        else:
            filter_label = 'Sede:'
            filter_options = ['Tutte'] + list(df['Sede'].unique())
        
        filter_value = st.selectbox(filter_label, filter_options)

        if filter_value != 'Tutte':
            filtered_data = df[df[x_axis] == filter_value]
        else:
            filtered_data = df

        fig2, ax2 = plt.subplots()
        ax2.hist(filtered_data[y_axis], bins=10, edgecolor='black')

        # ax2.set_xlabel(y_axis_labels[y_axis])
        # ax2.set_ylabel('Frequenza')
        # ax2.set_title(f'Distribuzione di {y_axis_labels[y_axis]} per {filter_value}')

        # Visualizzazione del secondo grafico
        st.pyplot(fig2)

    # CHART 4

    st.title("Analisi Topic")

    col1, col2 = st.columns(2)

    seniority = df['Seniority'].unique().tolist()
    seniority.insert(0, "Tutte le seniority")

    with col1:
        seniority_selezionata = st.selectbox("Seleziona una seniority", seniority)

    indici_colonne = [0, 3, 4, 5, 6]
    colonne_da_mostrare = df.columns[indici_colonne]

    with col2:
        colonna_selezionata = st.selectbox("Seleziona una domanda", colonne_da_mostrare)

    topics_colonna = df[f"topics_{colonna_selezionata}"]

    # Utilizziamo session state per mantenere lo stato del pulsante e del valore selezionato
    if "submit_button_1" not in st.session_state:
        st.session_state.submit_button_1 = False

    if st.button('Visualizza Topic'):
        st.session_state.submit_button_1 = True

    if st.session_state.submit_button_1:
        # Filtriamo il DataFrame in base alla seniority selezionata
        if seniority_selezionata != "Tutte le seniority":
            df_filtrato_seniority = df[df['Seniority'] == seniority_selezionata]
        else:
            df_filtrato_seniority = df

        # Mostra la frequenza dei valori unici di topics_colonna
        st.subheader(f"Frequenza dei valori unici di {colonna_selezionata}")
        fig, ax = plt.subplots()
        df_filtrato_seniority[f"topics_{colonna_selezionata}"].value_counts().plot(kind='barh', ax=ax)  # Invertiamo gli assi utilizzando 'barh'
        st.pyplot(fig)
        
        # Menù a tendina per selezionare un valore unico della colonna selezionata
        valore_unico_selezionato = st.selectbox("Seleziona un valore unico", df_filtrato_seniority[f"topics_{colonna_selezionata}"].unique(), key="valore_unico_selezionato")
        
        # Mostra il DataFrame filtrato solo se è stato selezionato un valore unico
        if valore_unico_selezionato:
            st.subheader(f"DataFrame filtrato per {colonna_selezionata} = {valore_unico_selezionato}")
            df_filtrato_finale = df_filtrato_seniority[df_filtrato_seniority[f"topics_{colonna_selezionata}"] == valore_unico_selezionato]
            st.dataframe(df_filtrato_finale[[colonna_selezionata]], width=2000)
