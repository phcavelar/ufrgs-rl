EPSILON=0.1
GAMMA=0.9
ALPHA=0.5
NOISE=0
NUM_EPISODES=25
PLAN_STEPS=5

for AGENT in "q" "d"
do
  FNAME="dynaq-grid-${AGENT}.txt"
  echo " " > ${FNAME}
  for REPEAT in {1..5}
  do
    python gridworld.py --text --quiet --agent=${AGENT} --learningRate=${ALPHA} --discount=${GAMMA} --epsilon=${EPSILON} --noise=${NOISE} --episodes=${NUM_EPISODES} --plan-steps=${PLAN_STEPS} | grep "AVERAGE RETURNS" >> ${FNAME}
  done
done





