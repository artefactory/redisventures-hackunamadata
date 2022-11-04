// whenever a value is updated, update chrome.storage.local
var options = Array.from(document.getElementsByTagName("input")).concat(Array.from(document.getElementsByTagName("select")));


for (var i = 0; i < options.length; i++) {
    options[i].addEventListener("change", function (obj) {
        var key = obj.target.id;
        var value = obj.target.value;
        var obj = {};
        obj[key] = value;
        chrome.storage.local.set(obj);
        console.log("set " + key + " to " + value);
    });
}

// set the value of the input to the value stored in chrome.storage.local or the default value
for (let i = 0; i < options.length; i++) {
    let key = options[i].id;
    let value = options[i].value;
    let lookup = {};
    lookup[key] = value;
    chrome.storage.local.get(lookup, (result) => {
        let value = result[key];
        document.getElementById(key).value = value;
        console.log("set " + key + " to " + value);
    });
}
