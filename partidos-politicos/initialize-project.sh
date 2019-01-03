#!/bin/bash

# If the file data does not exist create it
if [ ! -e data ]; then
  mkdir data
  mkdir data/zip
  mkdir data/csv
fi


# Dowload zip's of all political party data
politicalparty=(avante dc dem mdb novo patri pcb pc_do_b pco pdt phs pmb pmdb pmn pode pp ppl pps pr prb pros prp prtb psb psc psd psdb psdc psl psol pstu pt pt_do_b ppt ptb ptc ptn pv rede sd)
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
       wget $url -P data/zip/
     else
       echo "${url} inexistent"
     fi
   done
done

# Extract csv's from zip
files=($(ls data/zip/))
extractbase="aplic/sead/lista_filiados/uf/"

for file in "${files[@]}"; do
  extract=${extractbase}${file/zip/csv}
  unzip -j data/zip/${file} ${extract} -d "data/csv/"
done


# Dowload the gender names data
wget https://brasil.io/dataset/genero-nomes/nomes?format=csv -O data/names_gender.csv
