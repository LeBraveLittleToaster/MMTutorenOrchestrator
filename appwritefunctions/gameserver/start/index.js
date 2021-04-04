const fetch = require('node-fetch');
const payload = JSON.parse(process.env.APPWRITE_FUNCTION_EVENT_PAYLOAD)
console.log(payload)
console.log(process.env.IP_ADDRESS)
fetch("http://" + process.env.IP_ADDRESS + "/appwrite/event/start")
.then(v => {
    console.log("Success")
}).catch(error => {
    console.log(error)
})