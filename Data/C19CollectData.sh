echo -e $(date) 'Removing old data'
cd /Users/paulhart/Documents/Development/CovidProjects/Data
rm -rf COVID-19

echo -e $(date) 'Cloning data'
git clone https://github.com/CSSEGISandData/COVID-19.git
