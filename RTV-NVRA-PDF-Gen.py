#!/usr/bin/python

# This file is part of NVRA-PDF-Generator.
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
languages = {"English": {"abbrv": "en", "reg_deadline": "Registration Deadline: "},
  "Spanish": {"abbrv": "es", "reg_deadline": "Es reg deadline:"}} # List each language to be used.
PDF_Assembly_Dir = "PDF_Assembly_Area/" # Must end with '/'
template_PDF_Dir = "Template_PDFs/" # Must end with '/'
final_PDF_Dir = "Final_PDFs/" # Must end with '/'
state_Data_Dir = "State_Data/" # Must end with '/'
state_instructions_file = "widget-state-instructions.xml"
 
### Beginning of heavy lifting -- do not edit below here!
state_instructions = xml.dom.minidom.parse(state_Data_Dir + state_instructions_file)
print "Loaded state instructions file:", state_instructions_file

states_completed = 0
 
# For each State (node) create the appropriate NVRA PDF.
for state in state_instructions.getElementsByTagName("row"):
  
  # Skip state nodes that don't define the state name.
  if state.getElementsByTagName("state")[0].hasChildNodes() == 0:
    continue
 
  ### Begin reading in the state's information.
  name = state.getElementsByTagName("state")[0].firstChild.data
  lang = state.getElementsByTagName("language")[0].firstChild.data
  nvra_support = int(state.getElementsByTagName("nvra_support")[0].firstChild.data)
  print "Processing", name, "in", lang,
  if nvra_support == 0:
    print "-- does not support NVRA; stopping processing."
    continue

  # Get the language's abbreviation from the translation table.
  language = languages[lang]["abbrv"];

  # Load additional data for the state.
  regDeadline = state.getElementsByTagName("deadline")[0].firstChild.data
  abbrv = state.getElementsByTagName("state_abbr")[0].firstChild.data
  address = state.getElementsByTagName("sos_address")[0].firstChild.data
  requirements = state.getElementsByTagName("requirements")[0].firstChild.data
 
  # Read in and assemble address lines 1-4 for the mailer
  # generator script (save as double-quote delimited arguments)
  addressArgs = '"' + '" "'.join(address.split("<br>")) + '"'
   
  ### Begin the actual PDF generation.
  
  # Set PDF page paths.
  newCoverPath = PDF_Assembly_Dir + abbrv + "-Cover-" + language + ".pdf"
  newMailerPath = PDF_Assembly_Dir + abbrv + "-Mailer-" + language + ".pdf"
  coverTemplate = template_PDF_Dir + "Cover-Template-" + language + ".pdf"
  mailerTemplate = template_PDF_Dir + "Mailer-Template-" + language + ".pdf"
  regFormTemplate = template_PDF_Dir + "Reg_Form-Template-" + language + ".pdf"
  instrTempl_pg1 = template_PDF_Dir + "Instructions-PG1-Template-" + language + ".pdf"
  instrTempl_pg2 = template_PDF_Dir + "Instructions-PG2-Template-" + language + ".pdf"
  newInstruc_pg2 = PDF_Assembly_Dir + abbrv + "-Instructions-pg2-" + language + ".pdf"
  finalPDF_Path = final_PDF_Dir + abbrv + "-NVRA-" + language + ".pdf"
 
  # Generate Cover PDF (uses an external Perl script).
  cmd = "perl PDF-Cover-Generator.pl " + coverTemplate + " " + newCoverPath
  cmd += " \"" + regDeadline + "\" " + addressArgs
  cP = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 
  # Generate Mailer PDF (uses an external Perl script).
  cmd = "perl PDF-Mailer-Generator.pl " + mailerTemplate + " " + newMailerPath + " " + addressArgs
  mP = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 
  # Generate State-Specific Instructions (uses an external Perl script).
  cmd = "perl PDF-State_Instructions-Generator.pl " + instrTempl_pg2 + " " + newInstruc_pg2 + ' "' + name + '" '
  cmd += '"' + languages[lang]["reg_deadline"] + regDeadline + '" "' + requirements + '"' 
  iP = subprocess.Popen(cmd, shell=True)
 
  # Wait for each PDF creator script to exit before trying to combine them all.
  cP.wait() # Cover Process.
  print ".",
  mP.wait() # Mailer Process.
  print ".",
  iP.wait() # State-Specific Instructions Page Process.
  print ".",
     
  # Combine all of the pages together to form the completed PDF.
  cmd = "pdftk " + newCoverPath + " " + regFormTemplate + " " + newMailerPath + " " + instrTempl_pg1
  cmd += " " + newInstruc_pg2 + " cat output " + " " + finalPDF_Path
  p = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE)
  p.wait() # Wait until the subprocess completes.
  print ".",
     
    
  # Delete all temporary PDF's.
  cmd = "rm " + newCoverPath + "; rm " + newMailerPath + "; rm " + newInstruc_pg2 + "; "
  p = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE) 
  print "done."
  states_completed += 1

print "Finished processing", states_completed, "states."
