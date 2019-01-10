#!/bin/bash

# If the file data does not exist create it
if [ ! -e data ]; then
  mkdir data
  mkdir data/affiliates
  mkdir data/affiliates/zip
  mkdir data/affiliates/csv
  mkdir data/candidates
  mkdir test_figure
fi


# Dowload zip's of all political party data
politicalparty=(avante dc dem mdb novo patri pcb pc_do_b pco pdt phs pmb pmn pode pp ppl pps pr prb pros prp prtb psb psc psd psdb psl psol pstu pt ptb ptc pv rede sd)
states=(ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn rs ro rr sc sp se to)
baseurl="http://agencia.tse.jus.br/estatistica/sead/eleitorado/filiados/uf/filiados_"

# Function to validate if the url exists
function validate_url(){
  if [[ `wget -S --spider $1  2>&1 | grep 'HTTP/1.1 200 OK'` ]]; then echo "true"; fi
}

for st in "${states[@]}"; do
  for pol in "${politicalparty[@]}"; do
	   url=${baseurl}${pol}_${st}.zip
     if `validate_url $url > /dev/null`; then
       wget $url -P data/affiliates/zip/
     else
       echo "${url} inexistent"
     fi
   done
done

# Extract csv's from zip
files=($(ls data/affiliates/zip/))
extractbase="aplic/sead/lista_filiados/uf/"

for file in "${files[@]}"; do
  extract=${extractbase}${file/zip/csv}
  unzip -j data/affiliates/zip/${file} ${extract} -d "data/affiliates/csv/"
done


# Dowload the gender names data
wget https://brasil.io/dataset/genero-nomes/nomes?format=csv -O data/names_gender.csv



# Dowload the candidates data
wget http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2018.zip -O data/candidates/candidates.zip
unzip -j data/candidates/candidates.zip consulta_cand_2018_BRASIL.csv leiame.pdf -d "data/candidates"
