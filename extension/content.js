// Content script — auto-injected into every page.
// Listens for a message from the popup and replies with the page text.

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getPageText') {
        const text = document.body ? document.body.innerText : '';
        sendResponse({ text: text });
    }
    return true; // keep the message channel open for async response
});
