document.addEventListener('DOMContentLoaded', function() {
    populateStationSelect(); // populating the dropdown selection

    var stationsSelect = document.getElementById('stations-select');
    var stationHeader = document.getElementById('stationNumber');

    stationsSelect.addEventListener('change', function() {
        var selectedStationNumber = this.value; 
        console.log("Selected station number from dropdown:", selectedStationNumber);

        if (selectedStationNumber) {
            // ensuring the number is treated as a string
            var station = stations.find(s => s.number.toString() === selectedStationNumber);
            if (station) {
                stationHeader.innerText = "Station number: " + station.number; // Update the header var
                updateSidebarContent(station); // Update sidebar with selction
            } else {
                console.log("No station found with number:", selectedStationNumber);
                stationHeader.innerText = "Station number: "; // if the selection is not valid
                updateSidebarContent(null); 
            }
        } else {
            stationHeader.innerText = "Station number: "; // If dropdown is default
            updateSidebarContent(null); 
        }
    });
});

function updateSidebarContent(station) {

    var stationHeader = document.getElementById('stationNumber');
    var stationsSelect = document.getElementById('stations-select');

    if (station) {
        stationHeader.textContent = "Station number: " + station.number;
        stationsSelect.value = station.number; // Ensure dropdown is synchronized without reset
        document.getElementById("stationNumber").style.display = "block";
    } else {
        stationHeader.textContent = "";
        stationsSelect.value = ""; // Reset only if there's no station
        document.getElementById("stationNumber").style.display = "none";
    }

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
    clearMarkers();
}

document.getElementById('showHistoricalData').addEventListener('click', function() {
    displayPlot('historical');
});

document.getElementById('showPredictiveData').addEventListener('click', function() {
    displayPlot('predictive');
});


function displayPlot(type,station=null,mode=0) {
    var date;
    var stationNumber;
    var stationHeader = document.getElementById('stationNumber');

    if (station === null) {
        var selectElement = document.getElementById('stations-select');
        stationNumber = selectElement.value; // station number from the dropdown
        if (!stationNumber) {
            // If no station is selected, set it from the header if there is one
            var headerValue = stationHeader.innerText.split(': ')[1];
            if (headerValue) {
                selectElement.value = headerValue;
                stationNumber = headerValue;
            }
        } else {
            // Update the stationHeader if there is a selected option
            stationHeader.innerText = "Station number: " + stationNumber;
        }
        date = document.getElementById('dateInput').value;
    } else {
        stationNumber = station;
        stationHeader.innerText = "Station number: " + stationNumber; // update the header
        date = new Date();
        date = date.getFullYear() + "-" + (date.getMonth()+1) + "-" + date.getDate();
    }

    if (!date) {
        alert("Please select a date.");
        return;
    }

    let params = new URLSearchParams();
    params.append('date', date);

    if (type == 'predictive'){
        fetch(`/predictive_plot/${stationNumber}/${mode}`, {
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
            const plotImage2 = document.getElementById('plotImage2');
            const timestamp = new Date().getTime(); // Get current timestamp
            if (mode==0) {
                plotImage.src = `/static/images/bikes_predictions_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
                plotImage.style.display = 'block';
            
                plotImage2.src = `/static/images/stands_predictions_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
                plotImage2.style.display = 'block';
            } else {
                if (mode==1) {
                    plotImage.src = `/static/images/bikes_predictions_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
                    plotImage.style.display = 'block';
                } else if (mode==2) {
                    plotImage2.src = `/static/images/stands_predictions_plot.png?${timestamp}`; // Append timestamp to the image URL to make update the img
                    plotImage2.style.display = 'block';
                }
            }
            

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

const historicalStart = new Date(2024, 0, 19); 
const today = new Date();
const fiveDaysLater = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 5);

document.addEventListener('DOMContentLoaded', function() {
    populateStationSelect(); // populate dropdown

    flatpickr("#dateInput", {
        enableTime: false,
        dateFormat: "Y-m-d",
        minDate: historicalStart,
        maxDate: fiveDaysLater,
        onChange: function(selectedDates, dateStr, instance) {
            const selectedDate = new Date(dateStr);
            selectedDate.setHours(0, 0, 0, 0); // Normalize time component
            handleButtonVisibility(selectedDate);
        },
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const date = dayElem.dateObj;
            const currentDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
            const today = new Date();
            today.setHours(0, 0, 0, 0);
    
            // Apply 'current-day' class if it's the current date
            if (currentDate.getTime() === today.getTime()) {
                dayElem.classList.add("current-day");
            } else {
                // Otherwise, apply 'historical' or 'predictive' based on the date
                if (currentDate < today) {
                    dayElem.classList.add("historical");
                } else if (currentDate > today) {
                    dayElem.classList.add("predictive");
                }
            }
        }
    });

    stationsSelect.addEventListener('change', function() {
        const selectedDate = dateInput.value ? new Date(dateInput.value) : null;
        handleButtonVisibility(selectedDate);  //when station changes to make sure to handle the buttons
    });
    
    
});

function handleButtonVisibility(selectedDate) {
    const historicalButton = document.getElementById('showHistoricalData');
    const predictiveButton = document.getElementById('showPredictiveData');
    const stationsSelect = document.getElementById('stations-select');
    const selectedStationNumber = stationsSelect.value;  
    const today = new Date();
    today.setHours(0, 0, 0, 0);  

    // Checking if both a station and a date are selected
    if (selectedStationNumber && selectedDate) {
        if (selectedDate <= today) {
            historicalButton.style.display = 'block';
        } else {
            historicalButton.style.display = 'none';
        }

        if (selectedDate >= today && selectedDate <= fiveDaysLater) {
            predictiveButton.style.display = 'block';
        } else {
            predictiveButton.style.display = 'none';
        }
    } else {
        // Hiding both buttons if either the station or the date are selected
        historicalButton.style.display = 'none';
        predictiveButton.style.display = 'none';
    }
}




function populateStationSelect() {
    var select = document.getElementById('stations-select');
    select.innerHTML = '';

    var defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "Select a station";
    select.appendChild(defaultOption);

    stations.forEach(function(station) {
        var option = document.createElement('option');
        option.value = station.number;
        option.textContent = station.number + " - " + station.name;
        select.appendChild(option);
    });
}

