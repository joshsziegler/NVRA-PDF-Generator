#!/usr/bin/perl
#
# See below for information about argument order and usage!

use PDF::Reuse;
use PDF::Reuse::Util;
use strict;
use Switch;

my  $error;       
my  $numArgs     = $#ARGV + 1;
my  $resultsFile = " "; 
my  $sourceFile  = " "; 
my  $lineOne     = " "; 
my  $lineTwo     = " "; 
my  $lineThree   = " "; 
my  $lineFour    = " ";

# Check for minimum number of arguments 
if ($numArgs >= 2) { 
   $sourceFile  = $ARGV[0];  
   $resultsFile = $ARGV[1];
   # Address lines 1-4 are optional, leave as default if not present
   if ($numArgs >= 4) { $lineOne   = $ARGV[3]; }
   if ($numArgs >= 5) { $lineTwo   = $ARGV[4]; }
   if ($numArgs >= 5) { $lineThree = $ARGV[4]; }
   if ($numArgs == 6) { $lineFour  = $ARGV[5]; }

}else {  
     $error = "Error: Wrong number of Arguments! \n";
     $error += "\n";
     $error += "Options are (in order): \n";
     $error += "   1. Source File Path \n";
     $error += "   2. Results File Path \n";
     $error += "   3. Line 1 of the Address (Optional) \n";
     $error += "   4. Line 2 of the Address (Optional) \n";
     $error += "   5. Line 3 of the Address (Optional) \n";
     $error += "   6. Line 4 of the Address (Optional) \n";
     $error += " \n\n";
}

if (!$error){ # If there were no errors execute the main program block
   print $resultsFile;
   prFile($resultsFile); # Setup output file
    
   # Setup the font here -- see PDF:Reuse for options
   blackText();

   # Write out the address lines on the mailer PDF
   prText( 120, 160 , $lineOne);    # 1st Address Line
   prText( 120, 132 , $lineTwo);    # 2nd Address Line
   prText( 120, 103,  $lineThree);  # 3rd Address Line
   prText( 120, 75,   $lineFour);   # 4th Address Line

   # Provide the source file to use as our starting point
   prSinglePage($sourceFile); 
   prEnd; # Flush the buffers and save the completed PDF
}else {
   print $error;
}
