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

# Personal Libraries
require "PDF-Multiline_Output_Functions.pl";

# Max Registration Text Width sets the maximum width in points 
# that can fit on the Registration Date column/section.  If this 
# needs to be changed, you will have to test the new width using
# prStrWidth and carefully set the below variable!
my  $maxRegTextWidth = 200; 
my  $maxRegTextLines = 10; # TODO: May need to increase this to ~20.

# Setup the font here -- see PDF:Reuse for options
my $font         = 'Times-Roman';  
my $boldFont     = 'Times-Bold'; 
my $fontSize     = 9;

# Text output options
my $lineOffset   = $fontSize + 1; # Try $fontSize + 1 or 2

my  $error;       
my  $numArgs     = $#ARGV + 1;
my  $sourceFile  = "";
my  $resultsFile = "";
my  $text        = "";
my  $stateName   = "";
my  $regDeadline = "";

# Check for minimum number of arguments.
if ($numArgs >= 5) { 
   $sourceFile  = $ARGV[0];  
   $resultsFile = $ARGV[1];
   $stateName   = $ARGV[2];
   $regDeadline = $ARGV[3];
   $text        = $ARGV[4];
}
else {  
  $error = "Error: Wrong number of Arguments! \n";
}

if (!$error) {

   prFile($resultsFile); # Setup output file.
    

   # Font Options - Note that some of these are overridden in the multiline output function.
   blackText();
   prFont( $font );
   prFontSize ( $fontSize );
   prField('State', $stateName) or print "wtf?";

   # Output the state name.
   prFontSize(11);
   prFont("Times-Bold");
   prText(419, 737, $stateName);

   prFontSize(9);
   prFont("Times-Roman");

   # Convert long string to array of lines (using max width).
   my @deadlineArray = convLineToCol ($maxRegTextWidth, $font, $fontSize, $regDeadline);
   # Output the registration deadline string (e.g. "Registration Deadline:  30 days before the election.").
   writeMultiLineStr(316, 710, $lineOffset, $font, $boldFont, \@deadlineArray);
   # Note use of \@ to pass by reference.

   # Output the state-specific requirements text.
   my @txtArray = convLineToCol ( $maxRegTextWidth, $font, $fontSize, $text);
   writeMultiLineStr(316, 650, $lineOffset, $font, $boldFont, \@txtArray); 

   # Provide the source file to use as our starting point.
   prSinglePage($sourceFile); 
   prEnd(); # Flush the buffers and save the completed PDF.
}
else {
   print $error;
}
