async function initMap() {
    const dublin = { lat: 53.3476326, lng: -6.266265 };
  
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerView } = await google.maps.importLibrary("marker");
  
    const map = new Map(document.getElementById("map"), {
        zoom: 13,
        center: dublin,
        mapId: "DEMO_MAP_ID",
    });
  
    try {
        const response = await fetch('/map');
        const data = await response.json();

        data.forEach(station => {
            const pos = { lat: station.lat, lng: station.lng };

            new google.maps.Marker({
                map: map,
                position: pos,
                title: station.title,
            });
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
let slideIndex = 0;
showSlides();


initMap();
