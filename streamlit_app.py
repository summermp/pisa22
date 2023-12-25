import base64
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.express import choropleth_mapbox
from streamlit_option_menu import option_menu
from streamlit_pagination import pagination_component#https://github.com/Socvest/streamlit-pagination?tab=readme-ov-file
from streamlit_carousel import carousel#https://pypi.org/project/streamlit-carousel/
from streamlit_player import st_player
from st_tabs import TabBar#https://pypi.org/project/st-tabs/
st.set_page_config(page_title='PISA 2022', page_icon="🌎", initial_sidebar_state="expanded", layout='wide')
styles = {
    "container": {
        "margin": "0px !important",
        "padding": "0 !important",
        "align-items": "stretch",
        "background-color": "#fafafa"
    },
    "icon": {
        "color": "black",
        "font-size": "20px"
    }, 
    "nav-link": {
        "font-size": "20px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "#fafa"
    },
    "nav-link-selected": {
        "background-color": "#ff4b4b",
        "font-size": "20px",
        "font-weight": "normal",
        "color": "black",
    },
}
file_path = "pisa2022.csv"
df = pd.read_csv(file_path)
st.sidebar.image('./static/img/oecd.png')
st.image('./static/img/pisa.png', use_column_width=True)
st.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />""", unsafe_allow_html=True)

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md,unsafe_allow_html=True)

def chart1():
    user_country = st.text_input('Country 👇',placeholder='Write the country...', help='The country name')
    df['Rank'] = range(1, len(df) + 1)

    if user_country:
        # Filter DataFrame based on user input
        filtered_df = df[df['Region'].str.lower() == user_country.lower()]
        if not filtered_df.empty:
            # Add Rank column to the filtered DataFrame
            filtered_df['Rank'] = df['Rank']
            # Plotting the bar chart for the specific country
            fig = px.bar(filtered_df, x='Overall Score', y='Region', orientation='h',
                        title=f'Overall Score for {user_country} by Region',
                        labels={'Overall Score': 'Overall PISA Score'},
                        color='Region', color_discrete_sequence=px.colors.qualitative.Set3,
                        hover_name='Region', text=filtered_df['Rank'].apply(lambda x: f'#{x}'))
            fig.update_layout(
                showlegend=False,
                xaxis_title='Overall PISA Score',
                yaxis_title='Region',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial', size=12, color='black'),
                margin=dict(l=50, r=20, t=50, b=50),
            )
            fig.update_traces(
                # marker_color='rgb(44, 160, 44)',  # Bar color
                              marker_line_color='rgb(44, 160, 44)',  # Bar border color
                              marker_line_width=1.5,
                              opacity=0.7,
                              hovertemplate='<b>%{hovertext}</b><br>Average Score: %{x:,.0f}<br>Rank: %{text}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No data found for the country: {user_country}")
    else:
        fig = px.bar(df, x='Overall Score', y='Region', orientation='h',
                    title='Overall Score by Region',
                    labels={'Overall Score': 'Overall PISA Score'},
                    color='Region', color_discrete_sequence=px.colors.qualitative.Set3,
                    hover_name='Region', text=df['Rank'].apply(lambda x: f'#{x}'))
        fig.update_layout(
            showlegend=False,
            xaxis_title='Overall PISA Score',
            yaxis_title='Region',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='black'),
            margin=dict(l=50, r=20, t=50, b=50),
        )
        fig.update_traces(
            marker_color='rgb(44, 160, 44)',  # Bar color
                        marker_line_color='rgb(44, 160, 44)',  # Bar border color
                        marker_line_width=1.5,
                        opacity=0.7,
                        hovertemplate='<b>%{hovertext}</b><br>Average Score: %{x:,.0f}<br>Rank: %{text}')
        st.plotly_chart(fig, use_container_width=True)
        st.success(''' **Singapore** led the global league tables in the mathematics assessment,
followed by *Macau (China)*, *Chinese Taipei*, *Hong Kong (China)*, *Japan*, and *Korea*.

While overall performance levels declined, some education systems made progress towards closing the achievement gap.''', icon='🧐')
def chart2():
    grouped_data = df.groupby("Region")["Overall Score"].mean().reset_index()
    fig = px.choropleth(
        grouped_data,
        locations="Region",
        locationmode="country names",
        color="Overall Score",
        hover_name="Region",
        title="Overall Score by Region",
        color_continuous_scale="Viridis",
        animation_frame="Region",  # Add animation by region
        animation_group="Region",  # Set animation group
    )
    scatter_geo_trace = px.scatter_geo(
        grouped_data,
        locations="Region",
        locationmode="country names",
        text="Overall Score",
        custom_data=["Region"],
    ).update_traces(mode="markers", textposition="middle center", textfont_color="gray",  marker=dict(size=5, line=dict(color="black", width=0.5)))
    fig.add_trace(scatter_geo_trace.data[0])
    fig.update_geos(
        projection_type="natural earth",
        showland=True, landcolor="rgb(255, 255, 255)",
        showocean=True, oceancolor="rgb(204, 229, 255)",
        showcountries=True, countrycolor="rgb(150, 150, 150)",  # Set country border color
    )
    st.plotly_chart(fig, use_container_width=True)
def chart3():
    df_scores = pd.melt(df, id_vars=['Region'], value_vars=['Math Score', 'Science Score', 'Reading Score'],
                    var_name='Subject', value_name='Score')
    fig = px.line(df_scores, x='Region', y='Score', color='Subject',
                    title='Scores by Region',
                    labels={'Score': 'Score', 'Region': 'Region'},
                    color_discrete_map={
                        'Math Score': 'red',
                        'Science Score': 'green',
                        'Reading Score': 'blue'
                    },
                    markers=True
    )
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    fig.update_traces(line=dict(width=2),
                    marker=dict(size=8))
    fig.update_layout(legend=dict(title='Subject'))
    fig.update_xaxes(title_text='Region', showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text='Score', showgrid=True, gridcolor='lightgray')
    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{y}')
    fig.update_layout(
        hovermode='x',  # Display tooltips only on the x-axis
        showlegend=True,
        legend=dict(x=0, y=1),  # Position the legend
        font=dict(family='Arial', size=12, color='black'),  # Font style
        plot_bgcolor='white',  # Background color
        paper_bgcolor='white',  # Plot area background color
        margin=dict(l=20, r=20, t=40, b=20),  # Set margins
        xaxis_tickangle=-45,  # Rotate x-axis labels
        autosize=True,  # Adjust chart size automatically
        template='plotly_white'  # Use a white template for a clean look
    )
    st.plotly_chart(fig, use_container_width=True)
def data_chunk_choice():
    if 'foo' not in st.session_state:
        return 0
    return st.session_state['foo']
def chart4():
    columns_to_hide = ['Math Score', 'Science Score', 'Reading Score']
    df_hidden = df.drop(columns=columns_to_hide)
    grouped_data = df_hidden.sort_values(by="Overall Score", ascending=False)
    grouped_data.insert(0, '#', range(1, len(df) + 1))
    def open_image(path: str):
        with open(path, "rb") as p:
            file = p.read()
            return f"data:image/svg+xml;base64,{base64.b64encode(file).decode()}"
    grouped_data["Flag"] = grouped_data.apply(lambda x: open_image(x["Flag"]), axis=1)
    column_order = ['#', 'Flag', 'Region', 'Overall Score']
    grouped_data = grouped_data[column_order]
    n = 10
    list_df = [grouped_data[i:i+n] for i in range(0, grouped_data.shape[0], n)] 
    if grouped_data.shape[0] % n != 0:
        list_df.append(grouped_data[grouped_data.shape[0] - (grouped_data.shape[0] % n):])
    if data_chunk_choice is not None:
        data_l = list_df[data_chunk_choice()]
    else:
        print("Error: data_chunk_choice is None. Please handle this case appropriately.")    
        st.rerun()
    styled_df = data_l.style.background_gradient(subset=['Overall Score'], cmap='Spectral').set_caption("Row")
    st.dataframe(styled_df, column_config={
            "Flag": st.column_config.ImageColumn("Flag", help="Preview screenshots",),
            "Overall Score": st.column_config.ProgressColumn(
                "Score",
                help="Overall Score",
                format=" %f",
                min_value=0,
                max_value=1000,
            ),
        }, hide_index=True, width=500, height=400)
    st.markdown('''<style> 
    iframe{ height:100px; width:100%; } </style>''', unsafe_allow_html=True)
    layout = {'color':"primary", 'style':{'margin-top':'10px'}}
    pagination_component(len(list_df), layout=layout, key="foo")
def tooltip(image_url, text):
    tooltip_html = f"""
    <style>
    .tooltip {{
        margin:0px;
        padding:0px;
        top:0;
        position: relative;
        display: inline-block;
    }}
    .tooltip span {{
            cursor: pointer;
        }}
    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 250px;
        height: 200px;
        text-align: center;
        border-radius: 6px;
        margin:0px;
        position: fixed;
        z-index: 1;
        top: 0%;
        bottom: 0%;
        left: 50%;
        border: 1px solid orange;
        opacity: 0;
        transition: opacity 0.3s;
        background-color: #f0f0f0;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
        display: none;
    }}
    .tooltip .tooltiptext img {{
        display: block;
        height: 100%; /* Make the image fill the height of the tooltip */
    }}
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
        display: block;
    }}
    </style>

    <div class="tooltip">
        <span>{text}</span>
        <div class="tooltiptext">
            <img src='{image_url}' width='auto' height='auto'/>
        </div>
    </div>
    """
    return tooltip_html
def home():
    autoplay_audio("./static/audio/summer-adventures.mp3")
    st.markdown("""

    <h2 style='margin:0; text-align:center; font-weight:bold;'> <i class="fa-solid fa-square-poll-vertical fa-beat"></i> <span style='color:#262261;'> PISA 2022 Results</span></h2>""", unsafe_allow_html=True)
    test_items = [
    dict(title="",text="",interval=None,img="https://pisa22.streamlit.app/app/static/img/banner/insight1.png",),
    dict(title="",text="",interval=2000,img="https://pisa22.streamlit.app/app/static/img/banner/insight2.png",),
    dict(title="",text="",interval=2000,img="https://pisa22.streamlit.app/app/static/img/banner/insight3.png",),
    dict(title="",text="",interval=2000,img="https://pisa22.streamlit.app/app/static/img/banner/insight4.png",),
    dict(title="",text="",interval=2000,img="https://pisa22.streamlit.app/app/static/img/banner/insight5.png",),
    dict(title="",text="",interval=None,img="https://pisa22.streamlit.app/app/static/img/banner/insight6.png",),
    ]

    carousel(items=test_items, width=1, height=500)
    st.markdown("<h4 style='margin:0; font-weight:bold;'>Supporting students in and beyond the classroom is key</h4>", unsafe_allow_html=True)
    st.image('./static/img/supporting_students.png', use_column_width=True)
    st.markdown('**Source:** OECD, PISA 2022 Database')
    tab = TabBar(tabs=["Info 1", "Info 2", "Info 3", "Info 4", "Info 5", "Info 6", "Info 7", "Info 8"],default=0,background = "#F0F8FF",color="grey",activeColor="blue",fontSize="20px")
    if tab == 0:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>… Around 690 000 students took
        the PISA assessment in 2022,
        representing about 29 million
        15-year-olds from schools
        in 81 participating countries
        and economies. 

        </p>
        </div>
        ''', unsafe_allow_html=True)
    if tab == 1:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>… PISA assesses 15-year-olds as
        this is the last point at which
        most children are still enrolled
        in formal education.

        </p>
        </div>
        ''', unsafe_allow_html=True)
    elif tab == 2:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>… Students who attain PISA
        Level 5 or Level 6 are top
        performers; for example,
        they can work eff ectively with
        mathematical models for
        complex situations, comprehend
        abstract texts, and interpret and
        evaluate complex experiments. 

        </p>
        </div>
        ''', unsafe_allow_html=True)
    elif tab == 3:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>...45% of students reported
        feeling nervous or anxious if
        their phones were not near
        them, on average across
        OECD countries. 

        </p>
        </div>
        ''', unsafe_allow_html=True)
    elif tab == 4:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>...Seven out of ten students
        reported that they regularly
        received extra help from
        teachers in 2022, while 22% of
        students reported getting help
        in some lessons. Around 8%
        never or almost never received
        additional support,
        across the OECD. 

        </p>
        </div>
        ''', unsafe_allow_html=True)
    elif tab == 5:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>... PISA uses real life problems to
        assess students’ abilities through
        multiple-choice and open-ended
        questions. Students also answer
        a background questionnaire
        about themselves, their learning
        attitudes and their homes.  

        </p>
        </div>
        ''', unsafe_allow_html=True)
    elif tab == 6:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>… The average OECD scores in
        2022 were 472 in maths, 476
        in reading and 485 in science.
        These scores were at the upper
        end of PISA Level 2 in maths and
        reading while at the lower end of
        PISA Level 3 in science. 

        </p>
        </div>
        ''', unsafe_allow_html=True)
    elif tab == 7:
        st.markdown(''' 
        <div style='background-color:#D7EDFA; border-radius:8px;'>
        <h3 style='text-align:center; color:skyblue; font-weight:bold;'>Did you know…</h3>
        <p style='padding: 5px 0px; text-align:center; color: #262261; white-space: pre-line; font-weight:bold;'>… That 20 points in PISA tests
        is roughly equivalent to one
        year of schooling. 

        </p>
        </div>
        ''', unsafe_allow_html=True)
    
def about():
    txt1 = tooltip('https://pisa22.streamlit.app/app/static/img/students_talking.png', "<span style='boder: 1px solid blue; border-radius:4px; background-color:green; color: white; padding:2px;'><i class='fa-solid fa-child-reaching fa-fade'></i> 15-year-old students <i class='fa-solid fa-child-dress fa-fade'></i></span>")
    html("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <style>html{border: 1px solid #de3f53;padding: 4px;}</style>
    <h2 style='color: #de3f53; border-bottom: solid 5px; '>What is PISA?</h2>    
    
    <a href='https://www.oecd.org/pisa/' target='_blank'><b>PISA</b></a> stands for the "<b>Programme for International Student Assessment</b>".
    It is an international assessment conducted by the <a href='https://www.oecd.org' target='_blank'>Organisation for Economic Co-operation and Development (OECD)</a>
    to evaluate the knowledge and skills of"""+txt1+""" in 
    <span style='color: blue;font-weight: bold;'>reading <i class="fa-solid fa-book-open-reader fa-beat"></i></span>, 
    <span style='color: red; font-weight: bold;'>mathematics <i class="fa-solid fa-calculator fa-fade"></i></span>, and 
    <span style='color: green;font-weight: bold;'>science <i class="fa-solid fa-flask-vial fa-shake"></i></span>. PISA assessments are conducted <b>every three years</b>, 
    and the results provide insights into the performance of education systems around the <span style='margin-top: 0px;margin-bottom: 10px;font-family: sans-serif; font-weight: bold; background: linear-gradient(to right, #ef5350, #f48fb1, #7e57c2, #2196f3, #26c6da, #43a047, #eeff41, #f9a825, #ff5722);-webkit-background-clip: text;-webkit-text-fill-color: transparent;'>world</span>.
    """, height=200)

    st_player("https://www.youtube.com/watch?v=6JstvTnZjHM", playing=True, loop=True, volume=1, controls=False, height=400)
    with st.expander("**Key features of PISA include:**"):
        st.markdown('''
        1. **Cross-National Comparison:** PISA assesses students from a wide range of countries, allowing for cross-national comparisons of educational outcomes.

        2. **Focus on Real-World Skills:** PISA goes beyond traditional academic knowledge and focuses on assessing students' ability to apply their knowledge and skills to real-world problems.

        3. **Rotating Domains:** While reading, mathematics, and science are the core domains, each assessment cycle may also include a focus on one additional domain, such as collaborative problem-solving or financial literacy.

        4. **Assessment of Competencies:** PISA assesses not only what students know but also their ability to use their knowledge and skills to solve problems and meet challenges.

        5. **Sample-Based Approach:** PISA employs a sample-based approach, meaning that not all students in a country participate. Instead, a representative sample is selected to provide insights into the overall performance of the education system.
        ''')
    st.info('''
    The results of **PISA** assessments are widely used by **policymakers**, **educators**, and **researchers** to:

    * **Identify** strengths and weaknesses in education systems.
    * **Inform** educational policies.
    * **Explore** factors that contribute to successful student outcomes.

    **PISA** has become an **important** tool for **understanding** and **improving** the **quality** of education on a global scale.

    ''', icon="🧐")
    st.link_button("Go to pisa 2022 results volume I", "https://www.oecd-ilibrary.org/education/pisa-2022-results-volume-i_53f23881-en", type='primary')    
    
