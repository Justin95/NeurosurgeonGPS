# NeurosurgeonGPS
A tool to allow neurosurgeons to look into a patient's brain.


  Currently we have a system to write json files describing the positional relationship between different brain parts,
and linking neurolex entries to vtk 3D model files, and we have a script the runs a server allowing for web based
access to these json entries. It is worth noting that this repository does not contain the json entries, it is intended
to generate the json entries using the script in this repository, the neurolex files, and the vtk files. This is because
the json generator is not perfect and improvements to its accuracy can still be made thereby we don't want to commit to
any exact set of json entries yet.

  For the future cooperation with OBART (http://qnl.bu.edu/obart/region/AAL/15/CB/CYTO/HO/ICBM/LPBA/TALc/TALg/TG/AAL/ICBM/)
would be benificial. The end goal is a tool that highlights anotomical landmarks in an ontology to give a surgeon a map of
the surgery. In laymans terms it needs to show what parts of the head/brain will be in the way of a surgery on a specific
part of the brain.
