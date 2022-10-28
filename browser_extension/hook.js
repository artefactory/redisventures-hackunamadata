// key event listener, when any space key is pressed, send message to background.js
document.addEventListener('keydown', (event) => {
    chrome.runtime.sendMessage({key: event.key});
});
