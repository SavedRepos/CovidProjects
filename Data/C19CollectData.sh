echo
echo  $(date) "End C9 Data Collection starting"

echo -e $(date) 'Python version'
/usr/local/bin/python3 --version

echo -e $(date) 'Removing old data'
cd /Users/paulhart/Documents/Development/CovidProjects/Data
rm -rf COVID-19

echo -e $(date) 'Cloning data'
git clone https://github.com/CSSEGISandData/COVID-19.git

echo -e $(date) 'Creating csv data'
/usr/local/bin/python3 /Users/paulhart/Documents/Development/CovidProjects/Apps/C19DataCollection/CovidDataMain.py
echo -e $(date) 'Creating csv data complete'
echo 

echo -e "Add files"
/Users/paulhart/Documents/Development/CovidProjects
git add --all

echo 
echo -e  $(date) "Commit files"
git commit -m "Daily update $(date)"

echo 
echo -e  $(date) "Push files to Github"
git push -u origin master

echo
echo  $(date) "End C9 Data Collection complete"
