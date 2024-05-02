//  Script.js 
console.log('sliderjs')
document.addEventListener("DOMContentLoaded", () => {
    const minInput = document.querySelector(".min-input");
    const maxInput = document.querySelector(".max-input");
    const minRange = document.querySelector(".min-range");
    const maxRange = document.querySelector(".max-range");
    const rangeSlider = document.querySelector(".price-slider");

    const priceGap = 10;
    const maxPriceLimit = 5000;
    const minPriceLimit = 0;

    function updateRangeStyle() {
        const percentMin = (minRange.value / maxRange.max) * 100;
        const percentMax = 100 - (maxRange.value / maxRange.max) * 100;
        rangeSlider.style.left = `${percentMin}%`;
        rangeSlider.style.right = `${percentMax}%`;
    }

    function setRangeInputs(minVal, maxVal) {
        minRange.value = minVal;
        maxRange.value = maxVal;
        minInput.value = minVal;
        maxInput.value = maxVal;
        updateRangeStyle();
    }

    [minInput, maxInput].forEach(input => {
        input.addEventListener("input", () => {
            let minVal = parseInt(minInput.value) || minPriceLimit;
            let maxVal = parseInt(maxInput.value) || maxPriceLimit;

            if (minVal < minPriceLimit) {
                minVal = minPriceLimit;
                minInput.value = minVal;
            }

            if (maxVal > maxPriceLimit) {
                maxVal = maxPriceLimit;
                maxInput.value = maxVal;
            }

            if (minVal > maxVal - priceGap) {
                minVal = maxVal - priceGap;
                minInput.value = minVal;
            }

            if (maxVal < minVal + priceGap) {
                maxVal = minVal + priceGap;
                maxInput.value = maxVal;
            }

            setRangeInputs(minVal, maxVal);
        });
    });

    [minRange, maxRange].forEach(range => {
        range.addEventListener("input", () => {
            let minVal = parseInt(minRange.value);
            let maxVal = parseInt(maxRange.value);

            if (maxVal - minVal < priceGap) {
                if (range === minRange && minVal > minPriceLimit) {
                    minVal = maxVal - priceGap;
                } else if (range === maxRange && maxVal < maxPriceLimit) {
                    maxVal = minVal + priceGap;
                }
            }

            setRangeInputs(minVal, maxVal);
        });
    });
});
