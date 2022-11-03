// on message received from background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // if message is from background.js
    if (sender.id !== chrome.runtime.id) {
        return;
    }
    // if message is from background.js and has key property
    if (request.key !== 'textContent') {
        return;
    }
    let text = document.body.textContent.match(/"s" ?: ?"((?!").)*"/);
    text = text !== null ? text[0] : undefined;
    sendResponse({text: text});
});