import _dEploid


class Vcf(object):
    def __init__(self, args):
        self.vcf = _dEploid.Vcf(args)

    def get_altCount(self):
        """
        Returns VCF alternative allele count.
        """
        return self.vcf.get_altCount()

    def get_refCount(self):
        """
        Returns VCF reference allele count.
        """
        return self.vcf.get_refCount()

    def get_vcfheader(self):
        """
        Returns the VCF header as plain text.
        """
        return self.vcf.get_vcfheader()

    def get_vqslod(self):
        """
        Returns VCF SNP VQSLOD scores.
        """
        return self.vcf.get_vqslod()
