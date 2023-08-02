FROM mcr.microsoft.com/devcontainers/python:3

RUN python -m pip install --upgrade pip
RUN pipx install pdm \
    && pipx install pre-commit

RUN sudo apt-get update \
    && sudo apt-get install -y libcairo2-dev

RUN pre-commit install

#COPY pyproject.toml .
#RUN touch README.md \
#    && mkdir -p src/tabletop_smith \
#    && python -m flit install --only-deps --deps develop \
#    && rm -r pyproject.toml README.md src