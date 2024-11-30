#!/usr/bin/env python3
import numpy as np
from scipy.io import wavfile
import random
import sys
import subprocess  # to play the resulting wave file
import datetime  # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now
import argparse

######## CONFIG / constants ########
# fmt: off
# markBitFrequency = 2083 + 1/3
markBitFrequency = 6250 / 3
spaceBitFrequency = 1562.5
sample_rate = 43750
# fmt: on


def markBit():
    # fmt: off
    # time = 1.0 / (520 + 5/6)
    time = 6 / 3125  # seconds
    samples = np.arange(time * sample_rate) / sample_rate
    roffle = np.sin(2 * np.pi * markBitFrequency * samples)
    # fmt: on
    return roffle * 0.8


def spaceBit():
    # fmt: off
    # time = 1.0 / (520 + 5/6)
    time = 6 / 3125
    samples = np.arange(time * sample_rate) / sample_rate
    # fmt: on
    return np.sin(2 * np.pi * spaceBitFrequency * samples)


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


def main(args: argparse.Namespace = None):
    if args is None:
        # parse command-line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--playaudiolive", "-pal", action="store_true")
        parser.add_argument("--code", "-c", required=True)
        parser.add_argument("--output", "-o", default="same.wav")
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

    # Convert the signal from floating-point values to 16-bit samples
    signal *= 32767
    signal = np.int16(signal)

    wavfile.write(str(args.output), sample_rate, signal)

    if args.playaudiolive:
        subprocess.call(["aplay", args.output])


if __name__ == "__main__":
    main()
