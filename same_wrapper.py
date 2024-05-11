import datetime
import io
import addfips
import same
from pathlib import Path
from argparse import Namespace

code_temp = io.StringIO("ZCZC-")
# fmt: off
events = [
    "ADR", "AVA", "AVW", "BLU", "BZW", "CAE", "CDW", "CEM", "CFA", "CFW",
    "DMO", "DSW", "EAN", "EAT", "EHW", "EQW", "EVI", "EWW", "FFA", "FFS",
    "FFW", "FLA", "FLS", "FLW", "FRW", "FSW", "FZW", "HLS", "HMW", "HUA",
    "HUW", "HWA", "HWW", "LAE", "LEW", "NAT", "NIC", "NMN", "NPT", "NST",
    "NUW", "RHW", "RFW", "RMT", "RWT", "SMW", "SPS", "SPW", "SQW", "SSA",
    "SSW", "SVA", "SVR", "SVS", "TOA", "TOE", "TOR", "TRA", "TRW", "TSA",
    "TSW", "VOW", "WSA", "WSW", "BHW", "BWW", "CHW", "CWW", "DBA", "DBW",
    "DEW", "EVA", "FCW", "IBW", "IFW", "LSW", "POS", "WFA", "WFW",
]
# fmt: on


def main():
    fips_adder = addfips.AddFIPS()
    code_temp.seek(5)
    print("Python Specific Area Message Encoding (SAME) header encoder")
    waiting = True
    while waiting:
        print(
            """Select originator
1 - United States Government (PEP)
2 - Civil Authorities (CIV)
3 - National Weather Service (WXR)
4 - EAS Participant (EAS)
5 - EAN Network (EAN; deprecated)"""
        )
        match input(""):
            case "1" | "PEP":
                to_write = "PEP-"
            case "2" | "CIV":
                to_write = "CIV-"
            case "3" | "WXR":
                to_write = "WXR-"
            case "4" | "EAS":
                to_write = "EAS-"
            case "5" | "EAN":
                to_write = "EAN-"
            case _:
                print("Please input a valid option.")
                to_write = ""
        if to_write:
            waiting = False
    code_temp.write(to_write)
    waiting = True
    while waiting:
        # fmt: off
        event = (
            input("Enter event code. For a list of event codes type L. ")
            .upper()
        )
        # fmt: on
        if event not in events:
            if event == "L":
                print(
                    """\
0 - Administrative Message (ADR)       1 - Avalanche Watch (AVA)
2 - Avalanche Warning (AVW)            3 - Blue Alert (BLU)
4 - Blizzard Warning (BZW)             5 - Child Abduction Emergency (CAE)
6 - Civil Danger Warning (CDW)         7 - Civil Emergency Message (CEM)
8 - Coastal Flood Watch (CFA)          9 - Coastal Flood Warning (CFW)
10 - Practice/Demo Warning (DMO)       11 - Dust Storm Warning (DSW)
12 - National Emergency Message (EAN)  13 - Emergency Action Termination (EAT)
14 - Excessive Heat Warning (EHW)      15 - Earthquake Warning (EQW)
16 - Evacuation Immediate (EVI)        17 - Extreme Wind Warning (EWW)
18 - Flash Flood Watch (FFA)           19 - Flash Flood Statement (FFS)
20 - Flash Flood Warning (FFW)         21 - Flood Watch (FLA)
22 - Flood Statement (FLS)             23 - Flood Warning (FLW)
24 - Fire Warning (FRW)                25 - Flash Freeze Warning (FSW)
26 - Freeze Warning (FZW)              27 - Hurricane Local Statement (HLS)
28 - Hazardous Materials Warning (HMW) 29 - Hurricane Watch (HUA)
30 - Hurricane Warning (HUW)           31 - High Wind Watch (HWA)
32 - High Wind Warning (HWW)           33 - Local Area Emergency (LAE)
34 - Law Enforcement Warning (LEW)     35 - National Audible Test (NAT)
36 - National Information Center (NIC) 37 - Network Notification Message (NMN)
38 - Nationwide Test of the Emergency  39 - National Silent Test (NST)
     Alert System (NPT)
40 - Nuclear Power Plant Warning (NUW) 41 - Radiological Hazard Warning (RHW)
42 - Red Flag Warning (RFW)            43 - Required Monthly Test (RMT)
44 - Required Weekly Test (RWT)        45 - Special Marine Warning (SMW)
46 - Special Weather Statement (SPS)   47 - Shelter In Place Warning (SPW)
48 - Snow Squall Warning (SQW)         49 - Storm Surge Watch (SSA)
50 - Storm Surge Warning (SSW)         51 - Severe Thunderstorm Watch (SVA)
52 - Severe Thunderstorm Warning (SVR) 53 - Severe Weather Statement (SVS)
54 - Tornado Watch (TOA)               55 - 911 Telephone Outage (TOE)
56 - Tornado Warning (TOR)             57 - Tropical Storm Watch (TRA)
58 - Tropical Storm Warning (TRW)      59 - Tsunami Watch (TSA)
60 - Tsunami Warning (TSW)             61 - Volcano Warning (VOW)
62 - Winter Storm Watch (WSA)          63 - Winter Storm Warning (WSW)
64 - Biological Hazard Warning (BHW)   65 - Boil Water Warning (BWW)
66 - Chemical Hazard Warning (CHW)     67 - Contaminated Water Warning (CWW)
68 - Dam Watch (DBA)                   69 - Dam Break Warning (DBW)
70 - Contagious Disease Warning (DEW)  71 - Evacuation Watch (EVA)
72 - Food Contamination Warning (FCW)  73 - Iceberg Warning (IBW)
74 - Industrial Fire Warning (IFW)     75 - Landslide Warning (LSW)
76 - Power Outage Statement (POS)      77 - Wild Fire Watch (WFA)
78 - Wild Fire Warning (WFW)"""
                )
            else:
                try:
                    e_num = int(event)
                    if e_num >= 0 and e_num <= 78:
                        event = events[e_num]
                        waiting = False
                    else:
                        print("Invalid input.")
                except ValueError:
                    print("Invalid input.")
        else:
            waiting = False
    code_temp.write(f"{event}-")
    if input("Is this alert for the entire US? (yes or no) ") in ["yes", "y"]:
        code_temp.write("000000+")
    else:
        for i in range(31):
            state = input("Enter state name or abbriviation. ")
            if state.upper() in ["DISTRICT OF COLUMBIA", "DC"]:
                do_area = False
                area = 1
                code_temp.write("011001")
                code_temp.seek(code_temp.tell() - 6)
            else:
                do_area = True
            if do_area:
                area = input(
                    "Enter county name or equivalent, or independent city. To \
select the entire state, leave this blank. "
                ).title()
                if area:
                    fips = fips_adder.get_county_fips(area, state)
                else:
                    fips = fips_adder.get_state_fips(state)
                    area = 0
                if fips is None:
                    print("Area not found.")
                    continue
                if area:
                    code_temp.write(f"0{fips}")
                    code_temp.seek(code_temp.tell() - 6)
                else:
                    code_temp.write(f"0{fips}000")
            if area:
                while True:
                    partial = input(
                        "Area is partially affected? (0 - entire area, 1 - \
northwest, 2 - north-central, 3 - northeast, 4 - west-central, 5 - central, 6 \
- east-central, 7 - southwest, 8 - south-central, 9 - southeast) "
                    ).lower()
                    match partial:
                        case "0" | "all" | "entire":
                            code_temp.write("0")
                        case "1" | "northwest" | "nw":
                            code_temp.write("1")
                        case "2" | "north-central" | "nc":
                            code_temp.write("2")
                        case "3" | "northeast" | "ne":
                            code_temp.write("3")
                        case "4" | "west-central" | "wc":
                            code_temp.write("4")
                        case "5" | "central" | "c":
                            code_temp.write("5")
                        case "6" | "east-central" | "ec":
                            code_temp.write("6")
                        case "7" | "southwest" | "sw":
                            code_temp.write("7")
                        case "8" | "south-central" | "sc":
                            code_temp.write("8")
                        case "9" | "southeast" | "se":
                            code_temp.write("9")
                        case _:
                            print("Invalid input.")
                            continue
                    code_temp.seek(code_temp.tell() + 5)
                    break
            if i == 30:
                code_temp.write("+")
            else:
                print(f"You can include {30 - i} more area(s).")
                ans = input("Add another area? (yes or no) ")
                if ans in ["yes", "y"]:
                    code_temp.write("-")
                    continue
                else:
                    code_temp.write("+")
                    break
    while True:
        try:
            hours = int(input("For how many hours will this event last? (max 99) "))
        except ValueError:
            print("That's not an integer.")
            continue
        if hours < 0 or hours > 99:
            print("Out of range.")
            continue
        code_temp.write(f"{hours:02d}")
        break
    while True:
        try:
            minutes = int(input("Plus how many minutes? (max 59) "))
        except ValueError:
            print("That's not an integer.")
            continue
        if minutes < 0 or minutes > 59:
            print("Out of range.")
            continue
        code_temp.write(f"{minutes:02d}-")
        break
    ans = input("Use current time as the issuance time? (yes or no) ")
    if ans in ["yes", "y"]:
        code_temp.write(f"{datetime.datetime.now(datetime.UTC).strftime('%j%H%M')}-")
    else:
        print("Time zone is UTC.")
        while True:
            try:
                month = int(input("Enter the month of issuance (as a number) "))
                if month < 1 or month > 12:
                    print("Invalid month.")
                    continue
                day = int(input("Enter the day of issuance. "))
                if day < 1 or day > 31:
                    print("Invalid day.")
                    continue
                hour = int(input("Enter the hour of issuance. (0-23) "))
                if hour < 0 or hour > 23:
                    print("Invalid hour.")
                    continue
                minute = int(input("Enter the minute of issuance. "))
                if minute < 0 or minute > 59:
                    print("Invalid minute. ")
                    continue
            except ValueError:
                print("That's not an integer.")
                continue
            try:
                code_temp.write(
                    f"{datetime.datetime(datetime.datetime.now().year, month, day, hour, minute).strftime('%j%H%M')}-"
                )
            except ValueError:
                print("Invalid date entered.")
                continue
            break
    while True:
        sender = input("Enter the sender name. (no more than 8 characters) ")
        if len(sender) > 8:
            print("Sender name must be no more than 8 characters long.")
            continue
        if sender.find("-") + 1:
            print(
                "Sender name cannot have dashes. It is common practice to use \
/ in place of -."
            )
            continue
        break
    code_temp.write(f"{sender}-")
    code = code_temp.getvalue()
    print(code)
    ans = input("Here is the output SAME header. Is this OK? (yes or no) ")
    if ans in ["yes", "y"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    while main():
        code_temp.close()
        code_temp = io.StringIO("ZCZC-")
        continue
    ans = input("Create audio file? (yes or no) ")
    if ans in ["yes", "y"]:
        code = code_temp.getvalue()
        code_temp.close()
        filename = input("Enter output filename. (same.wav) ")
        if filename:
            outpath = str(Path(filename).with_suffix(".wav"))
        else:
            outpath = "same.wav"
        same.main(Namespace(playaudiolive=0, code=code, output=outpath))
