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


use PDF::Reuse;
use PDF::Reuse::Util;
use strict;

###
# "Converts (single) Line (of text) To (a mutiline) Column" 
#    Takes in a single string and returns an array of multiple 
#    lines with a maximum length (in points, see PDF::Reuse)
#    as requested (see argument list). 
###
sub convLineToCol{ # Convert (Single Long) Line To (Multiline) Column

   # Args: 1: max width in points 2: font 3: font size 4: String
   my $maxWidth     = @_[0];
   my $font         = @_[1];
   my $fontSize     = @_[2];
   my @words        = split(' ', @_[3]);

   # Other Variables
   my $curLineText  = "";
   my $tmpLineText  = "";
   my @lines;
   my $tmpLinePtLen = 0;

   foreach my $curWord (@words){
      # For each word, do as instructed if a flag, or add it to the line  
      # with the running array of lines
      if ($curWord eq "*NL*"){
         # When a newline flag is encountered, push the current line on
         # to the array and start a new one
         push( @lines, $curLineText);
         $curLineText = "";
         $tmpLineText = ""; 

      } elsif ($curWord eq "*S*") {
         # When a space flag is encountered, add in three spaces to the line
         
  
      }else{ # Add the word to the lines of text
         # if the next item in the word array doesn't put the cur line
         # over the max width, add it and keep going.
         $tmpLineText = "$tmpLineText $curWord";
         $tmpLinePtLen = prStrWidth( $tmpLineText, $font, $fontSize );

         if( $tmpLinePtLen <=  $maxWidth) {
            # If the new lenght is okay, save it as the "last good line"
            $curLineText = $tmpLineText;
         }else {
            # Insert new line to the begging of the line array
            push( @lines, $curLineText);
            # Start the process over with the word that didn't fit this time
            $tmpLineText = "$curWord";
         }
      }
  }
  # Because the last partial line will not be added when we run
  # fout of words, force it to added to the line array at the end
  if ($tmpLineText){
     push( @lines, $tmpLineText);
  }
      
  return @lines;
}


# Takes in a start point (X,Y Coordinates), a line offset and an array of pre-built lines
# Starts at the given coordinates, print outs one line, moves down according to the offset
# and prints the next line (continuing for each line provided). 
sub writeMultiLineStr {
   # Args- 1: Starting X Point  2: Starting Y Point 3: Line Offset 4: Regular Font 5: Bold Font 6: Line Array (Reference)
   # Take special note that the last argument must be a reference (ex \@txtArray  NOT  @txtArray)
   # Also note that bold font can only be denoted by a line-basis and has no end tag

   my $xPos       = @_[0];
   my $yPos       = @_[1];
   my $lineOffset = @_[2];
   my $normalFont = @_[3];
   my $boldFont   = @_[4]; 
   my @lineArray  = @{ $_[5] }; # De-reference this in order to use it;

   my $curFont    = $normalFont; # By default, always use normalFont

   foreach my $curLine (@lineArray){
      # Remove extra space if needed
      if( substr( $curLine,0,1) eq " ") {substr( $curLine,0,1) = "";} 

      if ( substr($curLine,0,3) eq "*B*") { # If this line is marked bold, turn bold font on
         substr( $curLine, 0, 3) = "";      # Remove the Bold markup tag   
         # Remove extra space if needed
         if( substr( $curLine,0,1) eq " ") {substr( $curLine,0,1) = "";} 
         prFont( $boldFont );
         prText( $xPos-4, $yPos , $curLine ); # Print slightly to the left 
      }else{
         prText( $xPos, $yPos , $curLine );
      }
      # Shift our Y Position down to move to the next "line"
      $yPos -= $lineOffset;
      # Reset our font back to normal
      prFont( $normalFont );
   } 
}

1;
