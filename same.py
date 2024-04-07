#!/usr/bin/env python3
import numpy as np
from scipy.io import wavfile
import random
import sys
import subprocess  # to play the resulting wave file
import datetime  # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now
import argparse

######## CONFIG / constants ########
markBitFrequency = 2083 + 1/3
spaceBitFrequency = 1562.5
fs = 43750


def markBit():
    global markBitFrequency

    # f = 2083.33333
    f = markBitFrequency
    t = 1.0 / (520 + 5/6)

    samples = np.arange(t * fs) / fs

    roffle = np.sin(2 * np.pi * f * samples)
    return roffle * 0.8


def spaceBit():
    global spaceBitFrequency

    # f = 1562.5
    f = spaceBitFrequency
    t = 1.0 / (520 + 5/6)

    samples = np.arange(t * fs) / fs

    return np.sin(2 * np.pi * f * samples)


def byte(the_byte):
    sys.stdout.write(the_byte)
    sys.stdout.write(" ")
    byte_data = np.zeros(0)
    for i in range(0, 8):
        if ord(the_byte) >> i & 1:
            sys.stdout.write("1")
            byte_data = np.append(byte_data, markBit())
        else:
            sys.stdout.write("0")
            byte_data = np.append(byte_data, spaceBit())

    sys.stdout.write("\n")
    sys.stdout.flush()

    return byte_data


def extramarks(numberOfMarks):
    """SAGE encoders seem to add a few mark bits at the beginning and end"""
    byte_data = np.zeros(0)

    for i in range(0, numberOfMarks):
        byte_data = np.append(byte_data, markBit())

    return byte_data


def preamble():
    byte_data = np.zeros(0)

    for i in range(0, 16):
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, spaceBit())
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, spaceBit())
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, spaceBit())
        byte_data = np.append(byte_data, markBit())

    return byte_data

# control string
# code = "ZCZC-EAS-RMT-011001+0100-2142200-KMMS FM -"
# useful FIPS codes
# 000000 - the whole fucking united states
# 024031 - silver spring, md / montgomery county
# 011001 - district of columbia
# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
# sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")


def main():
    # parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--playaudiolive", "-pal", nargs='?', default=0)
    parser.add_argument("--code", "-c", nargs='?', default="none")
    parser.add_argument("--output", "-o", nargs='?', default="same.wav")
    args = parser.parse_args()
    code = args.code
    samples = np.zeros(0)
    signal = np.zeros(20000)
    # print(args)

    for i in range(0, 3):
        # signal = np.append(signal, extramarks(10))
        signal = np.append(signal, preamble())

        # turn each character into a sequence of sine waves
        for char in code:
            signal = np.append(signal, byte(char))

        # signal = np.append(signal, extramarks(6)) # ENDEC might not be as picky about this as I once thought

        # wait the requisite one second
        signal = np.append(signal, np.zeros(43750))

    # EOM (3x)
    for i in range(0, 3):
        # signal = np.append(signal, extramarks(10))
        signal = np.append(signal, preamble())

        for char in "NNNN":  # NNNN = End Of Message
            signal = np.append(signal, byte(char))

        # signal = np.append(signal, extramarks(6))

        # wait the requisite one second
        signal = np.append(signal, np.zeros(43750))

    signal *= 32767

    signal = np.int16(signal)

    wavfile.write(str(args.output), fs, signal)

    if args.playaudiolive:
        subprocess.call(["aplay", args.output])


if __name__ == "__main__":
    main()
