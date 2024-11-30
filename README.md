# Emergency Alert System (EAS) Specific Area Message Encoding (SAME) Encoder

(original: https://github.com/nicksmadscience/eas-same-encoder)

Create SAME headers and encode them to audio.
Note: Wrapper requires the external module `addfips`. Install it by using `pip3 install addfips` if you haven't already.

[Here's a quick background on how EAS SAME headers work.](https://www.youtube.com/watch?v=Z5o1sfXXf9E)

This tool was built primarily to test EAS ENDECs.

An EAS ENDEC is a device that would sit in the headend room of TV / FM / AM stations, listen for EAS SAME signals on neighboring
stations, and, if the specified information matched the predefined filters, rebroadcast the emergency message on its local station.

[YouTube demo!](https://www.youtube.com/watch?v=OVxHkMDX2F8)

# Important Note

Please please please please PLEASE use this responsibly.  Did you just buy an old ENDEC on eBay and want to put it through its paces?  This is the script for you!

Don't use this to hack / exploit anything.  I made this for funsies in a few hours.  Please use it accordingly.
