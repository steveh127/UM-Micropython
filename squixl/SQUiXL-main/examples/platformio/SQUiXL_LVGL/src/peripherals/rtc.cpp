#include "rtc.h"
#include "esp32s3/rom/rtc.h"
#include "squixl.h"
#include <LittleFS.h>

using json = nlohmann::json;

/**
 * @brief Construct a new nlohmann define type non intrusive with default object
 *
 * All settings you want to be serialised and deserialised with JSON and stored in user flash need to be added here.
 * This has a HARD (NOT CHANGEABLE) LIMIT of 64 items
 */

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_WITH_DEFAULT(Alarm, type, dayOfMonth, dayOfWeek, hour, minute, enabled);

NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE_WITH_DEFAULT(Alarms, alarms);

static bool interruptTriggered = true;

static void rtcInterrupt()
{
	interruptTriggered = true;
}

const char *ntpServer = "pool.ntp.org";

// String days[7] = {"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"};
// String months[12] = {"JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"};

String day_names[7] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
String month_names[12] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};

bool RTC::init()
{
	if (rtc.begin() == false)
	{
		Serial.println("Failed to detect RV-3028-C7!");
		return false;
	}

	Serial.println("RV-3028-C7 connected!");

	enabled = true;

	interruptTriggered = true;

	// pinMode(RTC_INT, INPUT_PULLUP);
	// attachInterrupt(digitalPinToInterrupt(RTC_INT), rtcInterrupt, FALLING);

	requiresNTP = rtc.getCurrentDateTimeComponent(DATETIME_YEAR) < 23;

	Serial.printf("Does the RTC require NTP lookup? %s\n", (requiresNTP ? "YES" : "NO"));

	if (!requiresNTP)
		hasTime = true;

	// Load in any alarms that were previously set
	// load();
	// Not sure what I have to do to re-process these yet after a load, as the RTC should have retained all alarms
	// so long as the power was not removed (battery flat, or USB removed with no battery).
	// Future Seon issue!

	// save();

	// setup_interrupt();

	return true;
}

bool RTC::did_time_change()
{
	// if (requiresNTP)
	// 	return false;

	return rtc.didCurrentTimeChange();
}

void RTC::process_alarms()
{
	if (interruptTriggered)
	{
		if (rtc.isInterruptDetected(INTERRUPT_ALARM))
		{
			// squixl.notify_alarm();
			rtc.clearInterrupt(INTERRUPT_ALARM);
		}
		interruptTriggered = false;
	}
}

bool RTC::set_time_from_NTP(int16_t utc_offset)
{
	if (!enabled)
		return false;

	bool time_error = false;

	if (utc_offset != 999)
	{
		configTime(utc_offset * 3600, 0, ntpServer);
		delay(100);

		struct tm timeinfo;
		if (!getLocalTime(&timeinfo))
		{
			Serial.println("Failed to obtain time");
			time_error = true;
		}
		else
		{
			Serial.println("SET DA TIME!");
			rtc.setDateTimeFromTM(timeinfo);
		}
	}
	else
		time_error = true;

	if (time_error)
	{
		// Hard-coded for time error
		rtc.setDateTimeFromISO8601("1900-01-01T00:00:00");
	}

	// Writes the new date time to RTC, good or bad
	rtc.synchronize();

	return !time_error;
}

void RTC::set_hourly_alarm(uint minutes)
{
	setup_interrupt();

	rtc.setHourlyAlarm(/*minute=*/minutes);
	rtc.enableInterrupt(INTERRUPT_ALARM);
}

// String RTC::get_hours_string(bool padded, bool is24hour)
// {
// 	int hour = rtc.getCurrentDateTimeComponent(DATETIME_HOUR);
// 	if (!is24hour && hour > 12)
// 		hour -= 12;
// 	String txt = String(rtc.getCurrentDateTimeComponent(DATETIME_HOUR));
// 	if (padded && hour < 10)
// 		return "0" + String(hour);
// 	return String(hour);
// 	;
// }

