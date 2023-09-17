

PROJECT=clean-archi-demo

create-archive:
	rm -f clean-archi-demo.tar.gz
	~/.local/bin/poetry export -o requirements.txt
	cd .. && tar -czvf clean-archi-demo/clean-archi-demo.tar.gz --exclude "__pycache__" ${PROJECT}/Procfile ${PROJECT}/project ${PROJECT}/requirements.txt

deploy:
	scalingo --app test-fastapi deploy clean-archi-demo.tar.gz