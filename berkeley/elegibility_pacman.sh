echo " " > "sarsa_pacman.txt"
for LAMBDA in 0 0.1 0.3 0.5 0.7 0.9 1.0
do
  echo "lambda=${LAMBDA}"
  echo "lambda=${LAMBDA}" >> "sarsa_pacman.txt"
  python2 pacman.py -p PacmanSarsaAgent -x 2000 -n 2010 -l smallGrid -a lamda=${LAMBDA} >> "sarsa_pacman.txt"
  echo " " >> "sarsa_pacman.txt"
  echo " " >> "sarsa_pacman.txt"
done





