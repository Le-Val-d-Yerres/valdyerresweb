// variables global
var nbreEvenement = 0;
var zoom=16;
var listeMarkers = new Array(2);
var feature;
var map;
var controls;

for (var j = 0; j <= 20; j++)
{
	listeMarkers[j] = [' ', ' '];
}


// Corrdonnées GPS du centre de l'agglo (gare RER de Brunoy)
var aggloGPS = [];
aggloGPS['longitude'] = 2.50706;
aggloGPS['latitude'] = 48.698867;

var feature = [];
    
function map_init()
{
	OpenLayers.Lang.setCode("fr");
   	map = new OpenLayers.Map("map");
	var osm = new OpenLayers.Layer.OSM();            
    var gmap = new OpenLayers.Layer.Google("Google Streets");
    
    map.addLayers([osm, gmap]);

    map.addControl(new OpenLayers.Control.LayerSwitcher());
	
	epsg4326 =  new OpenLayers.Projection("EPSG:4326"); //WGS 1984 projection
	projectTo = map.getProjectionObject(); //The map projection (Spherical Mercator)
		  
    var vectorLayer = new OpenLayers.Layer.Vector("Evènements");
    
    for (i=1;i<=nbreEvenement;i++)
    {
    	feature = new OpenLayers.Feature.Vector(
			new OpenLayers.Geometry.Point( listeMarkers[i]['longitude'], listeMarkers[i]['latitude'] ).transform(epsg4326, projectTo),
			{description: listeMarkers[i]['description']} ,
			{externalGraphic: '/static/js/openstreetmap/img/'+listeMarkers[i]['marker']+'.png', graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
		);
	
    	vectorLayer.addFeatures(feature);
    }
    
    if (nbreEvenement > 1)
	{
		var lonLat = new OpenLayers.LonLat( aggloGPS['longitude'], aggloGPS['latitude'] ).transform(epsg4326, projectTo);
		zoom=12;
	}
	else
	{
		var lonLat = new OpenLayers.LonLat( listeMarkers[1]['longitude'], listeMarkers[1]['latitude'] ).transform(epsg4326, projectTo);
	}

	map.setCenter (lonLat, zoom);
		   
	map.addLayer(vectorLayer);
		 
		    
	//Add a selector control to the vectorLayer with popup functions
	controls = {
		selector: new OpenLayers.Control.SelectFeature(vectorLayer, { onSelect: createPopup, onUnselect: destroyPopup })
	};
	
	map.addControl(controls['selector']);
	controls['selector'].activate();
}


function nouveauMarker(lon, lat, desc, marker)
{
	nbreEvenement++;
	listeMarkers[nbreEvenement]['longitude'] = lon;
	listeMarkers[nbreEvenement]['latitude'] = lat;
	listeMarkers[nbreEvenement]['description'] = desc;		 	
	listeMarkers[nbreEvenement]['marker'] = marker;
}

function createPopup(feature) 
{
	feature.popup = new OpenLayers.Popup.FramedCloud("pop",
		feature.geometry.getBounds().getCenterLonLat(),
		null,
		'<div class="markerContent">'+feature.attributes.description+'</div>',
		 null,
		true,
		function() { controls['selector'].unselectAll(); }
	);
	
	//feature.popup.closeOnMove = true;
	map.addPopup(feature.popup);
}
		
function destroyPopup(feature) {
	feature.popup.destroy();
	feature.popup = null;
}
