import '../css/courses.css'

import { price_text } from './layout'

const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');

const durationRange = document.getElementById('durationRange');
const durationValue = document.getElementById('durationValue');

$(document).ready(function() {
    priceValue.textContent = priceRange.value;
    durationValue.textContent = durationRange.value;
    price_text();


    priceRange.addEventListener('input', function () {
        priceValue.textContent = priceRange.value;
        price_text();
    });

    // Function to update the value of the duration slider
    durationRange.addEventListener('input', function () {
        durationValue.textContent = durationRange.value;
    });
});