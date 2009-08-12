#!/usr/bin/python

This file is part of NVRA-PDF-Generator .

    NVRA-PDF-Generator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    NVRA-PDF-Generator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with NVRA-PDF-Generator .  If not, see <http://www.gnu.org/licenses/>.

import os, subprocess 
import xml.dom.minidom
from xml.dom.minidom import Node

### Naming Conventions Used:
# Templates:   
#        <PDF_Page>-Template-<Language_Abbreviation>.pdf
# Resulting PDFs::   
#        <State Abbreviation>-NRVA-<Language_Abbreviation>.pdf

# Script variables
language_versions = ["en", "es"] # List each language (abbreviation) to be used 
PDF_Assembly_Dir  = "PDF_Assembly_Area/" # Must end with '/'
template_PDF_Dir  = "Template_PDFs/"     # Must end with '/'
final_PDF_Dir     = "Final_PDFs/"        # Must end with '/'
state_Data_Dir    = "State_Data/"        # Must end with '/'
basic_State_Data  = "Basic_State_Info.xml"
state_Spec_Instr  = "State_Specific_Instructions.xml"

# Font-Specific Variables
regular_Font      = "H"                  # Helvetica
bold_Font         = "HB"                 # Helvetica Bold
font_Size         = 12                   

# Text Positioning Variables
cover_Xpos            = 370
cover_RegYpos         = 450
cover_addrLiOneYpos   = 550
cover_addrLiTwoYpos   = 535
cover_addrLiThreeYpos = 520
cover_addrLiFourYpos  = 505
max_ColWidth          = 200

mailer_Xpos            = 120
mailer_addrLiOneYpos   = 160
mailer_addrLiTwoYpos   = 160
mailer_addrLiThreeYpos = 160
mailer_addrLiFourYpos  = 160

### Beginning of heavy lifting -- do not edit below here!

basicStateInfo = xml.dom.minidom.parse(state_Data_Dir + basic_State_Data)
stateSpecInstr = xml.dom.minidom.parse(state_Data_Dir + state_Spec_Instr)
 
# For each State (node) create the appropriate NVRA PDF
for state in basicStateInfo.getElementsByTagName("State"):

  ###  Begin reading in the state's information 

  name  = state.getAttribute("name")
  abbrv = state.getAttribute("abbrv")
  regDeadline = state.getElementsByTagName("Reg_Deadline")[0].firstChild.data

  # Read in and assemble address lines 1-4 for the mailer 
  # generator script (save as double-quote delimited arguments) 
  addressArgs = "" 
  for subnode in state.getElementsByTagName("Addr_Line"):
     addressArgs +=  " \"" + subnode.childNodes[0].data + " \""

  ### Begin the actual PDF generation
  
  for language in language_versions:
     # Set PDF page paths
     newCoverPath    = PDF_Assembly_Dir + abbrv + "-Cover-" + language + ".pdf"
     newMailerPath   = PDF_Assembly_Dir + abbrv + "-Mailer-" + language + ".pdf"
     coverTemplate   = template_PDF_Dir + "Cover-Template-" + language + ".pdf"
     mailerTemplate  = template_PDF_Dir + "Mailer-Template-" + language + ".pdf" 
     regFormTemplate = template_PDF_Dir + "Reg_Form-Template-" + language + ".pdf"
     instrTempl_pg1  = template_PDF_Dir + "Instructions-PG1-Template-" + language + ".pdf"
     instrTempl_pg2  = template_PDF_Dir + "Instructions-PG2-Template-" + language + ".pdf"
     newInstruc_pg2  = PDF_Assembly_Dir + abbrv + "-Instructions-pg2-" + language + ".pdf"
     finalPDF_Path   = final_PDF_Dir + abbrv + "-NVRA-" + language + ".pdf"
 
     # Generate Cover PDF (uses an external Perl script)
     cmd =  "perl  PDF-Write-Hacker.pl" + coverTemplate + " " + newCoverPath + " "
     cmd += font_Size + " " + regularFont + " " + boldFont + " " 
     cmd += regDeadline + " " + max_ColWidth + " " + xpos + " " + ypos 
     cmd += " " + addressArgs 
     cP  = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
 
     # Generate Mailer PDF (uses an external Perl script)
     cmd =  "perl  PDF-Mailer-Generator.pl"
     cmd += " " + mailerTemplate 
     cmd += " " + newMailerPath
     cmd += " " + addressArgs 
     mP = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  

     # Generate 2nd Page of Instructions (State-Specific) (uses an external Perl script)
     # left blank for now

     # Wait for each PDF creator script to exit before trying to combine them all 
     cP.wait()  # Cover Process
     mP.wait()  # Mailer Process
     
     # Combine all of the pages together to form the completed PDF
     cmd =  "pdftk"
     cmd += " " + newCoverPath 
     cmd += " " + regFormTemplate
     cmd += " " + newMailerPath
     cmd += " " + instrTempl_pg1 
     # cmd += " " + newInstruc_pg2
     cmd += " cat output "
     cmd += " " + finalPDF_Path 
     p = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
     p.wait() # Wait until the subprocess completes
    
     # Delete all temporary PDF's
     cmd =  "rm " + newCoverPath + "; "
     cmd += "rm " + newMailerPath + "; "
     p = subprocess.Popen (cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