String RTC::get_hours_string(bool padded, bool is24hour)
{
	int hour = rtc.getCurrentDateTimeComponent(DATETIME_HOUR);
	if (!is24hour && hour > 12)
	{
		hour -= 12;
	}
	char buf[3]; // enough for "hh" and the null terminator
	if (padded)
	{
		snprintf(buf, sizeof(buf), "%02d", hour);
	}
	else
	{
		snprintf(buf, sizeof(buf), "%d", hour);
	}
	return String(buf);
}

// String RTC::get_mins_string(bool padded)
// {
// 	String txt = String(rtc.getCurrentDateTimeComponent(DATETIME_MINUTE));
// 	if (padded && txt.length() < 2)
// 		return "0" + txt;
// 	return txt;
// }

// String RTC::get_secs_string(bool padded)
// {
// 	String txt = String(rtc.getCurrentDateTimeComponent(DATETIME_SECOND));
// 	if (padded && txt.length() < 2)
// 		return "0" + txt;
// 	return txt;
// }

String RTC::get_mins_string(bool padded)
{
	int minute = rtc.getCurrentDateTimeComponent(DATETIME_MINUTE);
	char buf[3]; // "mm" + null terminator
	if (padded)
	{
		snprintf(buf, sizeof(buf), "%02d", minute);
	}
	else
	{
		snprintf(buf, sizeof(buf), "%d", minute);
	}
	return String(buf);
}

String RTC::get_secs_string(bool padded)
{
	int second = rtc.getCurrentDateTimeComponent(DATETIME_SECOND);
	char buf[3]; // "ss" + null terminator
	if (padded)
	{
		snprintf(buf, sizeof(buf), "%02d", second);
	}
	else
	{
		snprintf(buf, sizeof(buf), "%d", second);
	}
	return String(buf);
}

// String RTC::get_time_string(bool padded, bool is24hour)
// {
// 	String txt = get_hours_string(false, is24hour);
// 	txt += ":";
// 	txt += get_mins_string(padded);

// 	return txt;
// }

String RTC::get_time_string(bool padded, bool is24hour)
{
	int hour = rtc.getCurrentDateTimeComponent(DATETIME_HOUR);
	if (!is24hour && hour > 12)
	{
		hour -= 12;
	}
	int minute = rtc.getCurrentDateTimeComponent(DATETIME_MINUTE);
	char buf[6]; // Format "hh:mm" (or "h:mm") plus null terminator
	if (padded)
	{
		snprintf(buf, sizeof(buf), "%02d:%02d", hour, minute);
	}
	else
	{
		snprintf(buf, sizeof(buf), "%d:%02d", hour, minute);
	}
	return String(buf);
}

// String RTC::get_time_string_seconds(bool padded, bool is24hour)
// {
// 	String txt = get_hours_string(false, is24hour);
// 	txt += ":";
// 	txt += get_mins_string(padded);
// 	txt += ":";
// 	txt += get_secs_string(padded);

// 	return txt;
// }

String RTC::get_time_string_seconds(bool padded, bool is24hour)
{
	if (!hasTime)
		return "--:--:--";

	uint8_t seconds, mins, hours, day_week, day_month, month, year;

	rtc.getCurrentTimeComponents(&seconds, &mins, &hours);
	// rtc.getCurrentDateComponents(&day_week, &day_month, &month, &year);

	// if (year < 23)
	// 	return "--:--:--";

	if (!is24hour && hours > 12)
	{
		hours -= 12;
	}
	char buf[9]; // Format "hh:mm:ss" (or "h:mm:ss") plus null terminator
	if (padded)
	{
		snprintf(buf, sizeof(buf), "%02d:%02d:%02d", hours, mins, seconds);
	}
	else
	{
		snprintf(buf, sizeof(buf), "%d:%02d:%02d", hours, mins, seconds);
	}
	return String(buf);
}

