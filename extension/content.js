// SafeBite Content Script
(function() {
  let injected = false;
  let currentRestaurantName = '';

  function extractRestaurantName() {
    // 1. Check for Companion Demo or generic restaurant title
    const h1 = document.querySelector('h1');
    if (h1 && h1.innerText.trim()) {
      return h1.innerText.trim();
    }

    // 2. Check Swiggy selectors
    const swiggyTitle = document.querySelector('h1[title], [data-testid="restaurant-name"]');
    if (swiggyTitle && swiggyTitle.innerText.trim()) {
      return swiggyTitle.innerText.trim();
    }

    // 3. Check Zomato selectors
    const zomatoTitle = document.querySelector('h1.sc-7kepeu-0, h1');
    if (zomatoTitle && zomatoTitle.innerText.trim()) {
      return zomatoTitle.innerText.trim();
    }

    return null;
  }

  function initSafeBiteOverlay() {
    const name = extractRestaurantName();
    if (!name || name === currentRestaurantName) return;
    currentRestaurantName = name;

    // Send query to background service worker
    chrome.runtime.sendMessage(
      { action: 'MATCH_RESTAURANT', name: name },
      (response) => {
        if (!response || !response.matched) {
          removeExistingBadge();
          return;
        }
        renderSafeBiteBadge(response);
      }
    );
  }

  function removeExistingBadge() {
    const existing = document.getElementById('safebite-extension-root');
    if (existing) existing.remove();
  }

  function renderSafeBiteBadge(matchData) {
    removeExistingBadge();

    const restaurant = matchData.restaurant;
    const assessment = matchData.assessment;
    const score = restaurant?.safety_score || 90;
    const isVerified = !restaurant?.is_synthetic;
    const gradeLabel = assessment?.grade_label || restaurant?.safety_rating || 'Pass';

    // Color logic
    let scoreColor = '#10b981'; // green
    if (score < 60) scoreColor = '#ef4444'; // red
    else if (score < 75) scoreColor = '#f59e0b'; // amber
    else if (score < 90) scoreColor = '#3b82f6'; // blue

    const container = document.createElement('div');
    container.id = 'safebite-extension-root';
    container.innerHTML = `
      <div id="safebite-pill" title="Click to view SafeBite Safety Audit">
        <div class="safebite-pill-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </div>
        <div class="safebite-pill-content">
          <span class="safebite-pill-label">SafeBite</span>
          <span class="safebite-pill-score" style="color: ${scoreColor}">${score}/100</span>
          <span class="safebite-pill-tag">${isVerified ? 'VERIFIED' : 'DEMO'}</span>
        </div>
      </div>

      <div id="safebite-modal" class="safebite-hidden">
        <div class="safebite-modal-header">
          <div class="safebite-modal-title-row">
            <div class="safebite-modal-logo">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <span>SafeBite Audit Intelligence</span>
            </div>
            <button id="safebite-modal-close">✕</button>
          </div>
          <h3 class="safebite-restaurant-name">${restaurant.name}</h3>
          <p class="safebite-restaurant-addr">${restaurant.address || ''}, ${restaurant.city || ''}</p>
        </div>

        <div class="safebite-modal-body">
          <div class="safebite-score-box">
            <div>
              <div class="safebite-score-num" style="color: ${scoreColor}">${score}</div>
              <div class="safebite-score-sub">Safety Score / 100</div>
            </div>
            <div class="safebite-badge-col">
              <span class="safebite-grade-pill">${gradeLabel}</span>
              <span class="safebite-prov-pill ${isVerified ? 'verified' : 'demo'}">
                ${isVerified ? 'Official Health Authority' : 'Benchmark Simulation'}
              </span>
            </div>
          </div>

          ${assessment?.summary_explanation ? `
            <div class="safebite-explanation">
              <strong>Audit Assessment:</strong> ${assessment.summary_explanation}
            </div>
          ` : ''}

          ${assessment?.consumer_advice ? `
            <div class="safebite-advice">
              <strong>Consumer Advice:</strong> ${assessment.consumer_advice}
            </div>
          ` : ''}

          ${assessment?.positive_factors?.length ? `
            <div class="safebite-factors-section">
              <div class="safebite-factors-title">Verified Compliance Strengths:</div>
              <ul>
                ${assessment.positive_factors.map(f => `<li>✓ ${f}</li>`).join('')}
              </ul>
            </div>
          ` : ''}

          <div class="safebite-provenance-footer">
            <div><strong>Source:</strong> ${restaurant.source_name || 'Public Registry'}</div>
            <div><strong>Status:</strong> ${restaurant.verification_status || 'Verified'} | License #${restaurant.license_number || 'N/A'}</div>
          </div>

          ${restaurant.id ? `
            <a href="http://localhost:3001/restaurants/${restaurant.id}" target="_blank" class="safebite-view-btn">
              Open Full Transparency Report →
            </a>
          ` : ''}
        </div>
      </div>
    `;

    document.body.appendChild(container);

    // Event listeners
    const pill = container.querySelector('#safebite-pill');
    const modal = container.querySelector('#safebite-modal');
    const closeBtn = container.querySelector('#safebite-modal-close');

    pill.addEventListener('click', () => {
      modal.classList.toggle('safebite-hidden');
    });

    closeBtn.addEventListener('click', () => {
      modal.classList.add('safebite-hidden');
    });
  }

  // Periodic observer to catch single-page navigation in SPAs
  setInterval(initSafeBiteOverlay, 2000);
  initSafeBiteOverlay();
})();
