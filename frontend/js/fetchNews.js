// js/fetchNews.js

/**
 * Fetch top headlines for a given lat/lon, then render into #sidebar.
 * Expects your backend running at http://localhost:8000/news
 * returning:
 * {
 *   country: "in",
 *   articles: [ { title, url, source }, … ]
 * }
 */
async function fetchNews(lat, lon) {
  const sidebar = document.getElementById('sidebar');

  // 1) Show a loading state immediately
  sidebar.innerHTML = `
    <h2>Coordinates</h2>
    <p>Lat: ${lat.toFixed(2)}°, Lon: ${lon.toFixed(2)}°</p>
    <h2>Country</h2>
    <p>Loading…</p>
    <h2>News</h2>
    <p>Loading…</p>
  `;

  try {
    // 2) Fetch from your backend
    const res  = await fetch(`http://localhost:8000/news?lat=${lat.toFixed(2)}&lon=${lon.toFixed(2)}`);
    const json = await res.json();

    // 3) Extract and normalize the country code
    const countryCode = json.country ? json.country.toUpperCase() : 'Unknown';

    // 4) If no articles, show that
    if (!json.articles || json.articles.length === 0) {
      sidebar.innerHTML = `
        <h2>Coordinates</h2>
        <p>Lat: ${lat.toFixed(2)}°, Lon: ${lon.toFixed(2)}°</p>
        <h2>Country</h2>
        <p>${countryCode}</p>
        <h2>News</h2>
        <p>No articles found for this region.</p>
      `;
      return;
    }

    // 5) Build the final HTML: coords, country, then list of headlines
    let html = `
      <h2>Coordinates</h2>
      <p>Lat: ${lat.toFixed(2)}°, Lon: ${lon.toFixed(2)}°</p>
      <h2>Country</h2>
      <p>${countryCode}</p>
      <h2>Top Headlines</h2>
    `;
    json.articles.forEach(a => {
      html += `
        <div class="article" style="margin-bottom:1em">
          <h3 style="margin:0">
            <a href="${a.url}" target="_blank">${a.title}</a>
          </h3>
          <p style="margin:0;font-size:.9em;color:#555">${a.source}</p>
        </div>
      `;
    });

    // 6) Replace the sidebar with the complete, correct HTML
    sidebar.innerHTML = html;

  } catch (err) {
    console.error(err);
    sidebar.innerHTML = `
      <h2>Coordinates</h2>
      <p>Lat: ${lat.toFixed(2)}°, Lon: ${lon.toFixed(2)}°</p>
      <h2>Country</h2>
      <p>Error</p>
      <h2>News</h2>
      <p style="color:red">Failed to load news.</p>
    `;
  }
}

// expose globally
window.fetchNews = fetchNews;
