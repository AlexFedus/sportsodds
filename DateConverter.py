import datetime
import zoneinfo
from dateutil import parser
from datetime import timezone
import pytz, dateutil.parser

def convertDate(isodate):

    months = {	'01':'January',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'		
        }
   
  
    utctime = dateutil.parser.parse(isodate)
    convertedTime = utctime.astimezone(pytz.timezone("America/New_York"))

     
    year = convertedTime.strftime("%Y")
    

    month = convertedTime.strftime("%m")
    fullmonth = months.get(month)
    
    

    day = convertedTime.strftime("%d")
    

    time = convertedTime.strftime("%H:%M")
    stdtime = datetime.datetime.strptime(time,'%H:%M').strftime('%I:%M %p')

    if stdtime.startswith("0"):
        stdtime = stdtime[1:]
    
    return fullmonth + " " + day + ", " + year + " " + stdtime

   




