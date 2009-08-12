#!/usr/bin/perl

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


# See below for information about argument order and usage!

use PDF::Reuse;
use PDF::Reuse::Util;
use strict;
use Switch;

# Personal Libraries
do "PDF-Multiline_Output_Functions.pl";

# Max Registration Text Width sets the maximum width in points 
# that can fit on the Registration Date column/section.  If this 
# needs to be changed, you will have to test the new width using
# prStrWidth and carefully set the below variable!
my  $maxRegTextWidth = 200; 
my  $maxRegTextLines = 10; 

#Setup the font here -- see PDF:Reuse for options
my $font         = 'H';  # Helvetica
my $boldFont     = 'HB'; # Helvetica-Bold
my $fontSize     = 12;

# Text output options
my $lineOffset   = $fontSize + 1; # Try $fontSize + 1 or 2

my  $error;       
my  $numArgs     = $#ARGV + 1;
my  $resultsFile = " "; 
my  $sourceFile  = " "; 
my  $regDeadline = " ";
my  $lineOne     = " "; 
my  $lineTwo     = " "; 
my  $lineThree   = " "; 
my  $lineFour    = " ";

# Check for minimum number of arguments 
if ($numArgs >= 3) { 
   $sourceFile  = $ARGV[0];  
   $resultsFile = $ARGV[1];
   $regDeadline = $ARGV[2];
   # Address lines 1-4 are optional, leave as default if not present 
   if ($numArgs >= 4) { $lineOne   = $ARGV[3]; }
   if ($numArgs >= 5) { $lineTwo   = $ARGV[4]; }
   if ($numArgs >= 6) { $lineThree = $ARGV[5]; }
   if ($numArgs == 7) { $lineFour  = $ARGV[6]; }

}else {  
     $error = "Error: Wrong number of Arguments! \n";
     $error += "\n";
     $error += "Options are (in order): \n";
     $error += "   1. Source File Path \n";
     $error += "   2. Results File Path \n";
     $error += "   3. Registration Deadline \n";
     $error += "   4. Line 1 of the Address (Optional) \n";
     $error += "   5. Line 2 of the Address (Optional) \n";
     $error += "   6. Line 3 of the Address (Optional) \n";
     $error += "   7. Line 4 of the Address (Optional) \n";
     $error += " \n\n";
}

if (!$error){ # If there were no errors execute the main program block
   prFile($resultsFile); # Setup output file
    
   # Font Options - Note that some of these are overridden in
   # the multiline output function 
   blackText();
   prFont( $font );
   prFontSize ( $fontSize );

   # Use function to take care of multi-line Reg dates 
   # Waring: may overrun space provided 
   my @txtArray = convLineToCol ( $maxRegTextWidth, $font, $fontSize, $regDeadline);

   # Note that txtArray is being passed by reference!
   writeMultiLineStr( 370, 450, $lineOffset, $font, $boldFont, \@txtArray); 

   # Write out the address lines on the PDF
   prText( 370, 550, $lineOne);    # 1st Address Line
   prText( 370, 535, $lineTwo);    # 2nd Address Line
   prText( 370, 520, $lineThree);  # 3rd Address Line
   prText( 370, 505, $lineFour);   # 4th Address Line

   # Provide the source file to use as our starting point
   prSinglePage($sourceFile); 
   prEnd; # Flush the buffers and save the completed PDF
}else {
   print $error;
}
