import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="ONU Data Visualization - Haïti",
    page_icon="🇺🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1B365D;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .department-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1B365D;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1B365D 0%, #4A90E2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

def load_haiti_data():
    """Charge les données des départements d'Haïti"""
    departments = {
        'Ouest': {
            'population': 4029705, 'superficie': 4825, 'capital': 'Port-au-Prince',
            'projets_onu': 45, 'taux_pauvrete': 65, 'acces_eau': 72,
            'projets_developpement': 18, 'projets_sante': 12, 'projets_education': 8
        },
        'Artibonite': {
            'population': 1727524, 'superficie': 4987, 'capital': 'Gonaïves',
            'projets_onu': 28, 'taux_pauvrete': 78, 'acces_eau': 58,
            'projets_developpement': 12, 'projets_sante': 8, 'projets_education': 5
        },
        'Nord': {
            'population': 1067177, 'superficie': 2115, 'capital': 'Cap-Haïtien',
            'projets_onu': 32, 'taux_pauvrete': 72, 'acces_eau': 65,
            'projets_developpement': 14, 'projets_sante': 9, 'projets_education': 6
        },
        'Nord-Est': {
            'population': 393967, 'superficie': 1805, 'capital': 'Fort-Liberté',
            'projets_onu': 18, 'taux_pauvrete': 82, 'acces_eau': 45,
            'projets_developpement': 8, 'projets_sante': 5, 'projets_education': 3
        },
        'Nord-Ouest': {
            'population': 728807, 'superficie': 2176, 'capital': 'Port-de-Paix',
            'projets_onu': 22, 'taux_pauvrete': 85, 'acces_eau': 40,
            'projets_developpement': 10, 'projets_sante': 6, 'projets_education': 4
        },
        'Centre': {
            'population': 746236, 'superficie': 3487, 'capital': 'Hinche',
            'projets_onu': 25, 'taux_pauvrete': 75, 'acces_eau': 55,
            'projets_developpement': 11, 'projets_sante': 7, 'projets_education': 4
        },
        'Sud': {
            'population': 774976, 'superficie': 2794, 'capital': 'Les Cayes',
            'projets_onu': 30, 'taux_pauvrete': 70, 'acces_eau': 68,
            'projets_developpement': 13, 'projets_sante': 9, 'projets_education': 5
        },
        'Sud-Est': {
            'population': 632601, 'superficie': 2023, 'capital': 'Jacmel',
            'projets_onu': 20, 'taux_pauvrete': 68, 'acces_eau': 62,
            'projets_developpement': 9, 'projets_sante': 6, 'projets_education': 3
        },
        'Grand\'Anse': {
            'population': 468301, 'superficie': 3123, 'capital': 'Jérémie',
            'projets_onu': 15, 'taux_pauvrete': 80, 'acces_eau': 48,
            'projets_developpement': 7, 'projets_sante': 4, 'projets_education': 2
        },
        'Nippes': {
            'population': 342525, 'superficie': 1268, 'capital': 'Miragoâne',
            'projets_onu': 12, 'taux_pauvrete': 78, 'acces_eau': 52,
            'projets_developpement': 6, 'projets_sante': 3, 'projets_education': 2
        }
    }
    return pd.DataFrame.from_dict(departments, orient='index').reset_index().rename(columns={'index': 'Département'})

def load_un_data():
    """Charge les données thématiques ONU"""
    themes_data = {
        'Thème': ['Développement', 'Paix et Sécurité', 'Droits Humains', 
                 'Environnement', 'Santé', 'Éducation', 'Agriculture'],
        'Pourcentage': [25, 20, 15, 12, 18, 10, 8],
        'Budget (Million $)': [45, 35, 25, 20, 32, 18, 15],
        'Projets': [120, 85, 60, 45, 95, 55, 40],
        'Bénéficiaires': [1500000, 850000, 600000, 450000, 1200000, 950000, 700000]
    }
    return pd.DataFrame(themes_data)

def load_organizations_data():
    """Charge les données des organisations ONU"""
    orgs_data = {
        'Organisation': ['PNUD', 'UNICEF', 'PAM', 'OMS', 'UNESCO', 'FAO', 'HCR'],
        'Projets_Haïti': [45, 38, 32, 28, 22, 18, 15],
        'Budget_Haïti': [65, 55, 48, 42, 35, 28, 25],
        'Personnel': [120, 95, 80, 65, 45, 38, 32],
        'Année_établissement': [1979, 1949, 1963, 1948, 1946, 1945, 1951]
    }
    return pd.DataFrame(orgs_data)

