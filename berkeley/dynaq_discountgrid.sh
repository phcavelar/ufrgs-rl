EPSILON=0.1
GAMMA=0.9
ALPHA=0.5
NOISE=0
NUM_EPISODES=50
AGENT=d

for KAPPA in 0 0.1 0.5
do
  echo ${KAPPA}
  for PLAN_STEPS in {5..50..5}
  do
    echo ${PLAN_STEPS}
    FNAME="dynaq-discountgrid-${KAPPA}-${PLAN_STEPS}.txt"
    echo " " > ${FNAME}
    for REPEAT in {1..5}
    do
      python gridworld.py -g DiscountGrid --text --quiet --agent=${AGENT} --learningRate=${ALPHA} --discount=${GAMMA} --epsilon=${EPSILON} --noise=${NOISE} --episodes=${NUM_EPISODES} --kappa=${KAPPA} --plan-steps=${PLAN_STEPS} | grep "AVERAGE RETURNS" >> ${FNAME}
    done
  done
done





