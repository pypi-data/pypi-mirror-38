from __future__ import print_function
from setuptools import setup, find_packages
import sys
setup( name = "prapi",
        keywords = ("pip", "prapi","featureextraction"),
        escription = "Post-transcriptional regulation analysis pipeline for Iso-Seq", 
        long_description = "PRAPI is a one-stop solution for Iso-Seq analysis of analyze alternative transcription initiation (ATI), alternative splicing (AS), alternative cleavage and polyadenylation (APA), natural antisense transcripts (NAT), and circular RNAs (circRNAs) comprehensively.", license = "MIT Licence", 
        url = "http://www.bioinfor.org/tool/PRAPI/",
        author = "gaoyubang", author_email = "1489582340@qq.com",
        include_package_data = True, 
        platforms = "any", 
        install_requires = ["numpy","cairo","bx-python","scipy"]
)
