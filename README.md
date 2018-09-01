# Conversion of spectrophotometry data (CIE-L**a**b to sRGB)

Colour is an important parameter in the geosciences. It is used to describe sediment and often allows for the interpretation of depositional environment, estimate organic content or aids in the identification of geological boundaries, amongst others. 

In core analysis, colour is measured either manually or automatically with spectrophotometers. The output of these spectrophotometers, at least when we conducted these measurements more than 10 years ago, was a dataset in CIE-LAB format. While it is, theoretically, be possible to plot this data, it is much more straight forward to simply convert the data to the sRGB colorspace which can easily be used in many different programs.

An example of the results is shown below. On the left the raw CIE-LAB data, on the right the final colormap calculated from the CIE-LAB data.

<p align="center">
<img src="example.png" width="500">
</p>

There is very little information available about color conversion from official sources. Hence, most of the calculations used in the code were taken from information provided by www.easyrgb.com and http://www.brucelindbloom.com/. 