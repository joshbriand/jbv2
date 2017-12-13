//openweathermap API Key
var openWeatherMapKey = '2fd4f5a71f1a3c588985e3e6bee9335a';

//array of individual brewery objects
var breweries = [{
		name: '33 Acres Brewing Co.',
		address: '15 W 8th Ave.',
		city: 'Vancouver',
		phone: '604-620-4589',
		website: 'http://www.33acresbrewing.com'
	},

	{
		name: 'Andina Brewing Company',
		address: '1507 Powell St',
		city: 'Vancouver',
		phone: '604-253-2400',
		website: 'http://www.andinabrewing.ca'
	},

	{
		name: 'Bridge Brewing Company',
		address: '1448 Charlotte Rd.',
		city: 'North Vancouver',
		phone: '604-770-2739',
		website: 'http://www.bridgebrewing.com'
	},

	{
		name: 'Dageraad Brewing',
		address: '114–3191 Thunderbird Cr.',
		city: 'Burnaby',
		phone: '604-420-2050',
		website: 'http://www.dageraadbrewing.com'
	},

	{
		name: 'Deep Cove Brewers And Distillers',
		address: '170–2270 Dollarton Hwy.',
		city: 'North Vancouver',
		phone: '604-770-1136',
		website: 'http://www.deepcovecraft.com'
	},

	{
		name: 'Fuggles & Warlock Craftworks',
		address: '103-11220 Horseshoe Way',
		city: 'Richmond',
		phone: '604-285-7745',
		website: 'http://www.fuggleswarlock.com'
	},

	{
		name: 'Luppolo Brewing Company',
		address: '1123 Venables St',
		city: 'Vancouver',
		website: 'http://www.luppolobrewing.ca'
	},

	{
		name: 'Red Truck Beer Company',
		address: '295 East 1st Ave.',
		city: 'Vancouver',
		phone: '604-682-4733',
		website: 'http://www.redtruckbeer.com'
	},

	{
		name: 'Steamworks Brewing Company',
		address: '3845 William St.',
		city: 'Burnaby',
		phone: '604-620-7250',
		website: 'http://www.steamworks.com'
	},

	{
		name: 'Steel & Oak Brewing Co.',
		address: '1319 Third Ave.',
		city: 'New Westminster',
		phone: '604-540-6495',
		website: 'http://www.steelandoak.ca'
	},

	{
		name: 'Storm Brewing Ltd.',
		address: '310 Commercial Dr.',
		city: 'Vancouver',
		phone: '604-255-9119',
		website: 'http://www.stormbrewing.org'
	}
];

//declare empty array of cities
var cities = [];

//create array of unique cities by iterating over each element in brewery array
for (x = 0; x < breweries.length; x++) {
	var flag = true;
	for (y = 0; y < cities.length; y++) {
		if (cities[y] == breweries[x].city) {
			flag = false;
		}
	}
	if (flag === true) {
		cities.push(breweries[x].city);
	}
}

//sort cities alphabeticallly
cities.sort();

//add 'Select All' to start of cities array
cities.unshift('Select All');

//class to represent a city and the breweries in that city
function City(name, breweries) {
	var self = this;
	self.name = name;
	self.breweries = breweries;
};

//declare array to be used to store City objects
var cityList = [];

//declare array to be used to temporarily store brewery objects until they are
//pushed into the proper City object in the cityList array
var breweryList = [];

//iterate over array of cities and array of breweries
//for each city create City object
//for each brewery, add to City object
for (x = 0; x < cities.length; x++) {
	for (y = 0; y < breweries.length; y++) {
		if (breweries[y].city == cities[x]) {
			breweryList.push(breweries[y]);
		}
	}
	cityList.push(new City(cities[x], breweryList));
	breweryList = [];
}

function mapError() {
	alert('Error loading Google Maps API.  Please try reloading the page.');
};



