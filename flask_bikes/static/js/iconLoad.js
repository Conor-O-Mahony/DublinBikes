
document.addEventListener("DOMContentLoaded", function() {
    const city = "Dublin,IE";
    const api_key = "dd05f29b3c673dec7f4a9df4f8cce8fd";
    const units = "metric";
    const url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${api_key}&units=${units}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.weather && data.weather.length > 0) {
                const icon = data.weather[0].icon;
                const iconUrl = `http://openweathermap.org/img/wn/${icon}.png`;
                const button = document.querySelector('#weatherIcon button');
                button.innerHTML = `<img src="${iconUrl}" alt="Weather Icon" style="width: 40px; height: auto;">`; 
            }
        })
        .catch(error => console.error("Failed to load weather icon", error));
});