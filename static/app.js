document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");
    const taskList = document.getElementById("task-list");
    const reminderList = document.getElementById("reminder-list");
    const goalContainer = document.getElementById("goal-container");
    const micBtn = document.getElementById("mic-btn");
    const speakToggle = document.getElementById("speak-toggle");
    const voiceStatus = document.getElementById("voice-status");
    const transcriptPreview = document.getElementById("transcript-preview");
    const refreshBtn = document.getElementById("refresh-btn");
    const pendingCount = document.getElementById("pending-count");
    const completedCount = document.getElementById("completed-count");
    const reminderCount = document.getElementById("reminder-count");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const canSpeak = "speechSynthesis" in window;
    let recognition = null;
    let isRecording = false;
    let speakReplies = canSpeak;
    let lastSpoken = "";

    init();

    async function init() {
        setupSpeech();
        refreshBtn.addEventListener("click", pollState);

        try {
            const res = await fetch("/api/greet");
            const data = await res.json();
            if (data.greeting) appendMessage("nova-ai", data.greeting, { speak: true });
        } catch (error) {
            appendMessage("nova-ai", "Nova AI is having trouble reaching the local server.");
        }

        pollState();
        setInterval(pollState, 3000);
    }

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage("user", text);
        chatInput.value = "";
        transcriptPreview.hidden = true;

        const typingId = showTyping();

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            removeTyping(typingId);

            if (!res.ok) {
                appendMessage("nova-ai", data.error || "Nova AI could not process that.");
                return;
            }

            (data.responses || []).forEach((msg) => appendMessage("nova-ai", msg, { speak: true }));
            pollState();
        } catch (error) {
            removeTyping(typingId);
            appendMessage("nova-ai", "System error. The local API is offline.");
        }
    });

    speakToggle.addEventListener("click", () => {
        speakReplies = !speakReplies;
        speakToggle.classList.toggle("is-active", speakReplies);
        speakToggle.setAttribute("aria-pressed", String(speakReplies));
        voiceStatus.textContent = speakReplies ? "Voice replies on" : "Voice replies muted";
        if (!speakReplies && canSpeak) window.speechSynthesis.cancel();
    });

    taskList.addEventListener("click", async (event) => {
        const button = event.target.closest("button[data-action]");
        if (!button) return;

        const position = Number(button.dataset.position);
        const action = button.dataset.action;
        const endpoint = action === "complete" ? `/api/tasks/${position}/complete` : `/api/tasks/${position}`;
        const method = action === "complete" ? "POST" : "DELETE";

        try {
            const res = await fetch(endpoint, { method });
            const data = await res.json();
            appendMessage("nova-ai", data.message || "Task updated.", { speak: true });
            pollState();
        } catch (error) {
            appendMessage("nova-ai", "Task action failed. Try typing the command instead.");
        }
    });

    function setupSpeech() {
        if (!canSpeak) {
            speakReplies = false;
            speakToggle.disabled = true;
            speakToggle.classList.remove("is-active");
        }

        micBtn.addEventListener("click", async () => {
            if (isRecording) return; // Wait for current listening to finish

            isRecording = true;
            micBtn.classList.add("recording");
            micBtn.title = "Listening via backend...";
            voiceStatus.textContent = "Listening...";
            chatInput.placeholder = "Listening to your microphone...";
            transcriptPreview.hidden = false;
            transcriptPreview.textContent = "Speak now... (Backend STT)";

            try {
                const res = await fetch("/api/listen", { method: "POST" });
                const data = await res.json();

                if (res.ok && data.text) {
                    chatInput.value = data.text;
                    transcriptPreview.hidden = true;
                    chatForm.requestSubmit();
                } else {
                    throw new Error(data.error || "Could not recognize speech.");
                }
            } catch (error) {
                voiceStatus.textContent = "Voice input error";
                transcriptPreview.textContent = error.message;
                setTimeout(() => { transcriptPreview.hidden = true; }, 3000);
            } finally {
                isRecording = false;
                micBtn.classList.remove("recording");
                micBtn.title = "Start voice input";
                chatInput.placeholder = "Ask Nova AI anything or type a command...";
                if (voiceStatus.textContent === "Voice input error") {
                    setTimeout(() => {
                        voiceStatus.textContent = speakReplies ? "Voice replies on" : "Voice ready";
                    }, 3000);
                } else {
                    voiceStatus.textContent = speakReplies ? "Voice replies on" : "Voice ready";
                }
            }
        });

        voiceStatus.textContent = speakReplies ? "Voice replies on" : "Voice ready";
    }

    async function pollState() {
        try {
            const res = await fetch("/api/state");
            const data = await res.json();

            renderGoal(data.goal, data.memory);
            renderTasks(data.tasks || []);
            renderReminders(data.reminders || []);
            renderStats(data.stats || {});

            (data.messages || []).forEach((msg) => appendMessage("nova-ai", msg, { speak: true }));
        } catch (error) {
            console.error("Failed to poll state", error);
        }
    }

    function renderStats(stats) {
        pendingCount.textContent = stats.pending ?? 0;
        completedCount.textContent = stats.completed ?? 0;
        reminderCount.textContent = stats.reminders ?? 0;
    }

    function renderGoal(goal, memory = {}) {
        const fallbackGoal = Array.isArray(memory.goals) && memory.goals.length ? memory.goals[0] : "";
        const value = goal || fallbackGoal;
        goalContainer.innerHTML = value
            ? `<p>${escapeHTML(value)}</p>`
            : `<p class="empty-text">No goal defined.</p>`;
    }

    function renderTasks(tasks) {
        taskList.innerHTML = "";
        if (!tasks.length) {
            taskList.innerHTML = `<li class="empty-text">No pending tasks.</li>`;
            return;
        }

        tasks.forEach((task, index) => {
            const position = index + 1;
            const item = document.createElement("li");
            item.className = "task-item";
            item.innerHTML = `
                <div>
                    <span class="task-number">${position}</span>
                    <p>${escapeHTML(task.name)}</p>
                </div>
                <div class="task-actions">
                    <button type="button" class="icon-button mini" data-action="complete" data-position="${position}" title="Mark complete" aria-label="Mark task ${position} complete">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m20 6-11 11-5-5"/></svg>
                    </button>
                    <button type="button" class="icon-button mini danger" data-action="delete" data-position="${position}" title="Delete task" aria-label="Delete task ${position}">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/></svg>
                    </button>
                </div>
            `;
            taskList.appendChild(item);
        });
    }

    function renderReminders(reminders) {
        reminderList.innerHTML = "";
        const active = reminders.filter((reminder) => !reminder.fired);
        if (!active.length) {
            reminderList.innerHTML = `<li class="empty-text">No active reminders.</li>`;
            return;
        }

        active.slice(0, 4).forEach((reminder) => {
            const item = document.createElement("li");
            item.className = "reminder-item";
            item.innerHTML = `
                <span>${escapeHTML(reminder.time)}</span>
                <p>${escapeHTML(reminder.label)}</p>
            `;
            reminderList.appendChild(item);
        });
    }

    function appendMessage(sender, text, options = {}) {
        const div = document.createElement("article");
        div.className = `message ${sender}`;
        
        let contentHTML = escapeHTML(text);
        if (sender === "nova-ai" && typeof marked !== "undefined") {
            contentHTML = marked.parse(text);
        }
        
        div.innerHTML = `
            <span class="sender">${sender === "nova-ai" ? "Nova AI" : "You"}</span>
            <div class="content">${contentHTML}</div>
        `;
        chatMessages.appendChild(div);
        scrollToBottom();

        if (sender === "nova-ai" && options.speak) speak(text);
    }

    function speak(text) {
        if (!speakReplies || !canSpeak || !text || text === lastSpoken) return;
        lastSpoken = text;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        
        const voices = window.speechSynthesis.getVoices();
        const femaleVoice = voices.find(v => 
            v.name.includes("Zira") || 
            v.name.includes("Female") || 
            v.name.includes("Samantha")
        );
        if (femaleVoice) {
            utterance.voice = femaleVoice;
        }

        utterance.rate = 0.96;
        utterance.pitch = 1.1;
        utterance.volume = 0.9;
        window.speechSynthesis.speak(utterance);
    }

    function showTyping() {
        const id = `typing-${Date.now()}`;
        const div = document.createElement("div");
        div.id = id;
        div.className = "typing-indicator";
        div.innerHTML = `<span></span><span></span><span></span>`;
        chatMessages.appendChild(div);
        scrollToBottom();
        return id;
    }

    function removeTyping(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHTML(str) {
        return String(str).replace(/[&<>'"]/g, (tag) => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "'": "&#39;",
            '"': "&quot;"
        }[tag] || tag));
    }
});