var ViewModel = function() {
	var self = this;

	//array of cities that have been checked
	self.citiesFiltered = ko.observableArray([]).extend({
		rateLimit: 50
	});

	//array of breweries that have been checked
	self.breweriesFiltered = ko.observableArray([]).extend({
		rateLimit: 50
	});

	//array of markers that appear on map
	self.markers = ko.observableArray([]);

	//variable to store infoWindow
	self.infoWindow = ko.observable();

	//variable to store weather for current marker
	self.weather = ko.observable();

	//variables used to show or hide the sidebar when in mobile mode
	self.showOrHide = ko.observable('<-');
	self.sidebarDisplay = ko.observable();
	self.mapWidth = ko.observable();

	//variables to track where map should be centered
	self.avgLat = ko.observable(0);
	self.avgLng = ko.observable(0);
	self.visibleMarkers = ko.observable(0).extend({
		rateLimit: 1000
	});

	//function to add city to filtered list
	self.addCity = function(city) {
		if (city != 'Select All') {
			if (self.citiesFiltered().indexOf(city.name) == -1) {
				self.citiesFiltered.push(city.name);
			}
			for (breweryIndex = 0; breweryIndex < city.breweries.length; breweryIndex++) {
				self.addBrewery(city.breweries[breweryIndex]);
			}
		} else {
			self.citiesFiltered.push(city);
		}
	};

	//function to add brewery to filtered list
	self.addBrewery = function(brewery) {
		if (self.breweriesFiltered().indexOf(brewery) == -1) {
			self.breweriesFiltered.push(brewery);
		}
	};

	//function to remove city from filtered list
	self.removeCity = function(city) {
		self.citiesFiltered.remove(city);
		for (breweryIndex = self.breweriesFiltered().length - 1; breweryIndex >= 0; breweryIndex--) {
			if (self.breweriesFiltered()[breweryIndex].city == city) {
				self.removeBrewery(self.breweriesFiltered()[breweryIndex]);
			}
		}
	};

	//function to remove brewery from filtered list
	self.removeBrewery = function(brewery) {
		if (self.breweriesFiltered().indexOf(brewery) != -1) {
			self.breweriesFiltered.remove(brewery);
			self.hideBrewery(brewery);
		}
	};

	//function containing logic of city checklist
	self.cityBoxClicked = function(value) {
		if (value.name == 'Select All') {
			//criteria: select all is checked
			//effect: add all cities to citiesFiltered array and add all breweries to
			//breweriesFiltered array
			if (self.citiesFiltered().indexOf('Select All') != -1) {
				for (cityIndex = 0; cityIndex < cityList.length; cityIndex++) {
					self.addCity(cityList[cityIndex]);
				}
			}
			//criteria: select all is unchecked
			//effect: citiesFiltered array is emptied (all city checkboxes unselected)
			else if (self.citiesFiltered().indexOf('Select All') == -1) {
				for (cityIndex = self.citiesFiltered().length - 1; cityIndex >= 0; cityIndex--) {
					self.removeCity(self.citiesFiltered()[cityIndex]);
				}
			}
		} else if (value.name != 'Select All') {
			//criteria: a city checkbox is unselected when all city checkboxes and
			//select all are selected
			//effect: unselect select all checkbox
			if (self.citiesFiltered().indexOf('Select All') != -1 & self.citiesFiltered().length < cityList.length) {
				self.removeCity('Select All');
				self.removeCity(value.name);
			}
			//criteria: city checkbox is selected and value is not select all
			//effect: add breweries in city to breweriesFiltered array
			else if (self.citiesFiltered().indexOf(value.name) != -1) {
				if (self.citiesFiltered().length == cityList.length - 1) {
					self.addCity('Select All');
				}
				self.addCity(value);
			}
			//criteria: city is unchecked and is not select all
			//effect: remove breweries in city from breweriesFiltered array
			else if (self.citiesFiltered().indexOf(value.name) == -1) {
				self.removeCity(value.name);
			}
		}
	};

	//function that hides any marker associated with argument
	self.hideBrewery = function(brewery) {
		for (z = 0; z < self.markers().length; z++) {
			if (self.markers()[z].title == brewery.name) {
				self.avgLat(self.avgLat() - self.markers()[z].getPosition().lat());
				self.avgLng(self.avgLng() - self.markers()[z].getPosition().lng());
				self.visibleMarkers(self.visibleMarkers() - 1);
				self.markers()[z].setVisible(false);
			}
		}
	};

	//function that calculates center of map
	self.getAvgCoords = function() {
		var acgCoords = {};
		if (self.visibleMarkers() === 0) {
			avgCoords = {
				lat: 49.25940993636364,
				lng: -123.03965151818183
			};
		} else {
			var lat = self.avgLat() / self.visibleMarkers();
			var lng = self.avgLng() / self.visibleMarkers();
			avgCoords = {
				lat,
				lng
			};
		}
		return avgCoords;
	};

	//function that retrieves JSON data from openweathermap
	self.getWeather = function(marker, brewery) {
		var lat = marker.position.lat();
		var lng = marker.position.lng();
		var urlString = 'http://api.openweathermap.org/data/2.5/weather?lat=' +
			lat +
			'&lon=' +
			lng +
			'&appid=' +
			openWeatherMapKey +
			'&units=metric';
		$.getJSON(urlString, function(data) {
			self.weather(data);
			self.addInfoWindow(marker, brewery);
		})
		.error(function() {
			self.weather('weather data unavailable');
			self.addInfoWindow(marker, brewery);
		});
	};

	//function to create and display info window on map
	self.addInfoWindow = function(marker, brewery) {
		if (typeof self.infoWindow() === 'object') {
			self.infoWindow().anchor.setAnimation(null);
			self.infoWindow().close();
			self.infoWindow ('');
		};
		marker.setAnimation(google.maps.Animation.BOUNCE);
		var weatherInfo = '';
		if (self.weather() === 'weather data unavailable') {
			weatherInfo = 'weather data unavilable';
		} else {
			var sunset = new Date(self.weather().sys.sunset*1000);
			var sunrise = new Date(self.weather().sys.sunrise*1000);
			//sunset = sunset.format('hh:MM:ss');
			//sunrise = sunrise.format('hh:MM:ss');
			weatherInfo = 'Current Temperature(c): ' +
				self.weather().main.temp +
				'<br>Sunrise (PST): ' + sunrise.getHours() + ':' + sunrise.getMinutes() + ':' + sunrise.getSeconds() +
				'<br>Sunset (PST): ' + sunset.getHours() + ':' + sunset.getMinutes() + ':' + sunset.getSeconds();
		};
		var contentString = '<div>' +
			'<h3>' + brewery.name + '</h3>' +
			'<br>' + brewery.address + '<br>' +
			brewery.city + ' , BC' + '<br>' +
			brewery.phone + '<br><a href ="' +
			brewery.website + '" target="_blank">' + brewery.website +
			'</a><br>' + weatherInfo;
		self.infoWindow(new google.maps.InfoWindow({
			content: contentString
			}));
		self.infoWindow().open(self.map, marker);
		google.maps.event.addListener(self.infoWindow(), 'closeclick', function() {
			marker.setAnimation(null);
		});
	};

	//function to show or hide the sidebar when site is viewed on a mobile device
	self.sidebarClicked = function() {
		if (self.showOrHide() == '<-') {
			self.sidebarDisplay('none');
			self.mapWidth('calc(100% - 2em)');
			self.showOrHide('->');
			self.recenterMap();
		} else {
			self.sidebarDisplay('inline');
			self.mapWidth('calc(100% - 65% - 2em)');
			self.showOrHide('<-');
		}
		google.maps.event.trigger(map, 'resize');
	};

	//function to recenter map when in mobile mode
	self.recenterMap = function() {
		var bounds = self.map.getBounds();
		self.map.fitBounds(bounds);
		var avgCoords = self.getAvgCoords();
		self.map.setCenter(avgCoords);
	};

	//function that displays info window when brewery name is clicked in sidebar
	self.breweryNameClicked = function(value) {
		for (c = 0; c < self.markers().length; c++) {
			if (self.markers()[c].id == value.name) {
				self.getWeather(self.markers()[c], value);
			}
		}
	};

	//function that adds marker to map when brewery added to breweries filtered list
	//function also checks to see that at least one brewery in a city is checked, if not
	//it removes that city from the citiesFiltered list
	self.breweriesFiltered.subscribe(function() {
		for (f = 0; f < self.breweriesFiltered().length; f++) {
			var alreadyExists = false;
			for (m = 0; m < self.markers().length; m++) {
				if (self.breweriesFiltered()[f].name == self.markers()[m].title) {
					alreadyExists = true;
					if (self.markers()[m].visible === false) {
						self.avgLat(self.avgLat() + self.markers()[m].getPosition().lat());
						self.avgLng(self.avgLng() + self.markers()[m].getPosition().lng());
						self.visibleMarkers(self.visibleMarkers() + 1);
						self.markers()[m].setVisible(true);
						self.markers()[m].setAnimation(google.maps.Animation.DROP);
					}
				}
			}
			if (alreadyExists === false) {
				brewery = self.breweriesFiltered()[f];
				if (typeof google === 'object' && typeof google.maps === 'object') {
					self.createMarker(brewery);
				} else {
					setTimeout(location.reload.bind(location), 750);
				}
			}
		}
		for (c = 0; c < self.citiesFiltered().length; c++) {
			var cityCheck = false;
			for (b = 0; b < self.breweriesFiltered().length; b++) {
				if (self.breweriesFiltered()[b].city == self.citiesFiltered()[c]) {
					cityCheck = true;
				}
			}
			if (cityCheck === false && self.citiesFiltered()[c] !== 'Select All') {
				self.citiesFiltered.remove(self.citiesFiltered()[c]);
			}
		}
	});

	//adds a listener to a marker
	self.addMarkerListener = function(marker) {
		google.maps.event.addListener(marker, 'click', function() {
			for (breweryIndex = 0; breweryIndex < self.breweriesFiltered().length; breweryIndex++) {
				if (self.breweriesFiltered()[breweryIndex].name === marker.title){
					var brewery = self.breweriesFiltered()[breweryIndex];
					self.getWeather(marker, brewery);
				}
			}
		});
	};

	//function to call getAvgCoords to get center of map and then recenters map
	//also gets weather for average co-ordinates
	self.visibleMarkers.subscribe(function() {
		var avgCoords = self.getAvgCoords();
		self.map.setCenter(avgCoords);
	});

	//function that adds new markers coordinates to avgLag and avgLng, increases visibleMarkers by one
	//adds the marker to the map and sets up an event listener on the marker
	self.markers.subscribe(function() {
		for (x = 0; x < self.markers().length; x++) {
			if (self.markers()[x] !== null && self.markers()[x].getMap() === undefined) {
				self.avgLat(self.avgLat() + self.markers()[x].getPosition().lat());
				self.avgLng(self.avgLng() + self.markers()[x].getPosition().lng());
				self.visibleMarkers(self.visibleMarkers() + 1);
				self.markers()[x].setMap(self.map);
				self.addMarkerListener(self.markers()[x]);
			}
		}
	});

	//function to initialize map and create markers
	initMap = function() {
		//function to geocode brewery address and create marker
		self.createMarker = function(brewery) {
			var geocoder = new google.maps.Geocoder();
			geocoder.geocode({
				address: brewery.address + ', ' + brewery.city + ', BC, Canada'
			}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					var marker = new google.maps.Marker({
						title: brewery.name,
						id: brewery.name,
						animation: google.maps.Animation.DROP,
						position: {
							lat: results[0].geometry.location.lat(),
							lng: results[0].geometry.location.lng()
						}
					});
					self.markers.push(marker);
				} else {
					console.log(status);
				}
			});
		};

		self.map = new google.maps.Map(document.getElementById('map'), {
			center: {
				lat: 49.25940993636364,
				lng: -123.0396515181818
			},
			zoom: 11
		});
		google.maps.event.trigger(map, 'resize');
	};
};


ko.applyBindings(new ViewModel());

