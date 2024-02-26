async function initMap() {

  const dublin = { lat: 53.3476326, lng: -6.266265 };

  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

  const map = new Map(document.getElementById("map"), {
    zoom: 13,
    center: dublin,
    mapId: "DEMO_MAP_ID",
  });

  const pos = { lat: 53.345159, lng: -6.267393 }

  const marker = new AdvancedMarkerView({
    map: map,
    position: pos,
    title: "station1",
  });
}

initMap();