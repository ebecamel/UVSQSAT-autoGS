/*
    STATION CONFIGURATION FILE
*/

// Ground station emplacement
var gs_latitude = 0.00000; // latitude
var gs_longitude = 0.00000; // longitude
var gs_asl = 200; // Altitude above sea level

// file path
var tle_path = "https://www.celestrak.com/NORAD/elements/amateur.txt"; // path to .txt file or link to TLE file
var path_cmd_file = "/path/to/launch_decode.sh"; // path to the bash file

// Satellite
var target = 47438; // NORAD number of the target
var frequency_sat = 437.020e6; //Sat frequency in Hz

// RTLSDR
var rtl_gain = 49.6; // rtlsdr gain

// Print in terminal
var print_passes = true; // print list of future passes true or false
var print_debug = true; //Print debug in terminal true or false
