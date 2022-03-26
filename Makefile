WORKFLOW_NAME = homeassistant

WORKFLOW_FILES = info.plist install.sh python requirements.txt state.py template.py icon.png

.PHONY: workflow install clean

workflow: ${WORKFLOW_NAME}.alfredworkflow

${WORKFLOW_NAME}.alfredworkflow:
	zip -r7y ${WORKFLOW_NAME}.alfredworkflow ${WORKFLOW_FILES}

install: ${WORKFLOW_NAME}.alfredworkflow
	open ${WORKFLOW_NAME}.alfredworkflow

clean:
	rm -rf *.alfredworkflow venv tmp 
