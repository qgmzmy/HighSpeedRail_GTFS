startTime_s=`date +%s`


python3 generate_feed_info.py
echo feed_info done
python3 generate_calendar.py
echo calendar done
python3 generate_trips.py
echo trips done
python3 generate_stop_times.py
echo stop_times done
python3 generate_translations.py
echo translations done
zip -j gtfs.zip ./gtfs/*

endTime_s=`date +%s`

sumTime=$[ $endTime_s - $startTime_s ]

echo $sumTime
