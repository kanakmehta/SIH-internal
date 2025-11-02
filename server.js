// // server.js
// const express = require('express');
// const fetch = require('node-fetch'); // npm install node-fetch@2
// const cors = require('cors');

// const app = express();
// const PORT = 3000;

// app.use(cors());

// const API_KEY = '06e285a46caaecd8e1e626caa69446f7';

// app.get('/weather', async (req, res) => {
//     const city = req.query.city ? `${encodeURIComponent(req.query.city)},IN` : 'Yamuna Nagar,IN';
//     const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

//     try {
//         const response = await fetch(url);
//         if (!response.ok) {
//             return res.status(400).json({ error: `OpenWeatherMap API error: ${response.statusText}` });
//         }
//         const data = await response.json();
//         const weather = {
//             city: `${data.name}, ${data.sys.country}`,
//             temperature: data.main.temp,
//             feels_like: data.main.feels_like,
//             condition: data.weather[0].main,
//             humidity: data.main.humidity,
//             wind: data.wind.speed,
//             pressure: data.main.pressure
//         };
//         res.json(weather);
//     } catch (err) {
//         res.status(500).json({ error: 'Failed to fetch weather', details: err.message });
//     }
// });

// app.listen(PORT, () => console.log(`Weather server running on http://localhost:${PORT}`));






// server.js
const express = require('express');
const fetch = require('node-fetch'); // npm install node-fetch@2
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());

// 🔹 Serve static files
app.use(express.static(path.join(__dirname, 'frontend')));

// 🔹 Default route -> open login.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'login.html'));
});

// 🔹 Weather API route
const API_KEY = '06e285a46caaecd8e1e626caa69446f7';

app.get('/weather', async (req, res) => {
    const city = req.query.city ? `${encodeURIComponent(req.query.city)},IN` : 'Yamuna Nagar,IN';
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            return res.status(400).json({ error: `OpenWeatherMap API error: ${response.statusText}` });
        }
        const data = await response.json();
        const weather = {
            city: `${data.name}, ${data.sys.country}`,
            temperature: data.main.temp,
            feels_like: data.main.feels_like,
            condition: data.weather[0].main,
            humidity: data.main.humidity,
            wind: data.wind.speed,
            pressure: data.main.pressure
        };
        res.json(weather);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch weather', details: err.message });
    }
});

// 🔹 Start server
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
