import _dEploid
from matplotlib import pyplot

print("Hello from dEploid")
print("add: ", _dEploid.add(3, 4))
print(_dEploid.getLibraryVertionStr())
print(_dEploid.getLassoLibraryVertionStr())
print(_dEploid.getProgramVertionStr())
print(_dEploid.getCompileTimeStr())

a = _dEploid.Vcf("lib/data/exampleData/PG0390-C.eg.vcf.gz")

a.get_vcfheader()

ref = a.get_refCount()
alt = a.get_altCount()

count_max = max(max(ref), max(alt))
pyplot.scatter(ref, alt, c=a.get_vqslod())
pyplot.xlim(0, 0.9*count_max)
pyplot.ylim(0, 0.9*count_max)
pyplot.savefig("altVsRef.png", dpi=72)
pyplot.close('all')

ret = _dEploid.mcmcChain("-vcf lib/data/testData/PG0390-C.test.vcf \
    -plaf lib/data/testData/labStrains.test.PLAF.txt \
    -o PG0390-CNopanel -noPanel")

pyplot.plot(ret.get_llk())
pyplot.savefig("llk.png", dpi=72)
pyplot.close('all')
