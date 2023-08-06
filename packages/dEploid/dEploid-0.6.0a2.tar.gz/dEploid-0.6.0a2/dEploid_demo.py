import dEploid
from matplotlib import pyplot

ret = dEploid.mcmc.chain("-vcf lib/data/testData/PG0390-C.test.vcf \
    -plaf lib/data/testData/labStrains.test.PLAF.txt \
    -o PG0390-CNopanel -noPanel")

pyplot.plot(ret.get_llk())
pyplot.savefig("llk.png", dpi=72)
pyplot.close('all')
