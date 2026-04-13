const featureNames = [
    "Cross-Encoder (DNN)", "BERT Sim (Cosine)", "BM25 Probabilistic", "Diversity (MMR)",
    "Recency Factor", "Source Trust", "Length Match", "Readability"
];

function setQuery(text) {
    document.getElementById('searchInput').value = text;
    performSearch();
}

function handleKeyPress(e) {
    if (e.key === 'Enter') performSearch();
}

async function performSearch() {
    const query = document.getElementById('searchInput').value;
    if (!query) return;

    document.getElementById('loader').classList.remove('d-none');
    document.getElementById('resultsContainer').classList.add('d-none');

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        renderResults(data);
    } catch (err) {
        alert("Error executing search: " + err);
    } finally {
        document.getElementById('loader').classList.add('d-none');
    }
}

function renderResults(data) {
    document.getElementById('resultsContainer').classList.remove('d-none');

    // Agent status
    document.getElementById('learnedCount').innerText = data.agent_status.queries_learned;
    document.getElementById('learningProgress').style.width = `${Math.min(100, data.agent_status.queries_learned * 10)}%`;

    if (data.agent_status.optimal) {
        const badge = document.getElementById('optimalBadge');
        badge.className = 'badge bg-success text-light px-3 py-2 rounded-pill';
        badge.innerHTML = '<i class="fa-solid fa-check-circle me-1"></i> Optimal Weights Reached';
    }

    const wc = document.getElementById('weightsContainer');
    wc.innerHTML = '';
    data.agent_status.weights.forEach((w, i) => {
        wc.innerHTML += `<span class="badge border border-secondary text-info bg-dark px-3 py-2 weight-badge" title="${featureNames[i]}">${featureNames[i].substring(0, 10)}...: <strong>${w.toFixed(3)}</strong></span>`;
    });

    // Timings
    const t = data.timing;
    document.getElementById('timingMetrics').innerHTML = `
        <i class="fa-solid fa-bolt text-warning me-1"></i> ${t.total_ms}ms 
        <span class="opacity-50 ms-2 fw-normal">(S1: ${t.stage_1_ms}ms | S2: ${t.stage_2_ms}ms | S3: ${t.stage_3_ms}ms)</span>
    `;

    // Results
    const container = document.getElementById('resultsList');
    container.innerHTML = '';

    data.results.forEach((res, rank) => {
        const doc = res.doc;

        let featureRowsTop = '';
        let featureRowsBot = '';

        res.features.forEach((f, i) => {
            const row = `<td><span class="opacity-75">${featureNames[i]}</span></td><td class="text-info font-monospace fw-bold">${parseFloat(f).toFixed(3)}</td>`;
            if (i < 4) featureRowsTop += row;
            else featureRowsBot += row;
        });

        // Calculate Math logic
        let calculationVisual = data.agent_status.weights.map((w, i) => `(<span class="text-info fw-bold">${w.toFixed(3)}</span> <span class="text-secondary fw-bold">×</span> <span class="text-warning fw-bold">${res.features[i].toFixed(3)}</span>)`).join(' <span class="text-light fw-bold">+</span> ');

        let sourceHTML = doc.source.startsWith("http") ? `<a href="${doc.source}" target="_blank" class="text-info text-decoration-none text-truncate d-inline-block border-bottom border-info" style="max-width:200px; vertical-align: bottom;"><i class="fa-solid fa-external-link-alt small me-1"></i>ArXiv File</a>` : `<span class="text-light">${doc.source.toUpperCase()}</span>`;

        const html = `
        <div class="result-card p-4">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h4 class="text-primary mb-2 fw-bold">
                        <span class="badge bg-secondary text-light me-2 align-text-bottom fs-6 rounded-circle">#${rank + 1}</span>
                        ${doc.title}
                    </h4>
                    <div class="small fw-semibold text-muted">
                        <span class="me-3"><i class="fa-regular fa-calendar text-secondary"></i> <span class="text-light">${doc.date}</span></span>
                        <span class="me-3"><i class="fa-solid fa-book-journal-whills text-secondary"></i> ${sourceHTML}</span>
                        <span class="me-3"><i class="fa-solid fa-tag text-secondary"></i> <span class="badge bg-black border border-secondary text-light">${doc.category}</span></span>
                    </div>
                </div>
                <div class="text-end">
                    <div class="text-success fw-black fs-4 mb-1 border border-success bg-success bg-opacity-10 rounded px-3 py-1 shadow-sm">
                        ${res.utility.toFixed(3)} <span class="fs-6 fw-normal text-success opacity-75">Utility</span>
                    </div>
                </div>
            </div>
            
            <p class="mb-2 text-light opacity-75 lh-lg fs-6">${res.snippet || doc.content.substring(0, 350) + "..."}</p>
            <button class="btn btn-sm btn-outline-info mb-4 fw-bold shadow-sm" onclick='openDocumentModal(${JSON.stringify(doc).replace(/'/g, "&#39;")})'>
                <i class="fa-solid fa-book-open me-2"></i>Read Full Abstract
            </button>
            
            <div class="bg-black p-3 rounded-4 border border-secondary mb-4 position-relative shadow-sm glassmorphism">
                <span class="position-absolute top-0 start-0 translate-middle badge rounded-pill bg-primary ms-5 mt-1 border border-primary text-light shadow-sm fs-6 px-3 py-2"><i class="fa-solid fa-calculator me-2"></i> Bayesian Utility Calculation</span>
                
                <div class="alert border border-primary p-3 small font-monospace text-light mt-4 rounded-3 shadow-none lh-lg" style="background-color: rgba(30, 64, 175, 0.2);">
                    <div class="mb-2 text-center fs-6">
                        <strong class="text-white">Utility (U)</strong> = <span class="text-light opacity-75">Σ (Weight<sub>i</sub> × Feature<sub>i</sub>)</span>
                    </div>
                    <div class="text-center" style="word-break: break-all; line-height: 1.8;">
                        = ${calculationVisual}
                    </div>
                    <div class="text-center mt-2 fs-5 mt-3">
                        = <strong class="text-success border-bottom border-success pb-1">${res.utility.toFixed(3)}</strong>
                    </div>
                </div>

                <div class="table-responsive mt-1">
                    <table class="table feature-table table-borderless table-sm mb-0">
                        <tbody>
                            <tr>${featureRowsTop}</tr>
                            <tr>${featureRowsBot}</tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="d-flex justify-content-between align-items-center bg-dark p-3 rounded-3 border border-secondary">
                <span class="text-muted small fw-bold text-uppercase letter-spacing-1"><i class="fa-solid fa-chalkboard-user me-2"></i>Provide AI Feedback:</span>
                <div class="d-flex gap-2">
                    <button class="btn btn-sm btn-outline-success feedback-btn" onclick='sendFeedback("${doc.id}", ${JSON.stringify(res.features)}, true, this)'>
                        <i class="fa-solid fa-thumbs-up me-1"></i> Relevant (+)
                    </button>
                    <button class="btn btn-sm btn-outline-danger feedback-btn" onclick='sendFeedback("${doc.id}", ${JSON.stringify(res.features)}, false, this)'>
                        <i class="fa-solid fa-thumbs-down me-1"></i> Irrelevant (-)
                    </button>
                </div>
            </div>
        </div>
        `;
        container.innerHTML += html;
    });
}

