let options = {};

chrome.storage.sync.get({
    text_trigger_depth: "10",
    text_send_depth: "100",
    recommendation_popup_fade: "10",
    recommendation_service_url: "http://localhost:8080 ",
}, (result) => {
    options = result;
});

console.log("Starting up the extension with options: ", options);

// define a CircularBuffer class that implements push, get and head
class CircularBuffer {
    constructor(size) {
        this.size = size;
        this.buffer = [];
        this.head = 0;
        console.log("Created a CircularBuffer with size: ", size);
    }

    push(element) {
        if (this.buffer.length < this.size) {
            this.buffer.push(element);
        } else {
            this.buffer[this.head] = element;
            this.head = (this.head + 1) % this.size;
        }
    }

    get() {
        return this.buffer;
    }

    head() {
        return this.buffer[this.head];
    }
}


let buffer = new CircularBuffer(options.text_send_depth);

// key event listener, when any space key is pressed, send message to background.js
document.addEventListener('keydown', (event) => {
    buffer.push(event.key);
    if (event.key.match(/\s/)) {
        console.log("buffer: ", buffer.get());
    }
});
