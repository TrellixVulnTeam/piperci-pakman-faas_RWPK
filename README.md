# piedpiper-pakman-faas
Function for packaging up various artifacts into a single archive for storage and/or delivery.
# make sure to insall
  pip3 install PyYAML
# how to run
  python isoimage.py sample.yml  
# add these sample directory for testing these are not needed.
  artifacts
  logs
# the output looks similar to this for this sample
#Statred Processing :sample.yml
#Image name: customer.iso
#Image type: iso
#unarchive the files to destination: target/src
#unarchive the files to destination: target/docs
#Generating Iso image mkisofs  -V CDNAME -J -r -o customer.iso target
#Using RECEI000.PDF;1 for  target/docs/Receipt for Flight to New Orleans.pdf (Receipt for Raleigh.pdf)
#Using ITINE000.PDF;1 for  target/docs/Itinerary_ Flight to New Orleans.pdf (Itinerary_ Raleigh.pdf)
#Using __ITI000.PDF;1 for  target/docs/__MACOSX/._Itinerary_ Flight to New Orleans.pdf (._Itinerary_ Raleigh.pdf)
#Using __REC000.PDF;1 for  target/docs/__MACOSX/._Receipt for Raleigh.pdf (._Receipt for Flight to New Orleans.pdf)
#Using __CER000.PDF;1 for  target/src/test_tar/._Certificate (1).pdf (._Certificate.pdf)
#Using CERTI000.PDF;1 for  target/src/test_tar/Certificate (1).pdf (Certificate (2).pdf)
#Using CERTI001.PDF;1 for  target/src/test_tar/Certificate (2).pdf (Certificate.pdf)
#Using __CER001.PDF;1 for  target/src/test_tar/._Certificate.pdf (._Certificate (2).pdf)
#Using __CER002.PDF;1 for  target/src/test_tar/._Certificate (2).pdf (._Certificate (3).pdf)
#Using CERTI002.PDF;1 for  target/src/test_tar/Certificate.pdf (Certificate (3).pdf)
# 84.79% done, estimate finish Wed May 29 09:25:30 2019
#Total translation table size: 0
#Total rockridge attributes bytes: 4006
#Total directory bytes: 14336
#Path table size(bytes): 102
#Max brk space used 0
#5916 extents written (11 MB)

 
