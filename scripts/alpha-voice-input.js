// Alpha Voice Input — Web Speech API overlay for OpenClaw Control UI
// Paste this into the browser console on the dashboard, or save as a bookmarklet.
// Works in Chrome/Edge (Web Speech API support required).
//
// Usage: Click the 🎤 button (bottom-right), speak, text appears in chat input. Hit Enter to send.

(function () {
  'use strict';

  // Prevent double-init
  if (document.getElementById('alpha-voice-btn')) {
    console.log('[Alpha Voice] Already loaded.');
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('Web Speech API not supported in this browser. Try Chrome or Edge.');
    return;
  }

  // --- Styles ---
  const style = document.createElement('style');
  style.textContent = `
    #alpha-voice-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 99999;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      border: none;
      background: #3b82f6;
      color: white;
      font-size: 24px;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #alpha-voice-btn:hover { background: #2563eb; transform: scale(1.05); }
    #alpha-voice-btn.recording {
      background: #ef4444;
      animation: alpha-pulse 1s infinite;
    }
    @keyframes alpha-pulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
      50% { box-shadow: 0 0 0 12px rgba(239,68,68,0); }
    }
    #alpha-voice-status {
      position: fixed;
      bottom: 88px;
      right: 16px;
      z-index: 99999;
      background: rgba(0,0,0,0.8);
      color: white;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 280px;
      display: none;
      pointer-events: none;
    }
  `;
  document.head.appendChild(style);

  // --- Status indicator ---
  const status = document.createElement('div');
  status.id = 'alpha-voice-status';
  document.body.appendChild(status);

  function showStatus(msg, duration = 3000) {
    status.textContent = msg;
    status.style.display = 'block';
    if (duration > 0) {
      setTimeout(() => { status.style.display = 'none'; }, duration);
    }
  }

  // --- Find chat input (multiple selector strategies) ---
  function findChatInput() {
    // Strategy 1: common textarea/input patterns in Lit/Stencil components
    const selectors = [
      'textarea',
      'input[type="text"]',
      '[contenteditable="true"]',
      '[role="textbox"]',
      'textarea[placeholder]',
      'chat-input textarea',
      'chat-input input',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el) return el;
    }
    // Strategy 2: shadow DOM traversal (Lit components)
    const allElements = document.querySelectorAll('*');
    for (const el of allElements) {
      if (el.shadowRoot) {
        const inner = el.shadowRoot.querySelector('textarea, input[type="text"], [contenteditable="true"]');
        if (inner) return inner;
      }
    }
    return null;
  }

  // --- Recognition setup ---
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  let isRecording = false;

  const btn = document.createElement('button');
  btn.id = 'alpha-voice-btn';
  btn.textContent = '🎤';
  btn.title = 'Alpha Voice Input (click to speak)';
  document.body.appendChild(btn);

  btn.addEventListener('click', () => {
    if (isRecording) {
      recognition.stop();
      return;
    }
    recognition.start();
    isRecording = true;
    btn.classList.add('recording');
    btn.textContent = '⏹';
    showStatus('Listening...', 0);
  });

  recognition.onresult = (event) => {
    let finalTranscript = '';
    let interimTranscript = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript;
      } else {
        interimTranscript += transcript;
      }
    }

    if (interimTranscript) {
      showStatus('🎤 ' + interimTranscript, 0);
    }

    if (finalTranscript) {
      const input = findChatInput();
      if (input) {
        // Set value depending on element type
        if (input.tagName === 'TEXTAREA' || input.tagName === 'INPUT') {
          // Trigger input event for Lit/React reactivity
          const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value'
          )?.set || Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
          )?.set;
          if (nativeInputValueSetter) {
            nativeInputValueSetter.call(input, finalTranscript);
          } else {
            input.value = finalTranscript;
          }
          input.dispatchEvent(new Event('input', { bubbles: true }));
          input.dispatchEvent(new Event('change', { bubbles: true }));
        } else if (input.contentEditable === 'true') {
          input.textContent = finalTranscript;
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        showStatus('✅ Sent: ' + finalTranscript);
        input.focus();
      } else {
        showStatus('⚠️ Chat input not found. Text: ' + finalTranscript, 5000);
        console.log('[Alpha Voice] Could not find chat input. Transcript:', finalTranscript);
      }
    }
  };

  recognition.onend = () => {
    isRecording = false;
    btn.classList.remove('recording');
    btn.textContent = '🎤';
    if (status.textContent.startsWith('Listening')) {
      status.style.display = 'none';
    }
  };

  recognition.onerror = (event) => {
    isRecording = false;
    btn.classList.remove('recording');
    btn.textContent = '🎤';
    if (event.error === 'not-allowed') {
      showStatus('❌ Microphone access denied. Check browser permissions.', 5000);
    } else {
      showStatus('❌ Error: ' + event.error, 5000);
    }
  };

  console.log('[Alpha Voice] Loaded. Click the 🎤 button to speak.');
  showStatus('Alpha Voice loaded — click 🎤 to speak', 4000);
})();
