FROM mcr.microsoft.com/devcontainers/python:3

RUN python -m pip install --upgrade pip
RUN pipx install ruff

RUN sudo apt-get update \
    && sudo apt-get install -y libcairo2-dev

#COPY pyproject.toml .
#RUN touch README.md \
#    && mkdir -p src/tabletop_smith \
#    && python -m flit install --only-deps --deps develop \
#    && rm -r pyproject.toml README.md src