menu = {
    'title': 'Main menu',
    'items': { 
        'Home' : {
            'action': home,
            'item_icon': 'house',
        },
        'Insights' : {
            'action': None,
            'item_icon': 'bar-chart',
            'submenu': {
                'title': None,
                'items': {
                    'Bar chart' : {'action': chart1, 'item_icon': 'bar-chart-fill', 'submenu': None},
                    'Geo map' : {'action': chart2, 'item_icon': 'globe-americas', 'submenu': None},
                    'Line chart' : {'action': chart3, 'item_icon': 'bar-chart-line-fill', 'submenu': None},
                    'Ranking' : {'action': chart4, 'item_icon': 'table', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            } 
        },
        'About' : {
            'action': about,
            'item_icon': 'people'
        },
    },
    'menu_icon': 'clipboard2-check-fill', 
    'default_index': 0,
    'with_view_panel': 'sidebar',
    'orientation': 'vertical',
    'styles': styles
}

def show_menu(menu):
    def _get_options(menu):
        options = list(menu['items'].keys())
        return options
    def _get_icons(menu):
        icons = [v['item_icon'] for _k, v in menu['items'].items()]
        return icons
    kwargs = {
        'menu_title': menu['title'],
        'options': _get_options(menu),
        'icons': _get_icons(menu),
        'menu_icon': menu['menu_icon'],
        'default_index': menu['default_index'],
        'orientation': menu['orientation'],
        'styles': menu['styles']
    }
    with_view_panel = menu['with_view_panel']
    if with_view_panel == 'sidebar':
        with st.sidebar:
            menu_selection = option_menu(**kwargs)
    elif with_view_panel == 'main':
        menu_selection = option_menu(**kwargs)
    else:
        raise ValueError(f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")
    if 'submenu' in menu['items'][menu_selection] and menu['items'][menu_selection]['submenu']:
        show_menu(menu['items'][menu_selection]['submenu'])
    if 'action' in menu['items'][menu_selection] and menu['items'][menu_selection]['action']:
        menu['items'][menu_selection]['action']()
show_menu(menu)
st.sidebar.markdown('''
<div style='padding:5px 5px 1px 5px; border-radius:8px; background-color: orange; color:white;'>
<h4 style='color: white; padding:3px; font-weight:bold;'><i class="fa-solid fa-circle-chevron-right"></i> PISA 2025</h4>
<hr style='margin:0px 0px 5px 0px; padding:0; border: 2px solid white;'>
Focus on science and include:

<i class="fa-solid fa-language"></i> Foreign languages <br/>
<i class="fa-solid fa-globe"></i> Learning in the Digital World
</div>''', unsafe_allow_html=True)
st.components.v1.html(
    """
    <script>
    // Locate elements
    var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
    var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];

    // Observe sidebar size
    function outputsize() {
        decoration.style.left = `${sidebar.offsetWidth}px`;
    }

    new ResizeObserver(outputsize).observe(sidebar);

    // Adjust sizes
    outputsize();
    decoration.style.height = "6.0rem";
    decoration.style.right = "45px";

    // Adjust image decorations
    decoration.style.backgroundImage = "url(https://pisa22.streamlit.app/app/static/img/banner/merry_christmas.gif)";
    decoration.style.backgroundSize = "contain";
    </script>        
    """, width=0, height=0)
