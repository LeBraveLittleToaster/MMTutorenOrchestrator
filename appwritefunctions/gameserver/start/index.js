const sdk = require('node-appwrite')
const fetch = require('node-fetch');
const payload = JSON.parse(process.env.APPWRITE_FUNCTION_EVENT_PAYLOAD)
console.log(payload)
if (payload.$collection == process.env.SESSION_COL_ID) {

    let client = new sdk.Client();
    client
        .setEndpoint("https://" + process.env.APPWRITE_API_ENDPOINT + "/v1")
        .setProject(process.env.APPWRITE_PROJECT_ID)
        .setKey(process.env.APPWRITE_API_KEY)
        .setSelfSigned(true);

    let database = new sdk.Database(client);

    console.log(process.env.IP_ADDRESS)
    fetch("http://" + process.env.IP_ADDRESS + "/appwrite/event/start")
        .then(url => {

            database.updateDocument(
                process.env.SESSION_COL_ID,
                payload.$id,
                {
                    server_url: url,
                },
                payload.$permissions.read,
                payload.$permissions.write
            )
            .then(() => console.log("Success"))
            .catch((error) => console.log(error))
        }).catch(error => {
            console.log(error)
        })
} else {
    console.log("Non-Session Collection, skipping execution")
}