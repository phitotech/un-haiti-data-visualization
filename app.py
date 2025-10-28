import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="ONU Data Visualization - Haïti",
    page_icon="🇺🇳",
    layout="wide"
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
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_haiti_data():
    """Charge les données des départements d'Haïti"""
    data = {
        'Département': ['Ouest', 'Artibonite', 'Nord', 'Nord-Est', 'Nord-Ouest', 
                       'Centre', 'Sud', 'Sud-Est', 'Grand\'Anse', 'Nippes'],
        'Population': [4029705, 1727524, 1067177, 393967, 728807, 
                      746236, 774976, 632601, 468301, 342525],
        'Superficie_km2': [4825, 4987, 2115, 1805, 2176, 3487, 2794, 2023, 3123, 1268],
        'Capital': ['Port-au-Prince', 'Gonaïves', 'Cap-Haïtien', 'Fort-Liberté', 'Port-de-Paix',
                   'Hinche', 'Les Cayes', 'Jacmel', 'Jérémie', 'Miragoâne'],
        'Projets_ONU': [45, 28, 32, 18, 22, 25, 30, 20, 15, 12],
        'Taux_Pauvrete': [65, 78, 72, 82, 85, 75, 70, 68, 80, 78],
        'Acces_Eau': [72, 58, 65, 45, 40, 55, 68, 62, 48, 52]
    }
    return pd.DataFrame(data)

def load_un_data():
    """Charge les données thématiques ONU"""
    data = {
        'Thème': ['Développement', 'Paix et Sécurité', 'Droits Humains', 
                 'Environnement', 'Santé', 'Éducation'],
        'Pourcentage': [25, 20, 15, 12, 18, 10],
        'Budget_Million_USD': [45, 35, 25, 20, 32, 18],
        'Projets': [120, 85, 60, 45, 95, 55]
    }
    return pd.DataFrame(data)

def load_organizations_data():
    """Charge les données des organisations ONU"""
    data = {
        'Organisation': ['PNUD', 'UNICEF', 'PAM', 'OMS', 'UNESCO', 'FAO'],
        'Projets_Haïti': [45, 38, 32, 28, 22, 18],
        'Budget_Haïti_Million': [65, 55, 48, 42, 35, 28],
        'Personnel': [120, 95, 80, 65, 45, 38]
    }
    return pd.DataFrame(data)

def main():
    # Header
    st.markdown('<h1 class="main-header">🇺🇳 ONU Data Visualization - Haïti 🇭🇹</h1>', 
               unsafe_allow_html=True)
    
    # Chargement des données
    haiti_df = load_haiti_data()
    un_df = load_un_data()
    orgs_df = load_organizations_data()
    
    # Sidebar
    with st.sidebar:
        st.title("🔍 Filtres")
        
        selected_department = st.selectbox(
            "Département:",
            ["Tous"] + list(haiti_df['Département'].unique())
        )
        
        selected_theme = st.selectbox(
            "Thème ONU:",
            ["Tous"] + list(un_df['Thème'].unique())
        )
    
    # Métriques principales
    st.subheader("📊 Indicateurs Clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_population = haiti_df['Population'].sum()
        st.metric("Population Totale", f"{total_population:,}")
    
    with col2:
        total_projects = haiti_df['Projets_ONU'].sum()
        st.metric("Projets ONU", total_projects)
    
    with col3:
        avg_poverty = haiti_df['Taux_Pauvrete'].mean()
        st.metric("Pauvreté Moyenne", f"{avg_poverty:.1f}%")
    
    with col4:
        total_budget = un_df['Budget_Million_USD'].sum()
        st.metric("Budget ONU", f"${total_budget}M")
    
    # Première ligne: Graphiques
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique des projets par département
        fig1 = px.bar(
            haiti_df,
            x='Département',
            y='Projets_ONU',
            title='Projets ONU par Département',
            color='Projets_ONU',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Camembert des thèmes ONU
        fig2 = px.pie(
            un_df,
            values='Pourcentage',
            names='Thème',
            title='Répartition des Activités par Thème'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Deuxième ligne: Autres visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        # Budget par organisation
        fig3 = px.bar(
            orgs_df,
            x='Organisation',
            y='Budget_Haïti_Million',
            title='Budget par Organisation (Millions USD)',
            color='Budget_Haïti_Million'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Corrélation projets vs pauvreté
        fig4 = px.scatter(
            haiti_df,
            x='Projets_ONU',
            y='Taux_Pauvrete',
            size='Population',
            color='Département',
            title='Projets ONU vs Taux de Pauvreté',
            size_max=40
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Tableaux de données
    st.markdown("---")
    st.subheader("📋 Données Détailées")
    
    tab1, tab2, tab3 = st.tabs(["Départements", "Thèmes ONU", "Organisations"])
    
    with tab1:
        st.dataframe(haiti_df, use_container_width=True)
        
        # Téléchargement
        csv = haiti_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger données départements",
            data=csv,
            file_name="haiti_departments.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.dataframe(un_df, use_container_width=True)
    
    with tab3:
        st.dataframe(orgs_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>Application ONU Data Visualization - Haïti</strong></p>
        <p>Développé avec Streamlit • Données simulées pour démonstration</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
