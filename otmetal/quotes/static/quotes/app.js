const rows = document.querySelector('#product-rows');
const input = document.querySelector('#products-input');
const discount = document.querySelector('[name="discount"]');
const discountType = document.querySelector('[name="discount_type"]');
const money = value => `${Math.round(value).toLocaleString('fr-FR')} FCFA`;
function addRow(product = {}) {
  if (rows.children.length >= 15) return;
  const index = rows.children.length + 1;
  const row = document.createElement('div'); row.className = 'product-row'; row.dataset.index = index;
  row.innerHTML = `<span class="row-number">${index}</span><input class="designation" maxlength="90" placeholder="Désignation" value="${product.designation || ''}"><input class="quantity" type="number" min="0" step="0.01" placeholder="0" value="${product.quantity || ''}"><input class="unit-price" type="number" min="0" step="1" placeholder="0" value="${product.unit_price || ''}"><output class="line-total">—</output>`;
  rows.append(row); row.querySelectorAll('input').forEach(el => el.addEventListener('input', calculate));
}
function calculate() {
  const products = [...rows.children].map(row => ({designation: row.querySelector('.designation').value.trim(), quantity: Number(row.querySelector('.quantity').value || 0), unit_price: Number(row.querySelector('.unit-price').value || 0)}));
  let subtotal = 0; products.forEach((product, i) => { const total = product.quantity * product.unit_price; subtotal += total; rows.children[i].querySelector('.line-total').textContent = total ? money(total) : '—'; });
  const entered = Number(discount.value || 0); const reduction = discountType.value === 'percent' ? subtotal * entered / 100 : entered; const applied = Math.min(reduction, subtotal); const vat = (subtotal - applied) * .1925; input.value = JSON.stringify(products); document.querySelector('#subtotal').textContent = money(subtotal); document.querySelector('#vat').textContent = money(vat); document.querySelector('#total').textContent = money(subtotal - applied + vat);
}
document.querySelector('#add-line')?.addEventListener('click', () => { addRow(); calculate(); });
discount?.addEventListener('input', calculate); discountType?.addEventListener('change', calculate);
for (let i = 0; i < 3; i += 1) addRow(); calculate();
