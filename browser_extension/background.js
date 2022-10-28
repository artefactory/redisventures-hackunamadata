class CircularBuffer {
    /*
    * A circular buffer that stores the last N elements.
    * When the buffer is full, the oldest element is overwritten.
    * 
    * methods: push, resize
    */
    constructor(size) {
        this.size = Number((size <= 0 || isNaN(size)) ? 1 : size);
        this.buffer = [];
        this.index = Number(0);
    }

    push(element) {
        if (this.buffer.length < this.size) {
            this.buffer.push(element);
        } else {
            this.buffer[this.index] = element;
        }
        this.index = Number((this.index + 1) % this.size);
        console.log(this.buffer);
    }

    resize(size) {
        // if size <= 0 or is not a number, do nothing
        if (size <= 0 || isNaN(size)) {
            return;
        }
        size = Number(size);
        let right = this.buffer.slice(
            Math.max(this.buffer.length - size + this.index, this.index), this.buffer.length
        )
        let left = this.buffer.slice(
            Math.max(this.index - size, 0), this.index
        )
        this.buffer = right.concat(left);
        this.index = Number(size > this.size ? this.size : 0);
        this.size = size;
    }
}

var buffer = {};

chrome.storage.local.get({
    text_trigger_depth: "10",
    text_send_depth: "100",
    recommendation_popup_fade: "10",
    recommendation_service_url: "http://localhost:8080 ",
}, (result) => {
    buffer = new CircularBuffer(result.text_send_depth);
});


// add runtime message listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("request: ", request);
    if (request.key === undefined)
        return;
    let key = request.key.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    if (key.match(/^[\w\s]$/)) {
        buffer.push(key);
        console.log("buffer: ", buffer.buffer);
    }
});

// add storage change listener to resize buffer
chrome.storage.onChanged.addListener((changes, namespace) => {
    for (key in changes) {
        if (key === "text_send_depth") {
            buffer.resize(changes[key].newValue);
        }
    }
});