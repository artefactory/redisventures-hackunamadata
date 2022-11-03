// whenever a value is updated, update chrome.storage.local
var inputs = document.getElementsByTagName("input");

console.log("inputs: ", inputs);

for (var i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("change", function (obj) {
        var key = obj.target.id;
        var value = obj.target.value;
        var obj = {};
        obj[key] = value;
        chrome.storage.local.set(obj);
        console.log("set " + key + " to " + value);
    });
}

// set the value of the input to the value stored in chrome.storage.local or the default value
for (let i = 0; i < inputs.length; i++) {
    let key = inputs[i].id;
    let value = inputs[i].value;
    let lookup = {};
    lookup[key] = value;
    chrome.storage.local.get(lookup, (result) => {
        let value = result[key];
        document.getElementById(key).value = value;
        console.log("set " + key + " to " + value);
    });
}