String RTC::get_date_string(bool inc_dayofweek, bool date_us)
{
	if (!hasTime)
		return "...";
	uint8_t seconds, mins, hours, day_week, day_month, month, year;

	// rtc.getCurrentTimeComponents(&seconds, &mins, &hours);
	rtc.getCurrentDateComponents(&day_week, &day_month, &month, &year);

	if (cached_date = "" || cached_day != day_month || cached_month != month || cached_year != year)
	{

		cached_date = month_names[month - 1] + " " + String(day_month) + ", 20" + String(year);

		if (inc_dayofweek)
		{
			cached_date = day_names[day_week] + ", " + cached_date;
		}

		cached_day = day_month;
		cached_month == month;
		cached_year = year;
	}

	return cached_date;
}

int RTC::get_hours() { return (rtc.getCurrentDateTimeComponent(DATETIME_HOUR)); }

int RTC::get_mins() { return (rtc.getCurrentDateTimeComponent(DATETIME_MINUTE)); }

int RTC::get_seconds() { return (rtc.getCurrentDateTimeComponent(DATETIME_SECOND)); }

uint16_t RTC::get_day() { return (rtc.getCurrentDateTimeComponent(DATETIME_DAY_OF_MONTH)); }

uint16_t RTC::get_month() { return (rtc.getCurrentDateTimeComponent(DATETIME_MONTH)); }

uint16_t RTC::get_year() { return ((uint16_t)rtc.getCurrentDateTimeComponent(DATETIME_YEAR) + 2000); }

void RTC::get_step_date(uint16_t &day, uint16_t &month, uint16_t &year)
{
	if (next_rtc_read == 0 || millis() - next_rtc_read > 5000)
	{
		next_rtc_read = millis();
		cached_day = get_day();
		cached_month = get_month();
		cached_year = get_year();
	}

	day = cached_day;
	month = cached_month;
	year = cached_year;
}

void RTC::setup_interrupt()
{
	interruptTriggered = false;
	attachInterrupt(digitalPinToInterrupt(interruptPin), rtcInterrupt, FALLING);
}

String RTC::get_day_of_week() { return day_names[rtc.getCurrentDateTimeComponent(DATETIME_DAY_OF_WEEK)]; }

String RTC::get_month_date()
{
	String raw = month_names[rtc.getCurrentDateTimeComponent(DATETIME_MONTH) - 1].substring(0, 3);
	raw += " ";
	raw += String(rtc.getCurrentDateTimeComponent(DATETIME_DAY_OF_MONTH));
	return raw;
}

bool RTC::check_interrupt()
{
	if (!interruptTriggered)
	{
		return false;
	}

	interruptTriggered = false;
	if (rtc.isInterruptDetected(INTERRUPT_ALARM))
	{
		Serial.print("Alarm: ");
		Serial.println(get_time_string(true, true));
		rtc.clearInterrupt(INTERRUPT_ALARM);
	}

	return true;
}

void RTC::create_alarm(AlarmType _mode, uint8_t _dayOfMonth, uint8_t _hour, uint8_t _minute)
{
	Alarm a = Alarm();
	if (_mode == AlarmType::A_MONTHLY)
	{
		a.add_alarm_monthly(_mode, _dayOfMonth, _hour, _minute);
		rtc.setDateAlarm(_mode, _dayOfMonth, _hour, _minute);
		Serial.printf("Added Monthly Alarm: Day %d, %d:%d\n", _dayOfMonth, _hour, _minute);
	}
	else if (_mode == AlarmType::A_WEEKLY)
	{
		a.add_alarm_weekly(_mode, (DayOfWeek_t)_dayOfMonth, _hour, _minute);
		rtc.setWeekdayAlarm(_mode, (DayOfWeek_t)_dayOfMonth, _hour, _minute);
		Serial.printf("Added Weekly Alarm: %s, %d:%d\n", day_names[_dayOfMonth], _hour, _minute);
	}
	rtc.enableInterrupt(INTERRUPT_ALARM);
	current_alarms.alarms.push_back(a);

	save();
}

