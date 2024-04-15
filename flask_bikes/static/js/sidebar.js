function updateSidebarContent(station) {

    var stationNumber = document.getElementById("stationNumber");
    stationNumber.textContent = "Station number: " + station.number;
    var dateInput = document.getElementById("dateInput");
    dateInput.value = ""; 


    var plotImage = document.getElementById("plotImage");
    plotImage.style.display = "none";
    var plotImage2 = document.getElementById("plotImage2");
    plotImage2.style.display = "none";

    var plotHist = document.getElementById("plotHist");
    plotHist.style.display = "none";
    var plotHist2 = document.getElementById("plotHist2");
    plotHist2.style.display = "none";

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

    if (type == 'predictive'){
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
                alert('Failed to generate predictive plot: ' + data.error);
                return;
            }

            document.getElementById('plotHist').style.display = 'none';
            document.getElementById('plotHist2').style.display = 'none';
            
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
    if (type == 'historical') {
        fetch(`/historical_plot/${stationNumber}`, {
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
                alert('Failed to generate historical plot: ' + data.error);
                return;
            }

            document.getElementById('plotImage').style.display = 'none';
            document.getElementById('plotImage2').style.display = 'none';

            const plotHist = document.getElementById('plotHist');
            const timestamp = new Date().getTime(); // Get current timestamp
            // Appending timestamp to the image url to update the img, this will make sure the image changes everytime
            plotHist.src = `/static/images/bikes_historical_plot.png?${timestamp}`;
            plotHist.style.display = 'block';
    
            const plotHist2 = document.getElementById('plotHist2');
            plotHist2.src = `/static/images/stands_historical_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
            plotHist2.style.display = 'block';

        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to fetch historical data. ' + error.message);
            document.getElementById('plotHist').style.display = 'none';
            document.getElementById('plotHist2').style.display = 'none';
        });
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const historicalStart = new Date(today.getFullYear(), 1, 19); // february is 1 
    const fiveDaysLater = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 5); // until the next 5 days 

    // Using flatpickr library to customise the calendar (imported the scripts in the map.html)

    flatpickr("#dateInput", {
        enableTime: false,
        dateFormat: "Y-m-d",
        disable: [
            function(date) {
                return (date < historicalStart || date > fiveDaysLater);
            }
        ],
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const date = dayElem.dateObj;
            const currentDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

            if (currentDate >= historicalStart && currentDate <= today) {
                dayElem.classList.add("historical");
            } else if (currentDate > today && currentDate <= fiveDaysLater) {
                dayElem.classList.add("predictive");
            }
        }
    });
});

