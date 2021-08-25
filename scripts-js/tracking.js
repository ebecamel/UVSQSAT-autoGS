rename("tracking_task");
var tracker = new SharedMap('tracking');

var station1 = new Observer('station_1');

load("./config.js");

station1.setPosition( {'latitude' : gs_latitude, 'longitude' : gs_longitude, 'asl' : gs_asl} ); // Création de l'emplacement de la station

var TLE_first; // create TLE
var sat_track;

while(1)
{
	var satlist = TLE.loadTLE(tle_path); // Download TLE

	if(print_debug)
	{
		print(satlist.length + ' satellites loaded.');
	}

	for(var j=0; j < satlist.length; j++) // Read downloaded TLE
	{
		TLE_first = satlist[j];
		if(TLE_first.norad_number == target) // Search the NORAD number in the TLE
		{
			sat_track = new Satellite(satlist[j].name);
			sat_track.setTLE(TLE_first.L1, TLE_first.L2);
			break;
		}
	}

	var passes = sat_track.predictPasses(station1, 24); // calcul des passages sur les prochaines 24h sur la station sol

	if(passes.length > 0)
	{
		for(n=0; n < 5; n++)
		{
			var next = passes[n]; // On sélectionne le prochain passage
			var dopev = sat_track.getPassDetails(station1, next.aos_secs, next.pass_duration); // Stocke les infos du prochains passage
			if(print_passes)
			{
				print("AOS : " + dopev.pass_start_time + " -- LOS : " + dopev.pass_end_time + " -- max elev : " + passes[n].max_elevation);
			}
			
		}

	}

	var n = 0;
	var doppler = sat_track.getDopplerEstimation( station1, frequency_sat );

	while(sat_track.waitInView(station1) == false)
	{
		if(print_debug)
		{
			passes = sat_track.predictPasses(station1, 15);
			print("Waiting " + satlist[j].name + ", AOS in " + new Date(passes[0].aos_secs * 1000).toISOString().substr(11, 8) );
		}
		sleep(2000);
	}

	var n = 0;
	while(sat_track.waitInView( station1 ) == true)
	{
		doppler = sat_track.getDopplerEstimation( station1, frequency_sat );
		tracker.store('doppler', doppler.doppler_avg);
		if(print_debug)
		{
			print("Doppler: " + doppler.doppler_avg);
		}
		tracker.store('status', true);
		if(!n)
		{
			createTask("stream.js");
			n = 1;
		}
		sleep(1000);
	}
	tracker.store('status', false);
	if(print_debug)
	{
		print("end of pass");
	}
}