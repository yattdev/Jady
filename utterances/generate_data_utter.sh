# TODO: 'intents' should be give like argument
# $1: first arg = dir path for file.txt
for n in $(seq 1 $#); do
    for i in $1/*.txt; do
        python -m chatette $i
        echo "Create ../jady/data/"$1" if not exist"
        mkdir -p ../jady/data/$1
        echo "coping output/train/output.json to ../jady/data/"$i".json"
        cp output/train/output.json ../jady/data/$i.json
        echo "DONE SUCCESSFULL\n"
    done
  shift
done
