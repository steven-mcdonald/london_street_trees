import os
with open(os.path.join('/Users/Steven/Documents/projects/london_street_trees/','Procfile'), "w") as file1:
    toFile = 'web: sh setup.sh && streamlit run app.py'

file1.write(toFile)
