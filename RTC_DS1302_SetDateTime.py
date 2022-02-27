import RTC_DS1302
import os
import time

ThisRTC = RTC_DS1302.RTC_DS1302()

yr = input('Year(2 digits):')
mo = input('Month:')
dy = input('Day:')
dw = input('Day of week (0 - 6):')
hr = input('Hour:')
mi = input('Minutes:')
sc = input('Second:')
ThisRTC.WriteDateTime(yr, mo, dy, dw, hr, mi, sc)



Data = ThisRTC.ReadRAM()
print("Message: " + Data)
DateTime = { "Year":0, "Month":0, "Day":0, "DayOfWeek":0, "Hour":0, "Minute":0, "Second":0 }
Data = ThisRTC.ReadDateTime(DateTime)

print("Date/Time: " + Data)
print("Year: " + format(DateTime["Year"] + 2000, "04d"))
print("Month: " + format(DateTime["Month"], "02d"))
print("Day: " + format(DateTime["Day"], "02d"))
print("DayOfWeek: " + ThisRTC.DOW[DateTime["DayOfWeek"]])
print("Hour: " + format(DateTime["Hour"], "02d"))
print("Minute: " + format(DateTime["Minute"], "02d"))
print("Second: " + format(DateTime["Second"], "02d")) 

