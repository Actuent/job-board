'use strict';

document.addEventListener('DOMContentLoaded', function () {
  console.log('Hello Bulma!');
});

function showQuery() {
  var keywords = document.getElementById("keywords").value;
  var location = document.getElementById("location").value;

  var result = "Showing results for <i>" + keywords + "</i> in <i>" + location + "</i><br><br>";

  document.getElementById("youSearched").innerHTML = result.toString();

  const talent = new XMLHttpRequest();
  const url = "https://neuvoo.com/services/api-new/search?ip=1.1.1.1&useragent=123asd&k="+ keywords.replace(/ /g, "%20") + "&l=" + location.replace(/ /g, "%20") + "&country=us&contenttype=all&limit=100&format=json&publisher=92f7a67c&cpcfloor=1&subid=10101&jobdesc=1";

  talent.onreadystatechange = function() {
if (this.readyState == 4 && this.status == 200) {
  var jobsData = JSON.parse(this.responseText);
  buildResults(jobsData);
  }
};
  talent.open("GET", url);
  talent.send();

   }

function entryLevelQ(jobtitle, description) {
  let titlepattern = new RegExp("I{2,3}|IV|[sS]enior|SENIOR|[sS]r\.*|[lL]ead|[dD]irector|[Pp]rincipal|[mM]anage|[eE]xperienced|[mM]id-[lL]evel|TS/SCI|[tT]op [sS]ecret|Clearance", "i");
  // let  descriptionpattern = new RegExp("(?:[mM]inimum|[mM]in\.?|[aA]t least|[tT]otal|[iI]ncluding|[wW]ith).+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\+* (?:[yY]ears*|[yY]rs*) [^old]|[mM]aster'?s");

  let titleQ = titlepattern.test(jobtitle);
  // let descriptionQ = false;

  // If there was no exclusion because of the title check the description
  // if (!titleQ) {
  //   descriptionQ = descriptionpattern.test(description);
  // };
  return !(titleQ);
}

  function buildResults(arr) {
    var out = "";
    var i;
    for(i = 0; i < arr.results.length; i++) {
      let jobtitle = arr.results[i].jobtitle;
      let description = arr.results[i].description;

      if (entryLevelQ(jobtitle, description)) {

        // out += '<div class="card">'
        //     		+	'<header class="card-header">'
        //     				+ '<p class="card-header-title">'
        //     					+ '<a href="' + arr.results[i].url + '">'
        //               + jobtitle
        //               + '</a>'
        //               + ' at '
        //               + arr.result[i].company
        //     				+ '</p>'
        //     				+ '<a href="#" class="card-header-icon" aria-label="more options">'
        //           + '<span class="icon">'
        //             + '<i class="fas fa-angle-down" aria-hidden="true"></i>'
        //           + '</span>'
        //         + '</a>'
        //     			+ '</header>'
        //     			+ '<div class="card-content">'
        //     				+ '<div class="content">'
        //     				+	description.substring(0,200)
        //             + '...'
        //     				+ '</div>'
        //     			+ '</div>'
        //     			+ '<footer class="card-footer">'
        //     				+ '<a href="#" class="card-footer-item">Expand</a>'
        //     			+ '</footer>'
        //     		+ '</div><br>';

        out += '<a href="' + arr.results[i].url + '">' + jobtitle + '</a> at '+ arr.results[i].company + '<br><span class="teaser">' + description.substring(0, 200) + '</span> <span class ="complete">'+ description.substring(201) + '</span><span class="more">more...</span><br><br>';
        // may have to use a try-except block for that substring

        document.getElementById("jobResults").innerHTML = out;
      };

    }
  }

$(".more").toggle(function(){
    $(this).text("less..").siblings(".complete").show();
}, function(){
    $(this).text("more..").siblings(".complete").hide();
});
