FROM python:3.12 as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app"
ENV PATH="${PATH}:/home/python/.local/bin"
ENV USER="python"

RUN useradd --create-home python \
  && chown -R python:python /app \
  && apt-get update \
  && apt-get install -y \
    gcc \
    libmariadb-dev \
  && rm -rf /var/lib/apt/lists/*

USER python

COPY --chown=python:python \
  requirements.txt \
  docker-entrypoint.sh \
  ./
RUN pip install --no-warn-script-location --user -r requirements.txt

ENTRYPOINT [ "./docker-entrypoint.sh" ]

#-- setup python requirements and django --#
FROM base as production

RUN mkdir -p static_root

COPY --chown=python:python . .

CMD ["gunicorn", "-c", "python:portfolio.gunicorn", "portfolio.wsgi"]
