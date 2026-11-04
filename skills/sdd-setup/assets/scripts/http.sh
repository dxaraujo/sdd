#!/bin/sh
# sdd — chamada HTTP do agente sdd-verificador, só para a URL de teste do projeto.
# Instalado pela sdd-setup em .kiro/sdd/http.sh (o verificador tem permissão para rodar só este script, e nenhum
# agente pode alterá-lo). A URL vem da seção Verificação de aceite do .kiro/steering/sdd.md; mudou → rode a setup.
#
# Uso (da raiz do repositório):
#   sh .kiro/sdd/http.sh <MÉTODO> <caminho> [corpo.json]
#   ex.: sh .kiro/sdd/http.sh POST /api/saldos .kiro/specs/ft-031-saldo/massa/saldo-ok.json
# O corpo só pode vir da pasta massa/ de uma fatia. Token: variável SDD_HTTP_TOKEN (Bearer), se o ambiente pedir.
set -eu

BASE='{{URL_TESTE}}'

erro() { echo "http.sh: $1" >&2; exit 2; }

[ $# -ge 2 ] && [ $# -le 3 ] || erro "uso: sh .kiro/sdd/http.sh <MÉTODO> <caminho> [corpo.json]"
METODO=$1
CAMINHO=$2
CORPO=${3:-}

case $METODO in GET | POST | PUT | PATCH | DELETE | HEAD) ;; *) erro "método não permitido: $METODO" ;; esac
case $CAMINHO in /*) ;; *) erro "o caminho deve começar com / (a URL base é fixa)" ;; esac
case $CAMINHO in *[[:space:]]* | *'\'*) erro "caminho com espaço ou barra invertida" ;; esac

set -- -sS -i --max-time 60 -X "$METODO"
if [ -n "${SDD_HTTP_TOKEN:-}" ]; then
  set -- "$@" -H "Authorization: Bearer $SDD_HTTP_TOKEN"
fi

if [ -n "$CORPO" ]; then
  case $CORPO in *..*) erro "corpo fora da pasta massa/" ;; esac
  case $CORPO in
    .kiro/specs/*/massa/* | .kiro/local/wt/*/.kiro/specs/*/massa/*) ;;
    *) erro "o corpo deve estar na pasta massa/ de uma fatia" ;;
  esac
  [ -f "$CORPO" ] || erro "corpo não encontrado: $CORPO"
  set -- "$@" -H 'Content-Type: application/json' --data-binary "@$CORPO"
fi

exec curl "$@" "$BASE$CAMINHO"
