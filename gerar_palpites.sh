#!/bin/bash

# 1. PEGAR DATA E DIA
HORA=$(date -u -d "3 hours ago" +"%H")
if [ "$HORA" -ge 21 ]; then
    DATA=$(date -d "21 hours" +"%d/%m/%Y")
    DIA=$(date -d "21 hours" +"%d")
else
    DATA=$(date -u -d "3 hours ago" +"%d/%m/%Y")
    DIA=$(date -u -d "3 hours ago" +"%d")
fi

# 2. CAPTURAR RESULTADOS
CONTEUDO=$(curl -sL "https://resultadosdojogo.com/resultado-pt-rio-de-hoje")

# 3. TABELA COMPLETA (Bicho|Dezena|Centena|Milhar)
get_all_data() {
  case $1 in
    01) echo "01 - AVESTRUZ 🦩|01 - 04|601 - 704|${DIA}01 - ${DIA}04" ;;
    02) echo "02 - ÁGUIA 🦅|05 - 08|105 - 208|${DIA}05 - ${DIA}08" ;;
    03) echo "03 - BURRO 🫏|09 - 12|309 - 412|${DIA}09 - ${DIA}12" ;;
    04) echo "04 - BORBOLETA 🦋|13 - 16|413 - 516|${DIA}13 - ${DIA}16" ;;
    05) echo "05 - CACHORRO 🐕|17 - 20|217 - 320|${DIA}17 - ${DIA}20" ;;
    06) echo "06 - CABRA 🐐|21 - 24|121 - 224|${DIA}21 - ${DIA}24" ;;
    07) echo "07 - CARNEIRO 🐏|25 - 28|125 - 228|${DIA}25 - ${DIA}28" ;;
    08) echo "08 - CAMELO 🐪|29 - 32|129 - 232|${DIA}29 - ${DIA}32" ;;
    09) echo "09 - COBRA 🐍|33 - 36|333 - 436|${DIA}33 - ${DIA}36" ;;
    10) echo "10 - COELHO 🐰|37 - 40|437 - 540|${DIA}37 - ${DIA}40" ;;
    11) echo "11 - CAVALO 🐎|41 - 44|541 - 644|${DIA}41 - ${DIA}44" ;;
    12) echo "12 - ELEFANTE 🐘|45 - 48|745 - 848|${DIA}45 - ${DIA}48" ;;
    13) echo "13 - GALO 🐓|49 - 52|749 - 852|${DIA}49 - ${DIA}52" ;;
    14) echo "14 - GATO 🐈|53 - 56|553 - 656|${DIA}53 - ${DIA}56" ;;
    15) echo "15 - JACARÉ 🐊|57 - 60|657 - 760|${DIA}57 - ${DIA}60" ;;
    16) echo "16 - LEÃO 🦁|61 - 64|761 - 864|${DIA}61 - ${DIA}64" ;;
    17) echo "17 - MACACO 🐒|65 - 68|265 - 368|${DIA}65 - ${DIA}68" ;;
    18) echo "18 - PORCO 🐷|69 - 72|669 - 772|${DIA}69 - ${DIA}72" ;;
    19) echo "19 - PAVÃO 🦚|73 - 76|373 - 476|${DIA}73 - ${DIA}76" ;;
    20) echo "20 - PERU 🦃|77 - 80|877 - 980|${DIA}77 - ${DIA}80" ;;
    21) echo "21 - TOURO 🐂|81 - 84|481 - 584|${DIA}81 - ${DIA}84" ;;
    22) echo "22 - TIGRE 🐅|85 - 88|885 - 988|${DIA}85 - ${DIA}88" ;;
    23) echo "23 - URSO 🐻|89 - 92|889 - 992|${DIA}89 - ${DIA}92" ;;
    24) echo "24 - VEADO 🦌|93 - 96|193 - 296|${DIA}93 - ${DIA}96" ;;
    25) echo "25 - VACA 🐄|97 - 00|997 - 000|${DIA}97 - ${DIA}00" ;;
  esac
}

get_puxada_id() {
  case $1 in
    "01") echo "25" ;; "02") echo "10" ;; "03") echo "11" ;; "04") echo "06" ;; "05") echo "13" ;;
    "06") echo "07" ;; "07") echo "06" ;; "08") echo "05" ;; "09") echo "15" ;; "10") echo "07" ;;
    "11") echo "03" ;; "12") echo "06" ;; "13") echo "05" ;; "14") echo "05" ;; "15") echo "09" ;;
    "16") echo "12" ;; "17") echo "05" ;; "18") echo "09" ;; "19") echo "01" ;; "20") echo "01" ;;
    "21") echo "25" ;; "22") echo "14" ;; "23") echo "16" ;; "24") echo "20" ;; "25") echo "21" ;;
    *) echo "14" ;;
  esac
}

# EXTRAÇÃO E LOGICA ANTI-REPETIÇÃO
G_SITES=$(echo "$CONTEUDO" | grep -oE "Grupo [0-9]{2}" | awk '{print $2}' | head -n 5)
LISTA_RAW=""
for g in $G_SITES; do LISTA_RAW+="$(get_puxada_id "$g") "; done
LISTA_RAW+="21 22 14 01 05 15 16 09 10 11 12"
FINAL_IDS=$(echo $LISTA_RAW | tr ' ' '\n' | awk '!x[$0]++' | head -n 6)

# EXPORTAR VARIÁVEIS PARA O GITHUB
echo "DATA=$DATA" >> $GITHUB_ENV
echo "DIA=$DIA" >> $GITHUB_ENV

i=1
for id in $FINAL_IDS; do
    IFS='|' read -r b d c m <<< "$(get_all_data "$id")"
    echo "B$i=$b" >> $GITHUB_ENV
    echo "D$i=$d" >> $GITHUB_ENV
    echo "C$i=$c" >> $GITHUB_ENV
    echo "M$i=$m" >> $GITHUB_ENV
    i=$((i+1))
done
