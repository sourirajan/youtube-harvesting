import tab_load
import tab_analyze
import tab_data
import streamlit as st
import traceback

def main():

    load_tab, analyze_tab, data_tab = st.tabs(["Load","Analyze","Data"])

    with load_tab:
        try :
            tab_load.load()
        except Exception as e:
            traceback.print_exc()
            st.error("Error occured loading data from youtube")
            return
    with analyze_tab:
        try :
            tab_analyze.load()
        except Exception as e:
            traceback.print_exc()
            st.error("Error occured loading data from database")
            return
    with data_tab:
        try :
            tab_data.load()
        except Exception as e:
            traceback.print_exc()
            st.error("Error occured loading data from database")
            return

if __name__ == "__main__":
    main()