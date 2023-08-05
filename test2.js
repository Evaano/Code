document.getElementById("weatherForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const cityInput = document.getElementById("cityInput").value;
    console.log("City Input:", cityInput); // Add this line to check the value of cityInput
    fetchWeatherData(cityInput);
});

function fetchWeatherData(city) {
    console.log("Fetching weather data for city:", city); // Add this line to check the value of city
    const url = `/get_weather?city=${city}`;
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            console.log("Weather API Response:", data); // Add this line to check the API response
            if (data.error) {
                document.getElementById("weatherInfo").textContent = data.error;
            } else {
                const weather = data.weather;
                const temperature = data.temperature;
                document.getElementById("weatherInfo").innerHTML = `
                    <p>The weather in ${city} is: ${weather}</p>
                    <p>The temperature in ${city} is ${temperature.toFixed(2)}Â°C</p>
                `;
            }
        })
        .catch((error) => {
            console.log("Fetch Error:", error); // Add this line to check any fetch errors
            document.getElementById("weatherInfo").textContent = "Error: Unable to fetch data. Please try again later.";
        });
}