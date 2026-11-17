"use strict";
const input = document.querySelector("#research-search");
const results = document.querySelector("#search-results");
let index;
input.addEventListener("input", async () => {
  const query = input.value.trim().toLowerCase();
  results.replaceChildren();
  if (query.length < 2) return;
  try {
    if (!index) {
      const response = await fetch("search-index.json");
      if (!response.ok) throw new Error("Search unavailable");
      index = await response.json();
    }
    if (input.value.trim().toLowerCase() !== query) return;
    const matches = index.filter(item => item.title.toLowerCase().includes(query)).slice(0, 8);
    if (!matches.length) results.textContent = "No matching sections. Try the page navigation.";
    for (const item of matches) {
      const link = document.createElement("a");
      link.href = item.url;
      link.textContent = item.title;
      results.append(link);
    }
  } catch {
    results.textContent = "Search is unavailable. Use the page navigation.";
  }
});
