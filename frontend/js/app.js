const grid = document.getElementById("product-grid");
const statusEl = document.getElementById("status");
const searchEl = document.getElementById("search");
const categoryEl = document.getElementById("category");

function formatPrice(p) {
  return "\u20B9" + Number(p).toLocaleString("en-IN", { minimumFractionDigits: 2 });
}

function makeCard(p) {
  const a = document.createElement("a");
  a.className = "card";
  a.href = "/product.html?id=" + p.id;

  const img = document.createElement("img");
  img.src = p.image_url;
  img.alt = p.name;

  const info = document.createElement("div");
  info.className = "info";
  const h3 = document.createElement("h3");
  h3.textContent = p.name;
  const desc = document.createElement("p");
  desc.textContent = p.description;
  const price = document.createElement("span");
  price.className = "price";
  price.textContent = formatPrice(p.price);

  info.append(h3, desc, price);
  a.append(img, info);
  return a;
}

async function loadProducts() {
  const params = new URLSearchParams();
  if (searchEl.value.trim()) params.set("search", searchEl.value.trim());
  if (categoryEl.value) params.set("category", categoryEl.value);

  statusEl.className = "status";
  statusEl.textContent = "Loading...";
  grid.replaceChildren();
  try {
    const res = await fetch("/api/products?" + params);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Request failed");
    statusEl.textContent = data.length ? data.length + " product(s) found" : "No products found.";
    data.forEach(p => grid.appendChild(makeCard(p)));
  } catch (err) {
    statusEl.className = "status error";
    statusEl.textContent = "Could not load products: " + err.message;
  }
}

async function loadCategories() {
  try {
    const res = await fetch("/api/categories");
    const cats = await res.json();
    cats.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name;
      categoryEl.appendChild(opt);
    });
  } catch (_) { /* filter simply stays on "All categories" */ }
}

document.getElementById("filter-form").addEventListener("submit", e => { e.preventDefault(); loadProducts(); });
document.getElementById("reset").addEventListener("click", () => {
  searchEl.value = ""; categoryEl.value = ""; loadProducts();
});

loadCategories();
loadProducts();