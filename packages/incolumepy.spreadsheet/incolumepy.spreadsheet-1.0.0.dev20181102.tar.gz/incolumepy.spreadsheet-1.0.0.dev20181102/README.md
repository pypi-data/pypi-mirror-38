# README

## Check out do projeto
    git clone git@gitlab.com:development-incolume/incolumepy.spreadsheet.git
    
## Ambiente virtual
    cd incolumepy.spreadsheet
    python -m venv /tmp/venv

## Ativar ambiente virtual
    source venv/bin/activate
    
## Dependências requeridas
    pip install -rrequirements.txt
    
## Gerar pacote pypi
    python setup.py bdist_egg bdist_wheel sdist --formats=gztar,zip

## Upload pacote pypi
    twine upload dist/*
