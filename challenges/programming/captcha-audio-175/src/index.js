var express = require('express')
const uuidV4 = require('uuid/v4');
var path = require("path");
var session = require('express-session');
var timestamp = require('unix-timestamp');
var fs = require('fs');
var config = require(path.resolve(path.join(__dirname, './', 'config.js')));
var app = express();
app.use(session({
    secret: 'secretInSecurity',
    resave: true,
    saveUninitialized: true,
}));
var sess;
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(express.static('public'));

const captchaFilesDirectory = fs.readdirSync('./captchaFiles')
    .map(file => {
        return path.join('./captchaFiles', file);
    });


app.get('/', function(req, res) {
    sess = req.session;
    res.sendFile(path.join(__dirname + '/index.html'));
})

app.get('/captcha', function(req, res) {
    sess = req.session;
    var fileIndex = Math.floor(Math.random() * (captchaFilesDirectory.length - 1));
    var fileName = captchaFilesDirectory[fileIndex]
    sess.value = fileName.substring(13, fileName.length - 4);
    console.log(sess.value);
    session.timeSent = timestamp.now();
    res.sendFile(path.join(__dirname + '/' + fileName));
})
app.get('/debug', function(req, res) {
    sess = req.session;
    res.sendFile(path.join(__dirname + '/audioFiles.zip'));
})
app.post('/submit', function(req, res) {
    var valueCaptcha = req.body.captcha;
    sess = req.session;
    if (sess.value && (valueCaptcha == sess.value)) {
        if (timestamp.now("-5s") <= session.timeSent) {
            res.send(config.flag);
        } else {
            req.session.destroy();
            res.send("You're too long <script>setTimeout(function() {window.location.replace(\"/\")}, 2000);</script>");
        }
    } else {
        req.session.destroy();
        res.send("You're a robot <script>setTimeout(function() {window.location.replace(\"/\")}, 2000);</script>");
    }
})

app.listen(8070, function() {
    console.log('captcha running on port 8070')
})
