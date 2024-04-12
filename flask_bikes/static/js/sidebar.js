function updateSidebarContent(station) {

    var stationNumber = document.getElementById("stationNumber");
    stationNumber.textContent = "Station number: " + station.number;
    var dateInput = document.getElementById("dateInput");
    dateInput.value = ""; 


    var plotImage = document.getElementById("plotImage");
    plotImage.style.display = "none";
    plotImage.src = "";

    var plotFilters = document.getElementById("plotFilters");
    plotFilters.style.display = "none";

    var sidebar = document.getElementById("sidebar");
    var map = document.getElementById("map");
    var content = sidebar.querySelector('.sidebar-content');
    if (sidebar.style.width === "0px" || sidebar.style.width === "") {
        sidebar.style.width = "250px";
        map.style.marginLeft = "250px";
        content.style.opacity = "1";
        content.style.pointerEvents = "auto";
    }
}

function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    var map = document.getElementById("map");
    var content = sidebar.querySelector('.sidebar-content');
    if (sidebar.style.width !== "0px" && sidebar.style.width !== "") {
        sidebar.style.width = "0";
        map.style.marginLeft = "0";
        content.style.opacity = "0";
        content.style.pointerEvents = "none";
    } else {
        sidebar.style.width = "250px";
        map.style.marginLeft = "250px";
        content.style.opacity = "1";
        content.style.pointerEvents = "auto";
    }
}



document.getElementById('showHistoricalData').addEventListener('click', function() {
    displayPlot('historical');
});

document.getElementById('showPredictiveData').addEventListener('click', function() {
    displayPlot('predictive');
});

function displayPlot(type) {
    const date = document.getElementById('dateInput').value;
    if (!date) {
        alert("Please select a date.");
        return;
    }

    const plotUrl = `/${type}_plot_${date}.png`; // URL has to be generated or fetched, this is just example
    document.getElementById('plotImage').src = plotUrl;
    document.getElementById('plotImage').style.display = 'block';
    document.getElementById('plotFilters').style.display = 'block';
}

function filterData(timeFrame) {
    // Update the plot based on the selected timeframe
    const date = document.getElementById('dateInput').value;
    const plotUrl = `/filtered_${timeFrame}_plot_${date}.png`; // Modify as needed
    document.getElementById('plotImage').src = plotUrl;
}


