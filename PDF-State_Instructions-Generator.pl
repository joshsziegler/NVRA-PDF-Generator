#!/usr/bin/perl
#
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
   $text        = $ARGV[2];

}else {  
     $error = "Error: Wrong number of Arguments! \n";
}

if (!$error){ 

   prFile($resultsFile); # Setup output file
    
   # Font Options - Note that some of these are overridden in
   # the multiline output function 
   blackText();
   prFont( $font );
   prFontSize ( $fontSize );

   # Convert long string to array of lines (using max width)
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
