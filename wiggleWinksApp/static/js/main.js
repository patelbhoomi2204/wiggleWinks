
const err=document.querySelector(".error");
const options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};
function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
}
function showPosition() {
  if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
          var positionInfo = "Your current position is (" + "Latitude: " + position.coords.latitude + ", " + "Longitude: " + position.coords.longitude + ")";
          document.querySelector(".error").innerHTML = positionInfo;
      }, error, options);
  } else {
      alert("Sorry, your browser does not support HTML5 geolocation.");
  }
}

function getLatLngByZipcode(zipcode) {
    var geocoder = new google.maps.Geocoder();
    var address = zipcode;
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            alert("Latitude: " + latitude + "\nLongitude: " + longitude);
        } else {
            alert("Request failed.")
        }
    });
    return [latitude, longitude];
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition,showError);
  } else {
    err.innerHTML="Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  const lat=position.coords.latitude,
        lon=position.coords.longitude;
  document.querySelector(".form-lat-ip").value = lat;
  document.querySelector(".form-lon-ip").value = lon;
  document.querySelector(".form-lat-lon").classList.remove("form-lat-lon");
}

function showError(error)
  {
  switch(error.code)
    {
    case error.PERMISSION_DENIED:
      err.innerHTML="User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      err.innerHTML="Location information is unavailable."
      break;
    case error.TIMEOUT:
      err.innerHTML="The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      err.innerHTML="An unknown error occurred."
      break;
    }
  }

  document.querySelector(".btn-lcn").addEventListener('click', function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
      err.innerHTML="Geolocation is not supported by this browser.";
    }
  });