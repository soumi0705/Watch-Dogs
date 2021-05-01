const express = require('express');
const path = require('path');
const favicon = require('serve-favicon');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
var rootRoute = require('./root');
// var twnRoute = require('./township');
// var twnRoute = require('./township');
// var twnRoute = require('./township');
// var twnRoute = require('./township');
// var aboutRoute = require('./aboutus');
// var eventRoute = require('./event');
// var projectRoute = require('./project');
// Define our application
const app = express();
// Set 'port' value to either an environment value PORT or 5000
var port = 5000;
// Router listens on / (root)
app.use(bodyParser.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.use(express.static(__dirname + "/public"));
// Routes
app.use(rootRoute);
// app.use(aboutRoute);
// app.use(eventRoute);
// app.use(projectRoute);
app.listen(process.env.PORT || port, () => console.log(`App listening at http://localhost:${port}`))