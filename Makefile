gunicorn-logs:
	journalctl -ru gunicorn

collect-static:
	python3 manage.py collectstatic --noinput