async function sendFeedback(doc_id, features, clicked, btn) {
    const card = btn.closest('.result-card');
    const btns = card.querySelectorAll('.btn');
    const query = document.getElementById('searchInput').value;
    btns.forEach(b => b.disabled = true);

    // Visual feedback
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Learning...';

    try {
        const res = await fetch('/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, doc_id, features, clicked })
        });
        const data = await res.json();

        // Update global agent state locally as visual feedback
        document.getElementById('learnedCount').innerText = data.queries_learned;
        document.getElementById('learningProgress').style.width = `${Math.min(100, data.queries_learned * 10)}%`;

        if (data.optimal) {
            const badge = document.getElementById('optimalBadge');
            badge.className = 'badge bg-success text-light px-3 py-2 rounded-pill';
            badge.innerHTML = '<i class="fa-solid fa-check-circle me-1"></i> Optimal Weights Reached';
        }

        const wc = document.getElementById('weightsContainer');
        wc.innerHTML = '';
        data.new_weights.forEach((w, i) => {
            wc.innerHTML += `<span class="badge border border-success text-success bg-black px-3 py-2 weight-badge updated" title="${featureNames[i]}">${featureNames[i].substring(0, 10)}...: <strong>${w.toFixed(3)}</strong></span>`;
        });

        btn.innerHTML = '<i class="fa-solid fa-check"></i> Recorded';
        btn.classList.replace(clicked ? 'btn-outline-success' : 'btn-outline-danger', clicked ? 'btn-success' : 'btn-danger');

    } catch (err) {
        alert("Error sending feedback");
        btns.forEach(b => b.disabled = false);
        btn.innerHTML = clicked ? '<i class="fa-solid fa-thumbs-up me-1"></i> Relevant (+)' : '<i class="fa-solid fa-thumbs-down me-1"></i> Irrelevant (-)';
    }
}

function openDocumentModal(docInfo) {
    document.getElementById('modalTitle').innerText = docInfo.title;
    document.getElementById('modalDate').innerText = docInfo.date;
    document.getElementById('modalSource').innerText = docInfo.source.toUpperCase();
    document.getElementById('modalCategory').innerText = docInfo.category;
    document.getElementById('modalContent').innerText = docInfo.content;

    const myModal = new bootstrap.Modal(document.getElementById('documentModal'));
    myModal.show();
}
