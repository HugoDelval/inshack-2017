#!/usr/bin/env perl
## zoug.me
# decoder for retrieving hidden files in PNGs (inshack)
use autodie;
use strict;
use warnings;
use 5.010;

# open the files if specified, otherwise print usage
die "Usage: ./decoder.pl input.png hidden_file" unless @ARGV == 2;
open my $in, '<:raw', $ARGV[0];
open my $out, '>:raw', $ARGV[1];
my ($data, $chunkSize, $chunkType);

# png file signature
read $in, $data, 8;
die "[ERR] Weird PNG!" unless $data eq "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a";

# read all the bytes, chunk by chunk, and search for an inSa chunk
CHUNK: while (read $in, $data, 8) {
    # chunk size and type
    # unpack 'N' = unsigned long network order, 'a' = string
    ($chunkSize, $chunkType) = unpack 'Na4', $data;
    # discard non inSa chunks
    if ($chunkType ne "inSa") {
        seek $in, $chunkSize+4, 1; #discard the content + crc
        next CHUNK;   
    }

    say "inSa chunk detected, writing out";
    # if it's the inSa chunk, print the content out
    read $in, $data, $chunkSize;
    print $out $data;
}

