#!/usr/bin/env perl
## zoug.me
# encoder for hiding files in PNGs (inshack)
use autodie;
use strict;
use warnings;
use String::CRC32;
use 5.010;

# open the files if specified, otherwise print usage
die "Usage: ./encoder.pl input.png payload output.png" unless @ARGV == 3;
open my $in, '<:raw', $ARGV[0];
open my $payload, '<:raw', $ARGV[1];
open my $out, '>:raw', $ARGV[2];
my ($data, $chunkSize, $chunkType, $chunkCRC);
my ($payloadDataCRC, $payloadCRC, $payloadLength);

# png file signature
read $in, $data, 8;
die "[ERR] Weird PNG!" unless $data eq "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a";
print $out $data;

# read all the bytes, chunk by chunk
while (read $in, $data, 8) {
    # chunk size and type
    # unpack 'N' = unsigned long network order, 'a' = string
    ($chunkSize, $chunkType) = unpack 'Na4', $data;
    print $out $data;
    say "\n\nChunk size: $chunkSize\nChuck type: $chunkType";

    # content of the chunk
    read $in, $data, $chunkSize;
    print $out $data;

    # crc
    read $in, $data, 4;
    $chunkCRC = unpack 'N', $data;
    say "CRC: $chunkCRC";
    print $out $data;

    # after the IHDR chunk, we inject the payload
    if ($chunkType eq "IHDR") {
        # first, the length of our payload
        $payloadLength = -s $ARGV[1];
        say "Injecting payload\nPayload length: $payloadLength";
        print $out (pack 'N', $payloadLength);

        # payloadDataCRC contains the type + content of the chunk
        # since that's the part we need to compute the CRC for
        $payloadDataCRC = pack 'a4', "inSa";
        print $out $payloadDataCRC;

        # we now write out the content of the payload
        # and add it to payloadDataCRC
        read $payload, $data, $payloadLength;
        $payloadDataCRC .= $data;
        print $out $data;

        # finally, we compute the CRC and write it out
        $payloadCRC = crc32($payloadDataCRC);
        say "Computed CRC: $payloadCRC";
        $data = pack 'N', $payloadCRC;
        print $out $data;
    }
}

