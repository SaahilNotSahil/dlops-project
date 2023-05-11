# DL Lab Project - ViLT for Visual Question Answering

### Steps to run (Without Docker)

- ``` git clone https://github.com/XanderWatson/dlops-project ```
- ``` cd dlops-project/ ```
- ``` git clone https://github.com/XanderWatson/ViLT ```
- ``` cd ViLT ```
- ``` python setup.py install ```
- ``` cd .. ```
- ``` pip install -r requirements.txt ```
- ``` streamlit run ui.py ```

The streamlit interface will now be running at http://localhost:8501

### Steps to run (With Docker)

(First three steps same as above)

- ``` docker compose -f production/docker-compose.yml up --build -d ```

The streamlit interface will now be running at http://0.0.0.0:6969
