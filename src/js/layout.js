export function price_text() {
    const priceElements = document.getElementsByClassName('price-title');
    for (let i = 0; i < priceElements.length; i++) {
        const priceValue = priceElements[i].innerHTML;
        priceElements[i].innerHTML = priceValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
}

$(document).ready(function() {
    price_text();
})