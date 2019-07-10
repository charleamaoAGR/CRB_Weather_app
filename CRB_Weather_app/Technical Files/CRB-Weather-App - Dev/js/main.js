      function buttonZoomTo(b) {
        map1.fitBounds(b);
      }

      function getColor(rm,par) {
        for(var i = 0; i < currentjson.length; i++) {
          var obj = currentjson[i];

          if (obj.muni_name == rm) {
            theVal = obj[par];
            break;
          }
        }
        var theColor = valToColor(theVal,par);
        return theColor;
      }

      function valToColor(v,p) {
        if (p == "ws") {
          return v >= 40 ? '#ff3434' :
            v >= 30 ? '#ffa500' :
            v >= 20  ? '#1a9641' :
            v >= 10  ? '#a6d96a' :
                       '#555';
        } else if (p == "ws_pbl") {
          return v >= 80 ? '#ff3434' :
             v >= 60 ? '#ffa500' :
             v >= 40  ? '#1a9641' :
             v >= 20  ? '#a6d96a' :
                        '#555';
        } else if (p == "hgt_pbl") {
          return v >= 2000 ? '#0d4b20' :
            v >= 1500 ? '#1a9641' :
            v >= 700  ? '#a6d96a' :
            v >= 300  ? '#ffffbf' :
                        '#555';
        } else if (p == "vrate") {
          return v >= 25000 ? '#0d4b20' :
            v >= 7050 ? '#1a9641' :
            v >= 4700  ? '#a6d96a' :
            v >= 2350  ? '#ffffbf' :
                      '#555';
        }
      }

      function stylecrb(feature) {
        return {
          weight: 2,
          opacity: 1,
	  color: '#222',
          fillOpacity: 0
        }
      }

      function styleWS(feature) {
        return {
          fillColor: getColor(feature.properties.MUNI_NAME,"ws"),
          weight: 1,
          opacity: 1,
          color: '#777',
          dashArray: '3',
          fillOpacity: 0.7
        }
      }

      function styleTW(feature) {
        return {
          fillColor: getColor(feature.properties.MUNI_NAME,"ws_pbl"),
          weight: 1,
          opacity: 1,
          color: '#777',
          dashArray: '3',
          fillOpacity: 0.7
        }
      }

      function stylePBL(feature) {
        return {
          fillColor: getColor(feature.properties.MUNI_NAME,"hgt_pbl"),
          weight: 1,
          opacity: 1,
          color: '#777',
          dashArray: '3',
          fillOpacity: 0.7
        }
      }

      function styleVR(feature) {
        return {
          fillColor: getColor(feature.properties.MUNI_NAME,"vrate"),
          weight: 1,
          opacity: 1,
          color: '#777',
          dashArray: '3',
          fillOpacity: 0.7
        }
      }

      function $_GET(param) {
	var vars = {};
	window.location.href.replace( 
		/[?&]+([^=&]+)=?([^&]*)?/gi, // regexp
		function( m, key, value ) { // callback
			vars[key] = value !== undefined ? value : '';
		}
	);

	if ( param ) {
		return vars[param] ? vars[param] : null;	
	}
	return vars;
      }

      var lastRM;  //last RM clicked

      //list of dates
      var dateList = [];

      //create datetime dropdown.
      //get first value, to have something to compare
      dateList.push(wxdata[0].valid_date);

      for (var i = 1; i < wxdata.length; i++) {
        var obj = wxdata[i];
        if (obj.valid_date > dateList[i-1]) {
          dateList.push(obj.valid_date);
        } else {
          break;
        }
      }

      //make selection dropdown
      var $selectDT = $('<select id="dtSelect"></select>')
        .appendTo($('#dtVariables'))
        .on('change', function() {
            updateWxData($(this).val());
        });


     function formatAMPM2(hours, minutes) {
       var ampm = hours >= 12 ? 'pm' : 'am';
       hours = hours % 12;
       hours = hours ? hours : 12; // the hour '0' should be '12'
       minutes = minutes < 10 ? '0'+minutes : minutes;
       var strTime = hours + ':' + minutes + ' ' + ampm;
       return strTime;
     }


      var weekday = new Array(7);
      weekday[0]=  "Sun";
      weekday[1] = "Mon";
      weekday[2] = "Tue";
      weekday[3] = "Wed";
      weekday[4] = "Thu";
      weekday[5] = "Fri";
      weekday[6] = "Sat";

      var month = new Array(12);
      month[0] = "Jan";
      month[1] = "Feb";
      month[2] = "Mar";
      month[3] = "Apr";
      month[4] = "May";
      month[5] = "Jun";
      month[6] = "Jul";
      month[7] = "Aug";
      month[8] = "Sep";
      month[9] = "Oct";
      month[10] = "Nov";
      month[11] = "Dec";

      moment.tz.add('America/Winnipeg|CST CDT CWT CPT|60 50 50 50|010101023010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010|-2aIi0 WL0 3ND0 1in0 Jap0 Rb0 aCN0 8x30 iw0 1tB0 11z0 1ip0 11z0 1o10 11z0 1o10 11z0 1rd0 10L0 1op0 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1o10 11z0 1qN0 11z0 1o10 11z0 1o10 11z0 1o10 1cL0 1cN0 11z0 6i10 WL0 6i10 1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1a00 1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1a00 1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 14o0 1lc0 14o0 1o00 11A0 1o00 11A0 1o00 14o0 1lc0 14o0 1lc0 14o0 1o00 11A0 1o00 11A0 1o00 14o0 1lc0 14o0 1lc0 14o0 1lc0 14o0 1o00 11A0 1o00 11A0 1o00 14o0 1lc0 14o0 1lc0 14o0 1o00 11A0 1o00 11A0 1nX0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0');

      moment.tz.setDefault("America/Winnipeg");

      //add in values
      for (var i = 0; i < dateList.length; i++) {
        var thisDate = moment(dateList[i]);
        var thisWDay = weekday[thisDate.day()];
        var thisHour = formatAMPM2(thisDate.hour(),thisDate.minute());
        var thisMonth = month[thisDate.month()];
        var thisDay = thisDate.date();

        //if first hour, show the model date
        if (i == 0) {
          document.getElementById("modeldate").innerHTML = "Model run: " + thisWDay + " " + thisMonth + " " + thisDay + ", " + thisHour;
        }
        //Do not show midnight to 6am
        if (true) { //thisDate.hour() > 6
          $('<option></option>')
            .text(thisWDay + " " + thisMonth + " " + thisDay + ", " + thisHour)
            .attr('value', dateList[i])
            .appendTo($selectDT);
        }
      } 

      //create the RM dropdown
      rmList = [];
      rmList.push("");

      for (var i = 0; i < rmdata.features.length; i++) {
        rmList.push(rmdata.features[i].properties.MUNI_NAME);
      }

      //make selection dropdown with rm values
      var $selectRM = $('<select id="rmSelect"></select>')
        .appendTo($('#rmVariables'))
        .on('change', function() {
            rmPicked($(this).val());
        });

      //populate the rm dropdown
      for (var i = 0; i < rmList.length; i++) {
        $('<option></option>')
          .text(rmList[i])
          .attr('value', rmList[i])
          .appendTo($selectRM);
      }

      var lgroup1 = L.featureGroup();
      var lgroup2 = L.featureGroup();

      //for back button
      function backDT() {
        var x = document.getElementById("dtSelect").selectedIndex;
        var lastdt = document.getElementById("dtSelect").length - 1;

        if (x == 0) {
          document.getElementById("dtSelect").selectedIndex = lastdt;
        } else {
          document.getElementById("dtSelect").selectedIndex = x - 1;
        }
        updateWxData($selectDT.val());
        
      }

      //for forward button
      function nextDT() {
        var x = document.getElementById("dtSelect").selectedIndex;
        var lastdt = document.getElementById("dtSelect").length - 1;
        if (x == lastdt) {
          document.getElementById("dtSelect").selectedIndex = "0";
        } else {
          document.getElementById("dtSelect").selectedIndex = x + 1;
        }
        updateWxData($selectDT.val());
      }

      var center = [51.0, -97.3];
      //make basemap layers
      var bm1 = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
        attribution: ''
        });
      var bm2 = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
        attribution: ''
        });
      var bm3 = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
        attribution: ''
        });
      var bm4 = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
        });  

      //make 4 maps
      var map1 = L.map('map1', {
            layers: [bm1],
            center: center,
            zoom: 6
      });

      var map2 = L.map('map2', {
            layers: [bm2],
            zoomControl: false
      });

      var map3 = L.map('map3', {
            layers: [bm3],
            zoomControl: false
      });

      var map4 = L.map('map4', {
            layers: [bm4],
            zoomControl: false
      });

      //remove attribution text from first 3 maps
      map1.attributionControl.setPrefix('');
      map2.attributionControl.setPrefix('');
      map3.attributionControl.setPrefix('');

      //sync up all maps so they pam/zoom together
      map1.sync(map2);
      map1.sync(map3);
      map1.sync(map4);
      map2.sync(map1);
      map2.sync(map3);
      map2.sync(map4);
      map3.sync(map1);
      map3.sync(map2);
      map3.sync(map4);
      map4.sync(map1);
      map4.sync(map2);
      map4.sync(map3);

      //zoom to default bounds the first time
      map1.fitBounds([[52.6, -101.6],[49, -94.1]]);

      function highlightFeatureAllMaps(rm,theBM) {
       
        for (var lyr in theBM._layers) {
          if (theBM.getLayer(lyr).feature.properties.MUNI_NAME == rm) {
            var layer = theBM.getLayer(lyr);
            layer.setStyle({
              weight: 4,
              color: '#ff0',
              dashArray: '',
              fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera) {
              layer.bringToFront();
            }
            break;
          }
        }
      }

      function resetHighlightAllMaps(theBM) {
        //use global var lastRM
        for (var lyr in theBM._layers) {
          if (theBM.getLayer(lyr).feature.properties.MUNI_NAME == lastRM) {
            theBM.resetStyle(theBM.getLayer(lyr));
            break;
          }
        }
      }

      //RM clicked on the map
      function rmClicked(e) {
        //console.log(e);
        var layer = e.target;
        var theRM = layer.feature.properties.MUNI_NAME;

        document.getElementById("rmSelect").value = theRM;
        populateInfo(theRM);
        addChart(theRM); 

        //do this if theRM is not lastRM, in case the user clicked on it again
        if (theRM !== lastRM) { 
          highlightFeatureAllMaps(theRM,geojson1);
          highlightFeatureAllMaps(theRM,geojson2);
          highlightFeatureAllMaps(theRM,geojson3);
          highlightFeatureAllMaps(theRM,geojson4);

          resetHighlightAllMaps(geojson1);
          resetHighlightAllMaps(geojson2);
          resetHighlightAllMaps(geojson3);
          resetHighlightAllMaps(geojson4);

          lastRM = theRM;
        }
      }

      //RM picked in the list
      function rmPicked(theRM) {
          populateInfo(theRM);
          addChart(theRM); 
 
          highlightFeatureAllMaps(theRM,geojson1);
          highlightFeatureAllMaps(theRM,geojson2);
          highlightFeatureAllMaps(theRM,geojson3);
          highlightFeatureAllMaps(theRM,geojson4);

          resetHighlightAllMaps(geojson1);
          resetHighlightAllMaps(geojson2);
          resetHighlightAllMaps(geojson3);
          resetHighlightAllMaps(geojson4);

          lastRM = theRM;
      }
      

      function onEachFeature(feature, layer) {
			layer.on({
                                click: rmClicked
			});
      }


      //load wx data
      loadCurrentData($selectDT.val());

      //add rm's
      var geojson1 = new L.geoJson(rmdata, {
                   style: styleWS,
                   onEachFeature: onEachFeature
               }).addTo(map1);

      var geojson2 = new L.geoJson(rmdata, {
                   style: styleTW,
                   onEachFeature: onEachFeature
               }).addTo(map2);

      var geojson3 = new L.geoJson(rmdata, {
                   style: stylePBL,
                   onEachFeature: onEachFeature
               }).addTo(map3);

      var geojson4 = new L.geoJson(rmdata, {
  	           style: styleVR,
	           onEachFeature: onEachFeature
	       }).addTo(map4);

      //add crb zones
      var crb1 = new L.geoJson(crb_zones_old, {
                   style: stylecrb,
                   className: 'crb_zone'
               }).addTo(map1);

      var crb2 = new L.geoJson(crb_zones_old, {
                   style: stylecrb,
                   className: 'crb_zone'
               }).addTo(map2);

      var crb3 = new L.geoJson(crb_zones_old, {
                   style: stylecrb,
                   className: 'crb_zone'
               }).addTo(map3);

      var crb4 = new L.geoJson(crb_zones_old, {
                   style: stylecrb,
                   className: 'crb_zone'
               }).addTo(map4);

      //make wind icon
      var arrowIcon = L.icon({
        iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAaCAYAAABozQZiAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3wgCAikiJ2eNcQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAABQklEQVQ4y+2Uv04CQRCHv12NfyqzMZaKdyWhoTckcOcTWGqs9Dl8BAsLEwufwEIfAMSWIJ2aoAFiQYyabGFCA+xYCBGOAyGW+qt2J/Pt7M5OfooYGS93i1IpQHqhmq3lk9G8+TgYpRZBLQxEFuPSNPESppDmF/qH/zbcjexd7BQbL7hBqczsdeVJozgAOjOSbUQymkT7EZGTGeHzbse+KACzmdtA6zKwNgX4iuukbaPY1MYLsI3CM3A6ZdUz2yg2jReihhzEDyqg0uN7JHe2nk99uU12+KtEZHdiTcVhf2nr19/wSmILLa46/vpyhXMV4+UGzhoxvyCJUmVgeSDcApe1tUJp4oTZev4ecceRcCkKTpTxwzfjh2L8sA2wvn3082wbL9t7otvrLfYBPqrFmP7Fm37fq3dALueWVlvvDxcjeZ97zWSQ0tbKVQAAAABJRU5ErkJggg==',
        iconSize: [5, 16],
        iconAnchor: [0,-2],
        className: 'RotatedMarker'
      });

      function getWindDir(therm,par) {
        //get wind direction for selected parameter and currently rm
        for(var i = 0; i < currentjson.length; i++) {
          var obj = currentjson[i];

          if (obj.muni_name == therm) {
            if (par == "wd") {
              return obj.wd;
              break;
            } else if (par == "wd_pbl") {
              return obj.wd_pbl;
              break;
            }
          }
        }
      }

      function addWindVectors(par,themap,thegroup) {
        for (var i = 0; i < rm_centroids.features.length; i++) {
          var thisRM = rm_centroids.features[i].properties.MUNI_NAME;
          var wdir = getWindDir(thisRM,par);
          var wlyr = L.rotatedMarker([rm_centroids.features[i].geometry.coordinates[1],rm_centroids.features[i].geometry.coordinates[0]], {icon:arrowIcon, angle:wdir});
          thegroup.addLayer(wlyr);
        }
        thegroup.addTo(themap);
      }
     
      addWindVectors("wd",map1,lgroup1);
      addWindVectors("wd_pbl",map2,lgroup2);


    function loadCurrentData(selectedDate) {

      var newFeatures = [];

      //take the json object, and create a data array for the selected date
      for(var i = 0; i < wxdata.length; i++) {
        var obj = wxdata[i];

        if (obj.valid_date == selectedDate) {
          newFeatures.push(obj);
        }
      }
      currentjson = newFeatures;
    }


    function updateWxData(selectedDate) {

      var newFeatures = [];

      //take the json object, and create a data array for the selected date
      for(var i = 0; i < wxdata.length; i++) {
        var obj = wxdata[i];

        if (obj.valid_date == selectedDate) {
          newFeatures.push(obj);
        }
      }
      currentjson = newFeatures;

      geojson1.setStyle(styleWS);
      geojson2.setStyle(styleTW);
      geojson3.setStyle(stylePBL);
      geojson4.setStyle(styleVR);

      //now delete the current wind layers and update them
      map1.removeLayer(lgroup1);
      map2.removeLayer(lgroup2);

      lgroup1.clearLayers();
      lgroup2.clearLayers();
      addWindVectors("wd",map1,lgroup1);
      addWindVectors("wd_pbl",map2,lgroup2);

      //if lastRM is set, user has selected an RM, so highlight it again and add the data to the sidebar
      if (lastRM) {
        populateInfo(lastRM);
        highlightFeatureAllMaps(lastRM,geojson1);
        highlightFeatureAllMaps(lastRM,geojson2);
        highlightFeatureAllMaps(lastRM,geojson3);
        highlightFeatureAllMaps(lastRM,geojson4);
      }

       
    }

    function getCWD(dirVal)
    {
      if (dirVal >= 348.75) {
        return "N";
      } else if (dirVal <= 11.25) {
        return "N";
      } else if ((dirVal >= 11.25) && (dirVal <= 33.75)) {
        return "NNE";
      } else if ((dirVal >= 33.75) && (dirVal <= 56.25)) {
        return "NE";
      } else if ((dirVal >= 56.25) && (dirVal <= 78.75)) {
        return "ENE";
      } else if ((dirVal >= 78.75) && (dirVal <= 101.25)) {
        return "E";
      } else if ((dirVal >= 101.25) && (dirVal <= 123.75)) {
        return "ESE";
      } else if ((dirVal >= 123.75) && (dirVal <= 146.25)) {
        return "SE";
      } else if ((dirVal >= 146.25) && (dirVal <= 168.75)) {
        return "SSE";
      } else if ((dirVal >= 168.75) && (dirVal <= 191.25)) {
        return "S";
      } else if ((dirVal >= 191.25) && (dirVal <= 213.75)) {
        return "SSW";
      } else if ((dirVal >= 213.75) && (dirVal <= 236.25)) {
        return "SW";
      } else if ((dirVal >= 236.25) && (dirVal <= 258.75)) {
        return "WSW";
      } else if ((dirVal >= 258.75) && (dirVal <= 281.25)) {
        return "W";
      } else if ((dirVal >= 281.25) && (dirVal <= 303.75)) {
        return "WNW";
      } else if ((dirVal >= 303.75) && (dirVal <= 326.25)) {
        return "NW";
      } else if ((dirVal >= 326.25) && (dirVal <= 348.75)) {
        return "NNW";
      }

    }


    function populateInfo(rm) {
      var wd = "";
      var ws = "";
      var wd_pbl = "";
      var ws_pbl = "";
      var thePBL = "";
      var theVR = "";

      if (rm !== "") {
        //find the RM in the json data, and extract other data
        for(var i = 0; i < currentjson.length; i++) {
          var obj = currentjson[i];

          if (obj.muni_name == rm) {
            wd = obj.wd;
            ws = obj.ws;
            wd_pbl = obj.wd_pbl;
            ws_pbl = obj.ws_pbl;
            thePBL = obj.hgt_pbl;
            theVR = obj.vrate;
          }
        }
     
        document.getElementById("ws_data").innerHTML = getCWD(wd) + " @ " + ws + " km/h";
        document.getElementById("ws_color").style.backgroundColor = valToColor(ws,"ws");
        document.getElementById("tw_data").innerHTML = getCWD(wd_pbl) + " @ " + ws_pbl + " km/h";
        document.getElementById("tw_color").style.backgroundColor = valToColor(ws_pbl,"ws_pbl");
        document.getElementById("pbl_data").innerHTML = thePBL + " m";
        document.getElementById("pbl_color").style.backgroundColor = valToColor(thePBL,"hgt_pbl");
        document.getElementById("vr_data").innerHTML = theVR + " m<sup>2</sup>/s";
        document.getElementById("vr_color").style.backgroundColor = valToColor(theVR,"vrate");
 
      } else {  //blank RM picked
        document.getElementById("ws_data").innerHTML = "";
        document.getElementById("ws_color").style.backgroundColor = "#f8f8f8";
        document.getElementById("tw_data").innerHTML = "";
        document.getElementById("tw_color").style.backgroundColor = "#f8f8f8";
        document.getElementById("pbl_data").innerHTML = "";
        document.getElementById("pbl_color").style.backgroundColor = "#f8f8f8";
        document.getElementById("vr_data").innerHTML = "";
        document.getElementById("vr_color").style.backgroundColor = "#f8f8f8";
      }
    }

    function removeInfo() {
      document.getElementById("ws_data").innerHTML = "";
      document.getElementById("tw_data").innerHTML = "";
      document.getElementById("pbl_data").innerHTML = "";
      document.getElementById("vr_data").innerHTML = "";
      document.getElementById("ws_color").style.backgroundColor = "#f8f8f8";
      document.getElementById("tw_color").style.backgroundColor = "#f8f8f8";
      document.getElementById("pbl_color").style.backgroundColor = "#f8f8f8";
      document.getElementById("vr_color").style.backgroundColor = "#f8f8f8";      
    }


      //add legend to Surface Wind map
      var legend10m = L.control({position: 'bottomright'});
      legend10m.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
          grades = [40, 30, 20, 10, 8],
          labels = ['40 +','30-39','20-29','10-19','0-9 km/h'];

        div.innerHTML += "<strong>10 m Wind</strong><br>";
        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
         div.innerHTML +=
            '<i style="background:' + valToColor(grades[i] + 1,"ws") + '"></i> ' +
            (labels[i] ? labels[i] + '<br>' : '+');
        }
        return div;
      };
      legend10m.addTo(map1);


      //add legend to Transport Wind map
      var legendTW = L.control({position: 'bottomright'});
      legendTW.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
          grades = [80, 60, 40, 20, 10],
          labels = ['80 +','60-79','40-59','20-39','0-19 km/h'];

        div.innerHTML += "<strong>Transport Wind</strong><br>";
        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
         div.innerHTML +=
            '<i style="background:' + valToColor(grades[i] + 1,"ws_pbl") + '"></i> ' +
            (labels[i] ? labels[i] + '<br>' : '+');
        }
        return div;
      };
      legendTW.addTo(map2);


      //add legend to PBL map
      var legendPBL = L.control({position: 'bottomright'});
      legendPBL.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
          grades = [2000, 1500, 700, 300, 100],
          labels = ['2000 +','1500-1999', '700-1499','300-699','< 300 m'];

        div.innerHTML += "<strong>Mixing Layer</strong><br>";
        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
         div.innerHTML +=
            '<i style="background:' + valToColor(grades[i] + 1,"hgt_pbl") + '"></i> ' +
            (labels[i] ? labels[i] + '<br>' : '+');
        }
        return div;
      };
      legendPBL.addTo(map3);

      //add legend to VR map
      var legendVR = L.control({position: 'bottomright'});
      legendVR.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
          grades = [25001, 10000, 5000, 3000, 100],
          labels = ['Very High','Good','Fair','Marginal','Poor'];

        div.innerHTML += "<strong>Ventilation Rate</strong><br>";
        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
         div.innerHTML +=
            '<i style="background:' + valToColor(grades[i] + 1,"vrate") + '"></i> ' +
            (labels[i] ? labels[i] + '<br>' : '+');
        }
        return div;
      };
      legendVR.addTo(map4);

      function zoomToRM(rm) {
        console.log(rmdata);
        for (var i = 0; i < rmdata.features.length; i++) {
          var thisRM = rmdata.features[i].properties.MUNI_NAME;
          if (thisRM == rm) {
            console.log(thisRM);
            var minx = 180;
	    var maxx = -180;
	    var miny = 90;
	    var maxy = -90;

            for (var coord in rmdata.features[i].geometry.coordinates) {
              for (var x in rmdata.features[i].geometry.coordinates[coord]) {  //each coordinate pair
		//may be in a mutli-polygon, check if coordinate is still an array, and if so drill down one more level
		if (rmdata.features[i].geometry.coordinates[coord][x][0].constructor === Array) {
		  for (var y in rmdata.features[i].geometry.coordinates[coord][x]) {
		    var xcoord = rmdata.features[i].geometry.coordinates[coord][x][y][0];
		    var ycoord = rmdata.features[i].geometry.coordinates[coord][x][y][1];
		    if (xcoord > maxx) {maxx = xcoord;}
		    if (xcoord < minx) {minx = xcoord;}
		    if (ycoord > maxy) {maxy = ycoord;}
		    if (ycoord < miny) {miny = ycoord;}
                  }
                } else {
		  var xcoord = rmdata.features[i].geometry.coordinates[coord][x][0];
		  var ycoord = rmdata.features[i].geometry.coordinates[coord][x][1];
		  if (xcoord > maxx) {maxx = xcoord;}
		  if (xcoord < minx) {minx = xcoord;}
		  if (ycoord > maxy) {maxy = ycoord;}
		  if (ycoord < miny) {miny = ycoord;}
                }
              }
            }

 
            console.log(minx + " " + maxx);
            map1.fitBounds([[maxy, minx],[miny, maxx]]);
            
            break;
          }
        } 
      }

      var urlRM = decodeURI($_GET('rm'));
      if (urlRM) {
        zoomToRM(urlRM);
        document.getElementById("rmSelect").value = urlRM;
        populateInfo(urlRM);
        addChart(urlRM);
        highlightFeatureAllMaps(urlRM,geojson1);
        highlightFeatureAllMaps(urlRM,geojson2);
        highlightFeatureAllMaps(urlRM,geojson3);
        highlightFeatureAllMaps(urlRM,geojson4);

        resetHighlightAllMaps(geojson1);
        resetHighlightAllMaps(geojson2);
        resetHighlightAllMaps(geojson3);
        resetHighlightAllMaps(geojson4);

        lastRM = urlRM;
      }


