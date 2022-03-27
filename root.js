var router = require("express").Router();
const request = require("request");
require("dotenv").config();

const apiKey = process.env.WEATHER_API_KEY;

router.get("/", function (req, res) {
  let city = "gurgaon";
  let url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`;
  request(url, function (err, response, body) {
    if (err) {
      res.render("index", {
        weather: null,
        error: "Error, please try again",
        AESKey: process.env.AES_KEY,
      });
    } else {
      let weather = JSON.parse(body);
      if (weather.main == undefined) {
        res.render("index", {
          weather: null,
          error: "Error, please try again",
          AESKey: process.env.AES_KEY,
        });
      } else {
        let weatherText = `It's ${weather.main.temp} degrees Celcius with ${weather.weather[0].main} in ${weather.name}!`;
        res.render("index", {
          weather: weatherText,
          error: null,
          AESKey: process.env.AES_KEY,
        });
      }
    }
  });
});
module.exports = router;
