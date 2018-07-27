#!/bin/bash

function validate_url(){
  if [[ `wget -S --spider $1  2>&1 | grep 'HTTP/1.1 200 OK'` ]]; then echo "true"; fi
}

# Dowload zip's
politicalparty=(avante dc dem mdb novo patri pcb pc_do_b pco pdt phs pmb pmdb pmn pode pp ppl pps pr prb pros prp prtb psb psc psd psdb psdc psl psol pstu pt pt_do_b ppt ptb ptc ptn pv rede sd)
states=(ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn rs ro rr sc sp se to)
baseurl="http://agencia.tse.jus.br/estatistica/sead/eleitorado/filiados/uf/filiados_"

for st in "${states[@]}"; do
	for pol in "${politicalparty[@]}"; do
		url=${baseurl}${pol}_${st}.zip
		if `validate_url $url > /dev/null`; then
	 		wget $url -P zip/ 
		else 
			echo "${url} inexistent"
		fi
	done
done


# Extract csv's from zip
files=($(ls zip/))
extractbase="aplic/sead/lista_filiados/uf/"

for file in "${files[@]}"; do
	extract=${extractbase}${file/zip/csv}
	unzip -j zip/${file} ${extract} -d "csv/"
done