document.addEventListener('DOMContentLoaded', () => {
    const scanBtn    = document.getElementById('scanBtn');
    const resultCard = document.getElementById('resultCard');
    const resultTitle = document.getElementById('resultTitle');
    const riskScore  = document.getElementById('riskScore');
    const shieldIcon = document.getElementById('shieldIcon');
    const ringFill   = document.getElementById('ringFill');
    const resultHint = document.getElementById('resultHint');
    const btnText    = scanBtn.querySelector('.btn-text');
    const btnLoader  = document.getElementById('btnLoader');

    const API_URL = 'http://127.0.0.1:5001/check';
    const CIRCUMFERENCE = 2 * Math.PI * 52;

    scanBtn.addEventListener('click', () => {
        scanBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
        resultCard.classList.add('hidden');

        // Ask the content script in the active tab for the page text
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (!tabs || !tabs[0]) {
                showError('No active tab found. Open a webpage first.');
                resetBtn();
                return;
            }

            chrome.tabs.sendMessage(tabs[0].id, { action: 'getPageText' }, (response) => {
                if (chrome.runtime.lastError || !response) {
                    showError('Could not read this page. Try reloading the page first, then scan again.');
                    resetBtn();
                    return;
                }

                const pageText = response.text || '';
                if (!pageText.trim()) {
                    showError('No text content found on this page.');
                    resetBtn();
                    return;
                }

                // Send to backend
                fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: pageText }),
                })
                .then((res) => {
                    if (!res.ok) throw new Error('Bad response');
                    return res.json();
                })
                .then((data) => {
                    displayResult(data.result, data.risk_score);
                })
                .catch(() => {
                    showError('Backend server is offline. Start the Flask API first.');
                })
                .finally(() => {
                    resetBtn();
                });
            });
        });
    });

    function displayResult(status, score) {
        resultCard.classList.remove('hidden', 'status-safe', 'status-suspicious', 'status-scam');

        riskScore.textContent = score;
        resultTitle.textContent = status.toUpperCase();

        const icons = {
            'Safe':       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline></svg>',
            'Suspicious': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
            'Scam':       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>'
        };

        const hints = {
            'Safe':       'This page looks legitimate. No scam indicators detected.',
            'Suspicious': 'Some red flags detected. Verify company details before proceeding.',
            'Scam':       'High risk! This page shows strong scam patterns. Do not share personal info.',
        };

        let color = '--safe-color';
        if (status === 'Safe') {
            resultCard.classList.add('status-safe');
            color = '--safe-color';
        } else if (status === 'Suspicious') {
            resultCard.classList.add('status-suspicious');
            color = '--suspicious-color';
        } else {
            resultCard.classList.add('status-scam');
            color = '--scam-color';
        }

        shieldIcon.innerHTML = icons[status] || icons['Scam'];
        resultHint.textContent = hints[status] || '';

        const offset = CIRCUMFERENCE - (score / 100) * CIRCUMFERENCE;
        ringFill.style.stroke = 'var(' + color + ')';
        ringFill.style.strokeDashoffset = offset;
    }

    function showError(message) {
        resultCard.classList.remove('hidden', 'status-safe', 'status-suspicious', 'status-scam');
        resultCard.classList.add('status-scam');
        shieldIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
        resultTitle.textContent = 'ERROR';
        riskScore.textContent = '\u2014';
        resultHint.textContent = message;
        ringFill.style.strokeDashoffset = CIRCUMFERENCE;
    }

    function resetBtn() {
        scanBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});
