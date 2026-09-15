document.addEventListener('DOMContentLoaded', () => {
    // 1. 카테고리 탭 필터링 로직
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const targetCategory = btn.getAttribute('data-filter');

            cards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                if (targetCategory === 'ALL' || cardCategory === targetCategory) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // 2. 챗봇 인터랙션 로직
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');
    const chatLog = document.getElementById('chat-log');
    const toggleBtn = document.getElementById('chat-toggle-btn');
    const chatBody = document.getElementById('chat-body');

    if (toggleBtn && chatBody) {
        toggleBtn.addEventListener('click', () => {
            chatBody.style.display = chatBody.style.display === 'none' ? 'flex' : 'none';
        });
    }

    const sendMessage = async () => {
        if (!chatInput) return;
        const text = chatInput.value.trim();
        if (!text) return;

        const userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.textContent = text;
        chatLog.appendChild(userMsg);
        chatInput.value = '';
        chatLog.scrollTop = chatLog.scrollHeight;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            const botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.innerHTML = `<span class="sender">[AEGIS]</span> ${data.reply}`;
            chatLog.appendChild(botMsg);
            chatLog.scrollTop = chatLog.scrollHeight;
        } catch (e) {
            console.error('Chat API Error:', e);
        }
    };

    if (sendBtn && chatInput) {
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
});