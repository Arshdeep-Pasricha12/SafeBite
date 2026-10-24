// SafeBite Popup Controller

document.addEventListener('DOMContentLoaded', async () => {
  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-btn');
  const resultBox = document.getElementById('result-box');
  const resName = document.getElementById('res-name');
  const resAddr = document.getElementById('res-addr');
  const resScore = document.getElementById('res-score');
  const resRating = document.getElementById('res-rating');
  const resStatus = document.getElementById('res-status');
  const resSource = document.getElementById('res-source');
  const resAdvice = document.getElementById('res-advice');
  const resLink = document.getElementById('res-link');
  const apiUrlInput = document.getElementById('api-url');
  const saveSettingsBtn = document.getElementById('save-settings-btn');
  const connStatus = document.getElementById('conn-status');

  // Load configured API URL
  chrome.runtime.sendMessage({ action: 'GET_SETTINGS' }, (res) => {
    if (res && res.apiBase) {
      apiUrlInput.value = res.apiBase;
    }
  });

  // Save Settings
  saveSettingsBtn.addEventListener('click', () => {
    const apiBase = apiUrlInput.value.trim();
    if (!apiBase) return;
    chrome.runtime.sendMessage({ action: 'SET_SETTINGS', apiBase }, () => {
      saveSettingsBtn.textContent = 'Saved!';
      setTimeout(() => { saveSettingsBtn.textContent = 'Save'; }, 1500);
    });
  });

  // Search Action
  async function performSearch(query) {
    if (!query) return;
    searchBtn.textContent = '...';

    chrome.runtime.sendMessage({ action: 'MATCH_RESTAURANT', name: query }, (res) => {
      searchBtn.textContent = 'Search';

      if (!res || !res.matched) {
        resultBox.classList.remove('hidden');
        resName.textContent = `No Match Found for "${query}"`;
        resAddr.textContent = 'Not registered in SafeBite public transparency directory.';
        resScore.textContent = 'N/A';
        resScore.style.color = '#94a3b8';
        resRating.textContent = 'Uninspected';
        resStatus.textContent = 'Pending Verification';
        resSource.textContent = 'Unknown';
        resAdvice.textContent = 'This establishment has no verified on-site inspection data on file. Exercise caution.';
        resLink.style.display = 'none';
        return;
      }

      const rest = res.restaurant;
      const assess = res.assessment;

      resultBox.classList.remove('hidden');
      resName.textContent = rest.name;
      resAddr.textContent = `${rest.address || ''}, ${rest.city || ''}`;
      resScore.textContent = rest.safety_score;

      // Color score
      const score = rest.safety_score;
      resScore.style.color = score >= 90 ? '#10b981' : score >= 75 ? '#3b82f6' : score >= 60 ? '#f59e0b' : '#ef4444';

      resRating.textContent = assess?.grade_label || rest.safety_rating || 'Pass';
      resStatus.textContent = rest.verification_status || (rest.is_synthetic ? 'Synthetic Demo' : 'Verified Official');
      resSource.textContent = rest.source_name || 'Public Registry';
      resAdvice.textContent = assess?.consumer_advice || assess?.summary_explanation || 'Standards verified.';

      if (rest.id) {
        resLink.style.display = 'block';
        resLink.href = `http://localhost:3001/restaurants/${rest.id}`;
      } else {
        resLink.style.display = 'none';
      }
    });
  }

  searchBtn.addEventListener('click', () => performSearch(searchInput.value.trim()));
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') performSearch(searchInput.value.trim());
  });

  // Query active tab to auto-fill if on restaurant page
  if (chrome.tabs && chrome.tabs.query) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0]) {
        const title = tabs[0].title;
        if (title && !title.includes('SafeBite') && !title.includes('Extension')) {
          searchInput.placeholder = `Active page: ${title.slice(0, 20)}...`;
        }
      }
    });
  }
});
