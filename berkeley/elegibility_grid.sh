for ACT in 0 0.2
do
  for LAMBDA in 0 0.1 0.3 0.5 0.7 0.9 1.0
  do
    echo " " > "${ACT}-${LAMBDA}.txt"
    for REPEAT in {1..5}
    do
      python gridworld.py -t -q -a s -l 0.5 -d 0.9 -e 0.1 -n ${ACT} -r -0.04 -k 10 --lambda=${LAMBDA} | grep "AVERAGE RETURNS" >> "${ACT}-${LAMBDA}.txt"
    done
  done
done





