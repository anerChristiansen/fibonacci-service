FROM python:3.7

COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r ./requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org gunicorn

RUN adduser app
WORKDIR /home/app
RUN chown -R app:app ./

COPY project ./project

RUN chmod 777 ./project/entrypoint.sh

ENV FLASK_APP project.manage.py

USER app
EXPOSE 5000

CMD sh project/entrypoint.sh