#!/usr/bin/python

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
     cmd =  "perl  PDF-Cover-Generator.pl"
     cmd += " " + coverTemplate   
     cmd += " " + newCoverPath 
     cmd += " \"" + regDeadline + "\""
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
