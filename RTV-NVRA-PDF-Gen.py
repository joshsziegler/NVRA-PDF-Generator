#!/usr/bin/python

#This file is part of NVRA-PDF-Generator .
#
#    NVRA-PDF-Generator is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NVRA-PDF-Generator is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NVRA-PDF-Generator .  If not, see <http://www.gnu.org/licenses/>.
 
import os, subprocess
import xml.dom.minidom
from xml.dom.minidom import Node
 
### Naming Conventions Used:
# Templates:
# <PDF_Page>-Template-<Language_Abbreviation>.pdf
# Resulting PDFs::
# <State Abbreviation>-NRVA-<Language_Abbreviation>.pdf
 
# Script variables
language_versions = ["en", "es"] # List each language (abbreviation) to be used
PDF_Assembly_Dir = "PDF_Assembly_Area/" # Must end with '/'
template_PDF_Dir = "Template_PDFs/" # Must end with '/'
final_PDF_Dir = "Final_PDFs/" # Must end with '/'
state_Data_Dir = "State_Data/" # Must end with '/'
state_instructions_file = "widget-state-instructions.xml"
 
### Beginning of heavy lifting -- do not edit below here!
#basicStateInfo = xml.dom.minidom.parse(state_Data_Dir + basic_State_Data)
#stateSpecInstr = xml.dom.minidom.parse(state_Data_Dir + state_Spec_Instr)
state_instructions = xml.dom.minidom.parse(state_Data_Dir + state_instructions_file)

 
# For each State (node) create the appropriate NVRA PDF
for state in state_instructions.getElementsByTagName("row"):

  if state.getElementsByTagName("state")[0].hasChildNodes() == 0:
    continue
 
  ### Begin reading in the state's information
  name = state.getElementsByTagName("state")[0].firstChild.data
  lang = state.getElementsByTagName("language")[0].firstChild.data
  nvra_support = int(state.getElementsByTagName("nvra_support")[0].firstChild.data)
  print "Processing", name, "in", lang, "...",
  if nvra_support == 0:
    print "does not support NVRA, stopping processing."
    continue

  lang_translation = {"English" : "en", "Spanish": "es"}
  language = lang_translation[lang]

  regDeadline = state.getElementsByTagName("deadline")[0].firstChild.data
  abbrv = state.getElementsByTagName("state_abbr")[0].firstChild.data
  address = state.getElementsByTagName("sos_address")[0].firstChild.data
  requirements = state.getElementsByTagName("requirements")[0].firstChild.data
 
  # Read in and assemble address lines 1-4 for the mailer
  # generator script (save as double-quote delimited arguments)
  addressArgs = '"' + '" "'.join(address.split("<br>")) + '"'
   
  ### Begin the actual PDF generation
  
  # Set PDF page paths
  newCoverPath = PDF_Assembly_Dir + abbrv + "-Cover-" + language + ".pdf"
  newMailerPath = PDF_Assembly_Dir + abbrv + "-Mailer-" + language + ".pdf"
  coverTemplate = template_PDF_Dir + "Cover-Template-" + language + ".pdf"
  mailerTemplate = template_PDF_Dir + "Mailer-Template-" + language + ".pdf"
  regFormTemplate = template_PDF_Dir + "Reg_Form-Template-" + language + ".pdf"
  instrTempl_pg1 = template_PDF_Dir + "Instructions-PG1-Template-" + language + ".pdf"
  instrTempl_pg2 = template_PDF_Dir + "Instructions-PG2-Template-" + language + ".pdf"
  newInstruc_pg2 = PDF_Assembly_Dir + abbrv + "-Instructions-pg2-" + language + ".pdf"
  finalPDF_Path = final_PDF_Dir + abbrv + "-NVRA-" + language + ".pdf"
 
  # Generate Cover PDF (uses an external Perl script)
  cmd = "perl PDF-Cover-Generator.pl"
  cmd += " " + coverTemplate
  cmd += " " + newCoverPath
  cmd += " \"" + regDeadline + "\""
  cmd += " " + addressArgs
  #print "Generating cover page..."
#     print cmd
  cP = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
  # Generate Mailer PDF (uses an external Perl script)
  cmd = "perl PDF-Mailer-Generator.pl"
  cmd += " " + mailerTemplate
  cmd += " " + newMailerPath
  cmd += " " + addressArgs
  mP = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE)#, stderr=subprocess.PIPE)
  #print cmd
 
  # Generate State-Specific Instructions (uses an external Perl script)
  cmd = "perl PDF-State_Instructions-Generator.pl "
  cmd += instrTempl_pg2 + " " + newInstruc_pg2 + " "
  cmd += '"' + requirements + '"' 
  iP = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE)#, stderr=subprocess.PIPE)
  #print ""
  #print requirements
  print cmd
 
  # Wait for each PDF creator script to exit before trying to combine them all
  cP.wait() # Cover Process
  mP.wait() # Mailer Process
  iP.wait() # State-Specific Instructions Page Process
     
  # Combine all of the pages together to form the completed PDF
  cmd = "pdftk"
  cmd += " " + newCoverPath
  cmd += " " + regFormTemplate
  cmd += " " + newMailerPath
  cmd += " " + instrTempl_pg1
  cmd += " " + newInstruc_pg2
  cmd += " cat output "
  cmd += " " + finalPDF_Path
  #   print cmd
  p = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE)#, stderr=subprocess.PIPE)
  p.wait() # Wait until the subprocess completes
    
  # Delete all temporary PDF's
  cmd = "rm " + newCoverPath + "; "
  cmd += "rm " + newMailerPath + "; "
  cmd += "rm " + newInstruc_pg2 + "; "
  p = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  print "done."