void RTC::create_alarm(AlarmType _mode, uint8_t _hour, uint8_t _minute)
{
	Alarm a = Alarm();
	a.add_alarm_daily(_mode, _hour, _minute);
	current_alarms.alarms.push_back(a);
	rtc.setDailyAlarm(_hour, _minute);
	rtc.enableInterrupt(INTERRUPT_ALARM);

	Serial.printf("Added Daily Alarm: %s, %d:%d\n", _hour, _minute);

	save();
}

void RTC::create_alarm(AlarmType _mode, uint8_t _minute)
{
	Alarm a = Alarm();
	a.add_alarm_hourly(_mode, _minute);
	current_alarms.alarms.push_back(a);
	rtc.setHourlyAlarm(_minute);
	rtc.enableInterrupt(INTERRUPT_ALARM);

	Serial.printf("Added Hourly Alarm: XX:%d\n", _minute);

	save();
}

/**
 * @brief Load the alarms from the FLASH FS and deserialise them from JSON back into the Alarms struct
 *
 * @return true
 * @return false
 */
bool RTC::load()
{
	Serial.println("Loading Alarms");

	File file = LittleFS.open(filename);
	if (!file || file.isDirectory() || file.size() == 0)
	{
		// No data on the flash chip, so create new data
		file.close();

		Serial.println("Alarms CREATE: Creating new data...");

		current_alarms = {};

		save();

		return true;
	}

	std::vector<char> _data(file.size());
	size_t data_bytes_read = file.readBytes(_data.data(), _data.size());
	if (data_bytes_read != _data.size())
	{
		// Reading failed
		String log = "bad read " + String(file.size()) + " " + String((int)data_bytes_read);
		// log_to_nvs("load_status", log.c_str());
		file.close();
		// create();
		return false;
	}

	try
	{
		json json_data = json::parse(_data);

		// Convert json to struct
		current_alarms = json_data.get<Alarms>();
	}
	catch (json::exception &e)
	{
		Serial.println("Settings parse error:");
		Serial.println(e.what());
		file.close();
		// create();
		// log_to_nvs("load_status", "bad json parse");
		return false;
	}

	file.close();

	return true;
}

bool RTC::save()
{
	// // We only want to attempt  save every 1 min unless it's a forced save.
	// if (!force && millis() - last_save_time < max_time_between_saves)
	// 	return false;

	// Implicitly convert struct to json
	json data = current_alarms;

	// // If the data is the same as the last data we saved, bail out
	if (data == current_alarms.last_saved_data)
	{
		return false;
	}

	std::string serializedObject = data.dump();

	// Serial.print("Data Length: "+String(serializedObject.length())+"-> ");
	// Serial.println(serializedObject);

	File file = LittleFS.open(tmp_filename, FILE_WRITE);
	if (!file)
	{
		Serial.println("Failed to write to Alarms file");
		// log_to_nvs("save_status", "failed to open for write");
		return false;
	}

	file.print(serializedObject.c_str());
	// log_to_nvs("save_status", "data written");

	file.close();
	// log_to_nvs("save_status", "file closed");

	LittleFS.rename(tmp_filename, filename);
	// log_to_nvs("save_status", "file renamed");

	Serial.println("Alarms SAVE: Saved!");

	// Store last saved data for comparison on next save
	current_alarms.last_saved_data.swap(data);

	// last_save_time = millis();
	return true;
}

void RTC::print_file()
{
	File file = LittleFS.open(filename);
	std::vector<char> _data(file.size());
	size_t data_bytes_read = file.readBytes(_data.data(), _data.size());

	Serial.println("RTC Alarms JSON");
	for (char c : _data)
	{
		Serial.print(c);
	}
	Serial.println();

	file.close();
}

RTC rtc;
