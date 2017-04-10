var express = require('express');
var webshot = require('webshot');
const uuidV4 = require('uuid/v4');
var validUrl = require('valid-url');
var path = require("path");
var request = require('request');

var config = require(path.resolve(path.join(__dirname, './', 'config.js')));
var app = express();
app.use(express.static('public'));

var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/getname.html'));
})

app.post('/screen', function(req, res) {
    var nameUrl = req.body.name;
    if (nameUrl && nameUrl != "" && validUrl.isUri(nameUrl)) {
        if (nameUrl.search("protocolunlimited14.fr") != -1) {
            res.send(JSON.stringify({
                location: config.flag
            }));
        } else {
            var captcha = req.body.captcha;
            if (captcha && captcha != "") {
                request.post({
                    url: 'https://www.google.com/recaptcha/api/siteverify',
                    form: {
                        secret: config.captchaKey,
                        response: captcha
                    }
                }, function(error, response, body) {
                    if (!error) {
                        console.log(body);
                        var resultParsed = JSON.parse(body);
                        if (resultParsed.success) {
                            var name = uuidV4() + ".png";
                            webshot(nameUrl, "public/" + name, function(err) {
                                res.setHeader('Content-Type', 'application/json');
                                if (err) {
                                    res.send(JSON.stringify({
                                        location: "default/err.png"
                                    }));
                                } else {
                                    res.send(JSON.stringify({
                                        location: name
                                    }));
                                }
                            });
                        }
                    } else {
                        res.send("Nice try");
                    }
                });
            } else {
                res.send("Nice try");
            }
        }
    }else {
        res.send("Nice try");
    }
});

app.put('/', function(req, res) {
    res.send('Meeting Date :  Wed, 08 Nov 2017 12:00:00 CET \n     hashResult=int(hashlib.sha1(str(currentTime)).hexdigest(), 16) % (10 ** 9)\
        \nposWord1=hashResult//(10**6)\
        \nposWord2=(hashResult % (10**6))//(10**3)\
        \nposWord3=hashResult % (10**3)\
        \nresultDomain = \'http://\'+result[posWord1%300].lower()+....')
})

app.delete('/', function(req, res) {
    res.send('DGA uses sha1 function and I prefer 9 figures in a row')
})

app.listen(8060, function() {
    console.log('DGA running on port 8060')
})