def create_department_map(haiti_df):
    """Crée une carte des départements"""
    # Coordonnées approximatives des capitales pour la carte
    coordinates = {
        'Ouest': [18.5392, -72.335],
        'Artibonite': [19.4450, -72.6894],
        'Nord': [19.7595, -72.1980],
        'Nord-Est': [19.6677, -71.8393],
        'Nord-Ouest': [19.9333, -72.8333],
        'Centre': [19.1500, -72.0167],
        'Sud': [18.2000, -73.7500],
        'Sud-Est': [18.2343, -72.5347],
        'Grand\'Anse': [18.6500, -74.1167],
        'Nippes': [18.4500, -73.0833]
    }
    
    map_data = haiti_df.copy()
    map_data['lat'] = map_data['Département'].map(lambda x: coordinates.get(x, [0, 0])[0])
    map_data['lon'] = map_data['Département'].map(lambda x: coordinates.get(x, [0, 0])[1])
    
    fig = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        hover_name="Département",
        hover_data={
            'population': True,
            'projets_onu': True,
            'taux_pauvrete': True,
            'capital': True
        },
        size="projets_onu",
        color="projets_onu",
        color_continuous_scale="Viridis",
        size_max=30,
        zoom=7,
        height=500,
        title="Carte des Projets ONU en Haïti par Département"
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🇺🇳 ONU Data Visualization - Haïti 🇭🇹</h1>', 
                   unsafe_allow_html=True)
    
    # Chargement des données
    haiti_df = load_haiti_data()
    un_df = load_un_data()
    orgs_df = load_organizations_data()
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_the_United_Nations.svg/1200px-Flag_of_the_United_Nations.svg.png", 
                 width=100)
        st.title("Filtres")
        
        selected_department = st.selectbox(
            "Département:",
            ["Tous"] + list(haiti_df['Département'].unique())
        )
        
        selected_theme = st.selectbox(
            "Thème ONU:",
            ["Tous"] + list(un_df['Thème'].unique())
        )
        
        selected_org = st.selectbox(
            "Organisation:",
            ["Tous"] + list(orgs_df['Organisation'].unique())
        )
        
        st.markdown("---")
        st.info("""
        **Source des données:**
        - Nations Unies
        - IHSI Haïti
        - Rapports annuels ONU
        """)
    
    # Métriques principales
    st.subheader("📊 Tableau de Bord - Indicateurs Clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_population = haiti_df['population'].sum()
        st.metric("Population Totale", f"{total_population:,}", "11.4M")
    
    with col2:
        total_projects = haiti_df['projets_onu'].sum()
        st.metric("Projets ONU Actifs", total_projects, "247")
    
    with col3:
        avg_poverty = haiti_df['taux_pauvrete'].mean()
        st.metric("Taux de Pauvreté Moyen", f"{avg_poverty:.1f}%")
    
    with col4:
        total_budget = un_df['Budget (Million $)'].sum()
        st.metric("Budget Total ONU", f"${total_budget}M", "+8.5%")
    
    # Première ligne: Carte et indicateurs
    st.markdown("---")
    st.subheader("🗺️ Carte Interactive des Départements")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_map = create_department_map(haiti_df)
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Classements par Indicateur")
        
        # Top projets
        st.markdown("**Top 3 - Projets ONU**")
        top_projects = haiti_df.nlargest(3, 'projets_onu')
        for _, row in top_projects.iterrows():
            st.markdown(f"""
            <div class="department-card">
                <strong>{row['Département']}</strong><br>
                {row['projets_onu']} projets • {row['capital']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**Top 3 - Accès à l'Eau**")
        top_water = haiti_df.nlargest(3, 'acces_eau')
        for _, row in top_water.iterrows():
            st.markdown(f"""
            <div class="department-card">
                <strong>{row['Département']}</strong><br>
                {row['acces_eau']}% accès eau
            </div>
            """, unsafe_allow_html=True)
    
    # Deuxième ligne: Analyses ONU
    st.markdown("---")
    st.subheader("📈 Analyse des Activités ONU")
    
    tab1, tab2, tab3 = st.tabs(["Par Thème", "Par Organisation", "Indicateurs Combinés"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(
                un_df,
                values='Pourcentage',
                names='Thème',
                title='Répartition des Activités par Thème',
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_budget = px.bar(
                un_df,
                x='Thème',
                y='Budget (Million $)',
                title='Budget par Thème (Millions $)',
                color='Budget (Million $)',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_budget, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig_org = px.bar(
                orgs_df,
                x='Organisation',
                y='Projets_Haïti',
                title='Projets par Organisation',
                color='Projets_Haïti'
            )
            st.plotly_chart(fig_org, use_container_width=True)
        
        with col2:
            fig_bubble = px.scatter(
                orgs_df,
                x='Budget_Haïti',
                y='Personnel',
                size='Projets_Haïti',
                color='Organisation',
                title='Budget vs Personnel',
                size_max=40
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
    
    with tab3:
        # Graphique combiné
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Projets ONU vs Pauvreté', 'Budget vs Bénéficiaires', 
                          'Accès Eau par Département', 'Distribution des Thèmes'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "pie"}]]
        )
        
        # Graphique 1: Projets vs Pauvreté
        fig.add_trace(
            go.Scatter(x=haiti_df['projets_onu'], y=haiti_df['taux_pauvrete'],
                      mode='markers', text=haiti_df['Département'],
                      marker=dict(size=haiti_df['population']/100000, color='blue')),
            row=1, col=1
        )
        
        # Graphique 2: Budget vs Bénéficiaires
        fig.add_trace(
            go.Bar(x=un_df['Thème'], y=un_df['Budget (Million $)'], name='Budget'),
            row=1, col=2
        )
        
        # Graphique 3: Accès eau
        fig.add_trace(
            go.Bar(x=haiti_df['Département'], y=haiti_df['acces_eau'], name='Accès Eau'),
            row=2, col=1
        )
        
        # Graphique 4: Camembert
        fig.add_trace(
            go.Pie(labels=un_df['Thème'], values=un_df['Pourcentage']),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Données détaillées
    st.markdown("---")
    st.subheader("📋 Données Détailées")
    
    dataset_choice = st.radio("Choisir le dataset:", 
                             ["Départements Haïti", "Thèmes ONU", "Organisations"])
    
    if dataset_choice == "Départements Haïti":
        st.dataframe(haiti_df, use_container_width=True)
        csv = haiti_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger données départements",
            data=csv,
            file_name="haiti_departments.csv",
            mime="text/csv"
        )
    elif dataset_choice == "Thèmes ONU":
        st.dataframe(un_df, use_container_width=True)
    else:
        st.dataframe(orgs_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>Application ONU Data Visualization - Haïti</strong></p>
        <p>Développé pour la visualisation des données des Nations Unies en Haïti</p>
        <p>🇺🇳 Nations Unies • 🇭🇹 République d'Haïti • 📊 Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
