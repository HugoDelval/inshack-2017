all:
	rm -rf .git/
	git init
	git config user.name 'John Doe'
	git config user.email 'john.doe@smart-sensors.inshack.com'
	git add .gitignore
	git commit -m "Initial commit, adding gitignore file"
	git add src/smart_sensors_api.py
	git commit -m "Adding main flask-based API entry point"
	git add src/utils/ini.py
	git commit -m "Adding ini module"
	git add config/
	git add smart_sensors_api.ini
	git commit -m "Adding configuration link"
	git rm --cached config/smart_sensors_api.ini
	git add src/utils/validator.py
	git commit -m "Adding validator module : so much regexp I'm exhausted. Ooohhh... dumb..."
	git add src/utils/response.py
	git commit -m "Adding Response class"
	git add src/utils/wrappers.py
	git commit -m "Adding custom wrappers zbra..."
	git add run.py
	git commit -m "Adding launcher."
	git add src/utils/sensors.py	
	git commit -m "Adding sensors wrapper."
