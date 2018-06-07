from pythonforandroid.recipe import CythonRecipe


class XevanHashRecipe(CythonRecipe):

    url = 'https://files.pythonhosted.org/packages/e3/a9/6e74bab6b3bc97e5f68f8c1fbc9a4e4ad1617ba167fa004511b1f9288c64/xevan_hash-0.2.3.tar.gz'
    md5sum = 'ff2b5a650fbcd718109137da372c99aa'
    version = '0.2.3'
    depends = ['python3crystax']

    def should_build(self, arch):
        """It's faster to build than check"""
        return True


recipe = XevanHashRecipe()
