// js/fetchNews.js

/**
 * Fetch top headlines for a given lat/lon, then render into #sidebar.
 * Expects your backend running at http://localhost:8000/news
 */
async function fetchNews(lat, lon) {
    var sidebar = document.getElementById('sidebar');
    // show coords + loading
    sidebar.innerHTML = ''
      + '<h2>Coordinates</h2>'
      + `<p>Lat: ${lat.toFixed(2)}°, Lon: ${lon.toFixed(2)}°</p>`
      + '<h2>News</h2>'
      + '<p>Loading…</p>';
  
    try {
      var res  = await fetch(`http://localhost:8000/news?lat=${lat.toFixed(2)}&lon=${lon.toFixed(2)}`);
      var json = await res.json();
  
      if (!json.articles || json.articles.length === 0) {
        sidebar.innerHTML += '<p>No articles found for this region.</p>';
        return;
      }
  
      // render list of headlines
      var html = '<h2>Top Headlines</h2>';
      json.articles.forEach(function(a) {
        html += ''
          + '<div class="article" style="margin-bottom:1em">'
          +   `<h3 style="margin:0"><a href="${a.url}" target="_blank">${a.title}</a></h3>`
          +   `<p style="margin:0;font-size:.9em;color:#555">${a.source}</p>`
          + '</div>';
      });
      sidebar.innerHTML = html;
  
    } catch (err) {
      console.error(err);
      sidebar.innerHTML += '<p style="color:red">Failed to load news.</p>';
    }
  }
  
  // expose globally
  window.fetchNews = fetchNews;
  