//**************************************************************
      function addChart(rm) {
        document.getElementById("graph_container").innerHTML = "<svg id=\"graph\"></svg>";

        var margin = 45,
    width = parseInt(d3.select("#graph").style("width")) - margin*1.3,
    height = parseInt(d3.select("#graph").style("height")) - margin*2;

var xScale = d3.time.scale()
    .range([0, width])
    .nice(d3.time.hour);

var yScale = d3.scale.linear()
    .range([height, 0])
    .nice();

var xAxis = d3.svg.axis()
    .scale(xScale)
    .innerTickSize(-height)
    .outerTickSize(0)
    .tickPadding(10)
    .ticks(d3.time.days, 1)
    .tickFormat(d3.time.format("%a %I%p"))
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left")
    .innerTickSize(-width)
    .outerTickSize(0)
    .tickPadding(10);

var line = d3.svg.line()
    .interpolate("monotone")
    .x(function(d) { return xScale(d.valid_date); })
    .y(function(d) { return yScale(d.vrate); });

var graph = d3.select("#graph").append("svg")
    .attr("width", width + margin*1.3)
    .attr("height", height + margin*2)
  .append("g")
    .attr("transform", "translate(" + margin + "," + margin + ")");

  //get just the data for the seleced RM
  var data = [];

  //take the json object, and create a data array for the selected RM
  for(var i = 0; i < wxdata.length; i++) {
        var obj = wxdata[i];
        //console.log(obj);
        if (obj.muni_name == rm) {
          data.push(obj);
        }
      }

  data.forEach(function(d) {
    d.valid_date = moment(d.valid_date);
    d.vrate = +d.vrate;
  });


  xScale.domain(d3.extent(data, function(d) { return d.valid_date; }));
  yScale.domain([0,30000]);


  graph.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);
      //.selectAll("text")  
      //      .style("text-anchor", "end")
      //      .attr("dx", "-1.7em")
      //      .attr("dy", "-0em")
      //      .attr("transform", "rotate(-90)" );

  graph.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      //.attr("transform", "rotate(-90)")
      .attr("y", -16)
      .attr("dy", ".71em")
      .style("text-anchor", "start")
      .text("Ventilation Rate");

  graph.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);


  graph.append("linearGradient")
      .attr("id", "temperature-gradient")
      .attr("gradientUnits", "userSpaceOnUse")
      .attr("x1", 0).attr("y1", yScale(0))
      .attr("x2", 0).attr("y2", yScale(30000))
    .selectAll("stop")
      .data([
        {offset: "0%", color: "#555"},
        {offset: "7.83%", color: "#555"},
        {offset: "7.83%", color: "#ffffbf"},
        {offset: "15.6%", color: "#ffffbf"},
        {offset: "15.6%", color: "#a6d96a"},
        {offset: "23.5%", color: "#a6d96a"},
        {offset: "23.5%", color: "#1a9641"},
        {offset: "83.3%", color: "#1a9641"},
        {offset: "83.3", color: "#0d4b20"},
        {offset: "100%", color: "#0d4b20"}
      ])
    .enter().append("stop")
      .attr("offset", function(d) { return d.offset; })
      .attr("stop-color", function(d) { return d.color; });


  function resize() {
    var width = parseInt(d3.select("#graph").style("width")) - margin*1.3,
    height = parseInt(d3.select("#graph").style("height")) - margin*2;

    /* Update the range of the scale with new width/height */
    xScale.range([0, width]).nice(d3.time.hour);
    yScale.range([height, 0]).nice();

    /* Update the axis with the new scale */
    graph.select('.x.axis')
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    graph.select('.y.axis')
      .call(yAxis);

    /* Force D3 to recalculate and update the line */
    graph.selectAll('.line')
      .attr("d", line);
  }

  d3.select(window).on('resize', resize); 

  resize();
      }

