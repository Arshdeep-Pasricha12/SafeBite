# SafeBite — Chrome Browser Extension (Manifest V3)

**Version:** 1.0.0  
**Manifest Version:** 3 (Google Chrome Compliant)  
**Location:** `extension/`  

---

## 1. Overview

The SafeBite Chrome Extension projects food-safety intelligence directly into online food-ordering experiences. When a user browses restaurant menus on supported platforms or the SafeBite Companion Ordering Demo (`http://127.0.0.1:5173/demo/order`), the extension:
1. Detects the restaurant name from the page DOM.
2. Queries the SafeBite matching API (`GET /api/restaurants/match`).
3. Injects a non-intrusive floating SafeBite Safety Pill displaying the verified rating and grade.
4. Opens an interactive modal when clicked, displaying the complete inspection breakdown and provenance evidence.

---

## 2. Manifest V3 File Architecture

```
extension/
├── manifest.json       # Manifest V3 configuration & permission declarations
├── background.js       # Ephemeral service worker handling network queries & caching
├── content.js          # Injected DOM scraper, pill injector, and modal manager
├── content.css         # Isolated CSS styles for injected elements
├── popup.html          # Toolbar popup UI for manual restaurant search
├── popup.css           # Styling for toolbar popup
├── popup.js            # Client logic for manual toolbar searches
└── icons/              # Extension icons (16x16, 48x48, 128x128 PNG)
```

---

## 3. Core Component Workflows

### 3.1 Service Worker (`background.js`)
- Runs as an event-driven background service worker in accordance with Manifest V3 standards (no persistent background page).
- Listens for message events from `content.js` and `popup.js`.
- Queries the backend endpoint:
  ```
  GET http://127.0.0.1:8000/api/restaurants/match?name=<encoded_name>&city=<encoded_city>
  ```
- Caches match responses in local storage to prevent duplicate queries on DOM changes.
- Provides fallback mock assessment data if the backend is temporarily offline.

### 3.2 Content Script (`content.js` & `content.css`)
- Automatically matches supported food delivery domains and local demo pages (`*://127.0.0.1/*`, `*://localhost/*`).
- Extracts restaurant headings using prioritized selector strategies:
  - `[data-safebite-restaurant]`
  - `h1.restaurant-name`, `h1.store-name`, `h1`
  - Meta tags and document title fallback.
- Injects a styled badge element (`#safebite-floating-pill`) into the host page DOM.
- When clicked, creates `#safebite-modal-overlay` showing score, grade badge, positive compliance factors, critical deductions, and official government audit source links.

### 3.3 Toolbar Popup (`popup.html` & `popup.js`)
- Allows users to type any restaurant name manually from their browser toolbar.
- Renders safety status, grade label, and verification shield without opening full browser tabs.

---

## 4. How to Load and Test in Google Chrome

### Step 1: Open Chrome Extensions
1. Launch Google Chrome.
2. Navigate to `chrome://extensions/` in the URL bar.
3. Toggle on the **Developer mode** switch in the top-right corner.

### Step 2: Load Unpacked Extension
1. Click the **Load unpacked** button in the top-left toolbar.
2. Browse to this repository and select the `extension/` folder.
3. Verify that **SafeBite — Food Safety Transparency** appears in your installed extensions list with Manifest V3 badges.

### Step 3: Test on Companion Ordering Platform
1. Ensure the SafeBite backend is running on `http://127.0.0.1:8000`.
2. Ensure the SafeBite frontend is running on `http://127.0.0.1:5173`.
3. Open `http://127.0.0.1:5173/demo/order` in Chrome.
4. Observe the floating **SafeBite Score Pill** automatically injected in the top right of the food menu.
5. Click the pill to expand the SafeBite Safety Audit modal directly on the page!
