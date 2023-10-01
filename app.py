import pandas as pd
import streamlit as st
from search_product import search_product
import sys
import st_aggrid as st_agg
#import wikipedia
from streamlit_searchbox import st_searchbox
from analytics import page1, page2

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re




def main():
    st.set_page_config("Добро пожаловать в приложение Мипсы МИСИС")
    st.markdown("""
    # Tender Search Engine
    """)
    def user_input_features():
        
        data = pd.read_csv('the_final_df.csv', delimiter=',')
        #data = data.drop('full_desc', axis=1)
        data['category'] = data['category'] + ' (' + data['okpd'] + ')'
        # data['vendor'] = data['vendor'] + ' (INN: ' + data['inn'].apply(str) + ')'
        # st.write(data.columns)
        # Create a sidebar with navigation options
        st.sidebar.title("Навигация")
        page_options = ["Товару", "Поставщикам", "Отраслям"]
        selected_page = st.sidebar.radio("Анализ по", page_options)

        # Display the selected page
        if selected_page == "Поставщикам":
            page1(data)
        elif selected_page == "Отраслям":
            page2(data)
        else:
            product = st.sidebar.text_input("Введите название товара","").lower().strip()
       # st.sidebar.title("Выбор поставщика/категории")
        #page_options = ["Поставщики", "Категории"]
        #selected_page = st.sidebar.radio("перейти к", page_options)

        # Display the selected page
        #if selected_page == "Поставщики":
         #  page1()
        #elif selected_page == "Категории":
         #   page2()

            city = st.sidebar.text_input("Введите город доставки","").lower().strip()
        
            sort_type = st.sidebar.selectbox('cортировка по', ('цене', 'величине фирмы', 'отзывам'))
            
            return [product, city, sort_type]
        return [""]
    input_features = user_input_features()
    click = st.sidebar.button('Поиск')
   
    if click and  input_features[0] != "":
        #old_search_request = input_features[0]
        #if not utils.has_only_latin_letters(search_request):
         #   search_request = jsp.FixFragment(search_request)
        #if old_search_request != search_request:
         #   st.markdown(f"""
          #              Автоисправление <br/>
           #             {old_search_request} было заменено на {search_request}
            #            """, unsafe_allow_html=True)
                        
        path = search_product(input_features[1:])
        figs_expander = st.expander("Анализ рынка")
        search_results = pd.read_csv(path, delimiter=",", low_memory=False)
        gb_main = st_agg.GridOptionsBuilder.from_dataframe(search_results)
        gb_main.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, editable=False)
        gb_main.configure_side_bar()
        #gb_main.configure_selection(selection_mode="single", use_checkbox=True)
        gb_main.configure_pagination(
            paginationPageSize=10, paginationAutoPageSize=False)
        gb_main.configure_grid_options(domLayout='normal')
        grid_main_options = gb_main.build()
        grid_main_response = st_agg.AgGrid(
            search_results,
            gridOptions=grid_main_options,
            width='100%',
            update_mode=st_agg.GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=True,
            enable_enterprise_modules=True,
            key='inn',
            reload_data=False,
            use_checkbox=True,
            theme = "streamlit"
        )
        
if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Error. Not enough parameters.")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("Error. Too many parameters.")
        sys.exit(1)
    main()
