#!/usr/bin/perl

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

# See below for information about argument order and usage!

use PDF::Reuse;
use PDF::Reuse::Util;
use strict;
use Switch;

# Helper Functions/Libraries
do "PDF-Multiline_Output_Functions.pl";

my  $error;       
my  $numArgs     = $#ARGV + 1;

if ($numArgs == 21) { 
   # Arguments Note: All must be passed, but any of the text and its coordinates
   # can be ignored by providing an empty string ""  

   my $sourceFile    = $ARGV[0]; # Template/Background to start with 
   my $resultsFile   = $ARGV[1]; # File to save results to
 
   my $fontSize      = $ARGV[2];
   my $regularFont   = $ARGV[3]; 
   my $boldFont      = $ARGV[4];
   
   my $lineOffset    = $fontSize + 1; # Try $fontSize + 1 or 2

   my $multilineTxt  = $ARGV[5]; # String to be made into multi-line column
   my $maxMuLiTxtWd  = $ARGV[6]; # "Maximum Multi-Line Text Width" (Size of Column) 
   my $multilineXpos = $ARGV[7]; # X Position to print this text at
   my $multilineYpos = $ARGV[8]; # Y Position to print this text at

   my $lineOne       = $ARGV[9]; # Single line of text to be printed as is 
   my $liOneXpos     = $ARGV[10]; # X Position to print this text at
   my $liOneYpos     = $ARGV[11]; # Y Position to print this text at

   my $lineTwo       = $ARGV[12]; 
   my $liTwoXpos     = $ARGV[13];
   my $liTwoYpos     = $ARGV[14];

   my $lineThree     = $ARGV[15];
   my $liThreeXpos   = $ARGV[16];
   my $liThreeYpos   = $ARGV[17];

   my $lineFour      = $ARGV[18]; 
   my $liFourXpos    = $ARGV[19];
   my $liFourYpos    = $ARGV[20];
   }
}else {  
     $error = "Error: Wrong number of Arguments! Please see the script for the current argument requirements. \n";
}

### Begin main program block

if (!$error){ 
   prFile($resultsFile); # Setup output file
    
   # Font Options - Note that some of these are overridden in
   # the multiline output function 
   blackText();
   prFont( $regularFont );
   prFontSize ( $fontSize );

   # Write out the single text lines on the PDF if given
   if ($lineOne  ){ prText( $liOneXpos,   $liOneYpos,   $lineOne);  } # 370,550
   if ($lineTwo  ){ prText( $liTwoXpos,   $liTwoYpos,   $lineTwo);  } # 370,535
   if ($lineThree){ prText( $liThreeXpos, $liThreeYpos, $lineThree);} # 370,520
   if ($lineFour ){ prText( $liFourXpos,  $liFourYpos,  $lineFour); } # 370,505

   if ( $multilineTxt ) { # If a long text block was provided, divide it into lines, then print it 
      # Divide the long string into multiple lines with a certain max width  
      my @txtLinesArray = convLineToCol ( $maxMuLiTxtWd, $regularFont, $fontSize, $multilineTxt);

      # Note that txtArray is being passed by reference!
      writeMultiLineStr( multilineXpos, multilineYpos, $lineOffset, $regularFont, $boldFont, \@txtLinesArray); # 370,450 
   }

   # Provide the source file to use as our starting point
   prSinglePage($sourceFile); 
   prEnd; # Flush the buffers and save the completed PDF

}else {
   print $error;
}
