function updateSidebarContent(station) {

    var stationNumber = document.getElementById("stationNumber");
    stationNumber.textContent = "Station number: " + station.number;
    var dateInput = document.getElementById("dateInput");
    dateInput.value = ""; 


    var plotImage = document.getElementById("plotImage");
    plotImage.style.display = "none";
    var plotImage2 = document.getElementById("plotImage2");
    plotImage2.style.display = "none";

    var sidebar = document.getElementById("sidebar");
    var map = document.getElementById("map");
    var content = sidebar.querySelector('.sidebar-content');
    if (sidebar.style.width === "0px" || sidebar.style.width === "") {
        sidebar.style.width = "500px";
        map.style.marginLeft = "500px";
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
        sidebar.style.width = "500px";
        map.style.marginLeft = "500px";
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
    const stationNumber = document.getElementById('stationNumber').innerText.split(': ')[1];

    if (!date) {
        alert("Please select a date.");
        return;
    }

    let params = new URLSearchParams();
    params.append('date', date);

    fetch(`/predictive_plot/${stationNumber}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert('Failed to generate plot: ' + data.error);
            return;
        }
        const plotImage = document.getElementById('plotImage');
        const timestamp = new Date().getTime(); // Get current timestamp
        plotImage.src = `/static/images/bikes_predictions_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
        plotImage.style.display = 'block';

        const plotImage2 = document.getElementById('plotImage2');
        plotImage2.src = `/static/images/stands_predictions_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
        plotImage2.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to fetch predictive data. ' + error.message);
        document.getElementById('plotImage').style.display = 'none';
        document.getElementById('plotImage2').style.display = 'none';
    });
}


