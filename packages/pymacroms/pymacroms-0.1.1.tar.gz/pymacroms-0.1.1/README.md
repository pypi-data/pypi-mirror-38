# pyMacroMS
##### _High performance quantification of complex high resolution polymer mass spectra_

The purpose of this program is to identify and quantify macromolecular species 
in high resolution mass spectra based on the used monomer(s), possible end-groups 
and the adduct ion. Experimental spectra are imported as a centroided peaklist
from a comma-separated values (csv) file. Please find code for example usage
 on our [webpage](http://macroarc.org/research/pymacroms.html).

##### Dependencies

pyMacroMS requires the following modules to be installed:
* [IsoSpecPy](http://matteolacki.github.io/IsoSpec/) for the generation of isotopic patterns
* numpy and pandas for data processing
* sklearn for quantification via linear regression
* matplotlib for quick representation of results
* progressbar2 for feedback during the more time consuming steps 

##### Citation

Please refer to our publication for more details about the algorithm and 
cite us when using pyMacroMS in your work:

K. De Bruycker, T. Krappitz, C. Barner-Kowollik, _ACS Macro Lett._ **2018**. [DOI: 10.1021/acsmacrolett.8b00804](http://dx.doi.org/10.1021/acsmacrolett.8b00804)

##### License

pyMacroMS is available free of charge under a GNU General Public License v3.0. 
See the LICENCE file for more details.

##### Changelog

###### 0.1.1
* Minor fixes to the interfacing with IsoSpecPy
* Fixed compatibility with IsoSpecPy >= 1.9.X

###### 0.1.0
* Initial release



