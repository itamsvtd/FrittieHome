var WEBSITE_HOMEPAGE = "http://localhost:8000";

var month_name_short = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }

var month_name_full = {
          1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }

var week_day_text = {
          "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", 
          "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"
        }

var week_day_num = {
          0: "Monday", 1: "Tuesday", 2: "Wednesday", 
          3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"
        }

var state_name = {
   "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California",
   "CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia",
   "HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa",
   "KS":"Kansas","KY":"Kentucky","LA":"Louisana","ME":"Maine","MD":"Maryland",
   "MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri",
   "MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
   "NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio",
   "OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
   "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont",
   "VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"
}

// Constant value for daylight saving time in USA
// DST_start and DST_end define the interval time
// of daylight saving time. hour_offset define how
// many hour deduct to get the exact local time
var DST_start = {"month": 3, "day": 11}
var DST_end = {"month": 11, "day": 4}
var hour_offset = {"in": 4, "out": 5}

function show_message(data,el) {
    var new_item = $(data).hide();
    $(el).append(new_item);
    new_item.slideDown();
    setTimeout(function(){
        new_item.slideUp(function(){ 
            jQuery(this).remove(); 
        });
    },3000);
}

// Custom error notice if the ajax request is failed
function custom_error(error_message){
    var data = '<div class="error-message-content">' + error_message + "</div>"
    show_message(data,$('.error-area'))
}

// Another function of getting cursor
function getCaret(el) {
  if (el.selectionStart) {
    return el.selectionStart;
  } else if (document.selection) {
    el.focus();

    var r = document.selection.createRange();
    if (r == null) {
      return 0;
    }

    var re = el.createTextRange(),
        rc = re.duplicate();
    re.moveToBookmark(r.getBookmark());
    rc.setEndPoint('EndToStart', re);

    return rc.text.length;
  } 
  return 0;
}

// Strip whitespace function
function strip_whitespace(str) {
    return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}

// Convert 24hr system to am/pm system 
function convert_24hr_to_AM_PM(year,month,day,hour,minute){
    var minute_str = minute.toString();
    if (minute < 10){
        minute_str = "0" + minute.toString();
  }
    if (hour == 0) 
        return "12" + ":" + minute_str+ "am";
    if ((hour > 0) && (hour < 12))
        return hour.toString() + ":" + minute_str + "am";
    if (hour == 12) 
        return "12" + ":" + minute_str + "pm";
    if (hour > 12)
        return (hour-12).toString() + ":" + minute_str + "pm";
}

// Simple function return this type of format: Wednesday, January 13, 2012
function convert_date_name(year,month,day,weekday) {
  return week_day_num[weekday] + ", " + month_name_full[month] + " " + day + ", " + year;
}

// Analyze datetime string taken from API with 
// iso format and return the corresponding datetime value
function iso_date_analyze(date) {
    var year = parseInt(date.substring(0,4));
    var month = parseInt(date.substring(5,7),10);
    var day = parseInt(date.substring(8,10),10);
    var hour = parseInt(date.substring(11,13),10);
    var minute = parseInt(date.substring(14,16),10);
    var second = parseInt(date.substring(17,19),10);
    return { "year": year, "month": month, "day": day, "hour": hour, "minute": minute, "second": second }
}


function is_numeric(el_check,default_val,range,return_result) {
    if (typeof return_result == "undefined") return_result = false
    var temp=parseInt($(el_check).val());
    var result;
    if (isNaN(temp)) {
        result = false
        temp=default_val;
    } else {
        result = true
        if (range.length != 0) {
            if (temp < range['min']) temp = range['min'];
            if (temp > range['max']) temp = range['max'];
        }
    }
    if (default_val != null) {
        $(el_check).val(temp);
    }
    if (return_result) return result
}

function is_empty(el_check) {
    if(($(el_check).val().length==0) || ($(el_check).val()==null)) {
        return true;
    } else{
        return false
    }
}

function is_el_exist(el) {
    if ($(el).length > 0){
        return true
    } else {
        return false
    } 
}

// Return a datetime format for comment: June 19, 2012, 12:42pm. All the function here can be found in common.js
function standard_datetime_format(year,month,day,hour,minute) {
    return month_name_full[month] + " " + day + ", " + year + ", " + convert_24hr_to_AM_PM(year,month,day,hour,minute)['string']
}