const statusEl = document.getElementById("status");
const container = document.getElementById("product");
const id = new URLSearchParams(location.search).get("id");

function el(tag, className, text) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (text !== undefined) e.textContent = text;
  return e;
}

async function load() {
  try {
    const res = await fetch("/api/products/" + encodeURIComponent(id));
    const p = await res.json();
    if (!res.ok) throw new Error(p.error || "Request failed");

    document.title = p.name + " - ShopEasy";
    const img = el("img");
    img.src = p.image_url;
    img.alt = p.name;

    const text = el("div", "text");
    text.append(
      el("h1", "", p.name),
      el("span", "tag", p.category),
      el("p", "", p.description),
      el("p", "price", "\u20B9" + Number(p.price).toLocaleString("en-IN", { minimumFractionDigits: 2 })),
      el("p", "", p.stock > 0 ? "In stock: " + p.stock : "Out of stock")
    );
    container.append(img, text);
  } catch (err) {
    statusEl.className = "status error";
    statusEl.textContent = "Could not load product: " + err.message;
  }
}

load();