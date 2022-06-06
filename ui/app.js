const express = require("express");
const ejs = require("ejs");
const fetch = require("node-fetch");

const app = express();

app.set("view engine", "ejs");

app.use(express.urlencoded({ extended: true }));
// app.use(express.static("public"));
app.use(express.static(__dirname + "/public"));

app.get("/", function (req, res) {
  res.render("home", {});
});

app.get("/checkIp", function (req, res) {
  res.render("checkIp", { is_ip: false });
});

app.get("/honeypot", function (req, res) {
  fetch("http://192.168.43.98:8000/get-honeypot-log")
    .then((response) => response.json())
    .then((json) => {
      // console.log(json);
      const data = eval(json); //converting json to js obj
      // console.log(data);                                         //json data obj
      // console.log(Object.keys(data)[1]);                         //timestamp
      // console.log(data[Object.keys(data)[1]]["IP"]);     //IP
      // console.log(data["2022-04-16 14:38:26.293472"]["MAC"]);    //MAC
      res.render("honeypot", { data: data });
    });
});

app.get("/serverLogger", function (req, res) {
  fetch("http://192.168.43.98:8000/get-server-log")
    .then((response) => response.json())
    .then((json) => {
      const data = eval(json);

      res.render("serverLogger", { data: data });
    });
});

//post routes

app.post("/searchIp", async function (req, res) {
  // event.preventDefault();
  // console.log(req.body);
  const ip_add = req.body.ip;
  fetch(`http://192.168.43.98:8000/detect-proxy/${ip_add}`)
    .then((response) => response.json())
    .then((json) => {
      // console.log(json);
      
      if (json.is_proxy) {

        async function call() {
          const [proxy_details, ip_details] = await Promise.all([
            fetch(`http://192.168.43.98:8000/proxy-details/${ip_add}`),
            fetch(`http://192.168.43.98:8000/ip-details/${ip_add}`)
          ]);
          const proxy_detail = await proxy_details.json();
          const ip_detail = await ip_details.json();
          return [proxy_detail, ip_detail];
        }
        call().then(([proxy_detail, ip_detail]) => {
          res.render("checkIp", {
            is_ip: true,
            ip_details: ip_detail,
            proxy_details: proxy_detail,
          });
        }).catch(error => {
          // /movies or /categories request failed
        });

          
          
      } else {
        fetch(`http://192.168.43.98:8000/ip-details/${ip_add}`)
          .then((response) => response.json())
          .then((json) => {
            // console.log(json);
            res.render("checkIp", { is_ip: true, ip_details: json });
          });
      }
    })
    .catch((err) => console.log(err));
});

app.listen(3001,'192.168.43.98');
console.log("LISTENING ON PORT 3001....");

