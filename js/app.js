// Archetype data for different cities
const archetypeData = {
    student: {
        inflation: '4.8%',
        label: 'Annual inflation for grad student basket',
        items: [
            { name: 'TJ RAMEN CHICKEN 6PK', price: '3.49', sku: '12345', qty: '1', change: '+0.30' },
            { name: 'FROZEN PAD THAI', price: '4.99', sku: '23456', qty: '1', change: '+0.50' },
            { name: 'CHARLES SHAW RED WINE', price: '3.99', sku: '34567', qty: '1', change: '+1.00' },
            { name: 'PB FILLED PRETZELS', price: '2.99', sku: '45678', qty: '1', change: '+0.20' },
            { name: 'MARGHERITA PIZZA FRZ', price: '3.99', sku: '56789', qty: '1', change: '+0.40' }
        ],
        subtotal: '19.45',
        tax: '1.56',
        total: '21.01',
        change: '+2.96 (16.4%)'
    },
    teacher: {
        inflation: '3.2%',
        label: 'Annual inflation for teacher basket',
        items: [
            { name: 'BREAKFAST BARS 6CT', price: '4.49', sku: '67890', qty: '1', change: '+0.20' },
            { name: 'POWER GREENS SALAD KIT', price: '3.99', sku: '78901', qty: '1', change: '+0.30' },
            { name: 'COLD BREW COFFEE 32OZ', price: '7.99', sku: '89012', qty: '1', change: '+0.50' },
            { name: 'GREEK YOGURT 4PK', price: '4.99', sku: '90123', qty: '1', change: '+0.25' },
            { name: 'TRAIL MIX CRANBRRY', price: '5.99', sku: '01234', qty: '1', change: '+0.15' }
        ],
        subtotal: '27.45',
        tax: '2.20',
        total: '29.65',
        change: '+1.40 (4.9%)'
    },
    family: {
        inflation: '5.1%',
        label: 'Annual inflation for family basket',
        items: [
            { name: 'GOLDFISH CRACKERS', price: '2.99', sku: '11111', qty: '2', change: '+0.40' },
            { name: 'ORGANIC MILK 1/2GAL', price: '4.99', sku: '22222', qty: '1', change: '+0.60' },
            { name: 'CHICKEN NUGGETS FRZ', price: '6.99', sku: '33333', qty: '1', change: '+0.70' },
            { name: 'MANDARIN ORANGES', price: '3.49', sku: '44444', qty: '1', change: '+0.30' },
            { name: 'MAC & CHEESE 6PK', price: '4.99', sku: '55555', qty: '1', change: '+0.50' },
            { name: 'SOURDOUGH BREAD', price: '2.99', sku: '66666', qty: '1', change: '+0.35' }
        ],
        subtotal: '29.43',
        tax: '2.35',
        total: '31.78',
        change: '+3.85 (13.8%)'
    },
    fed: {
        inflation: '2.8%',
        label: 'Federal Reserve regional basket',
        items: [
            { name: 'ORGANIC EVERYTHING', price: '8.99', sku: '77777', qty: '1', change: '+0.20' },
            { name: 'ARTISANAL CHEESE', price: '12.99', sku: '88888', qty: '1', change: '+0.40' },
            { name: 'PREMIUM PINOT NOIR', price: '19.99', sku: '99999', qty: '1', change: '+0.50' },
            { name: 'QUINOA SALAD KIT', price: '6.99', sku: '10101', qty: '1', change: '+0.30' },
            { name: 'FAIR TRADE COFFEE', price: '11.99', sku: '20202', qty: '1', change: '+0.25' }
        ],
        subtotal: '60.95',
        tax: '4.88',
        total: '65.83',
        change: '+1.65 (2.6%)'
    },
    cpi: {
        inflation: '3.4%',
        label: 'TJ\'s basket vs. Federal CPI',
        items: [
            { name: 'FOOD BASKET STANDARD', price: '45.99', sku: '30303', qty: '1', change: '+1.50' },
            { name: 'BEVERAGES ASSORTED', price: '12.99', sku: '40404', qty: '1', change: '+0.45' },
            { name: 'HOUSEHOLD ITEMS', price: '18.99', sku: '50505', qty: '1', change: '+0.60' },
            { name: 'PERSONAL CARE', price: '8.99', sku: '60606', qty: '1', change: '+0.25' }
        ],
        subtotal: '86.96',
        tax: '6.96',
        total: '93.92',
        change: '+2.80 (3.1%)'
    }
};

// Navigation functions
function goToMap() {
    window.location.href = 'map.html';
}

function goToDashboard(cityName) {
    window.location.href = `dashboard.html?city=${encodeURIComponent(cityName)}`;
}

function goBack() {
    window.location.href = 'map.html';
}

// Utility functions
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function selectCity(cityName) {
    goToDashboard(cityName);
}

function updateArchetypesForCity(city) {
    const archetypes = document.querySelectorAll('.archetype-card');
    if (archetypes.length < 2) return;
    
    const studentCard = archetypes[0];
    const teacherCard = archetypes[1];
    
    if (city === 'Chicago') {
        studentCard.querySelector('h4').textContent = 'UChicago Grad Student';
        teacherCard.querySelector('h4').textContent = 'CPS Teacher';
    } else if (city === 'New York') {
        studentCard.querySelector('h4').textContent = 'NYU Grad Student';
        teacherCard.querySelector('h4').textContent = 'NYC DOE Teacher';
    } else if (city === 'Los Angeles') {
        studentCard.querySelector('h4').textContent = 'UCLA Grad Student';
        teacherCard.querySelector('h4').textContent = 'LAUSD Teacher';
    } else {
        studentCard.querySelector('h4').textContent = 'UT Grad Student';
        teacherCard.querySelector('h4').textContent = 'Austin ISD Teacher';
    }
}

function selectArchetype(card, type) {
    // Remove previous selection
    document.querySelectorAll('.archetype-card').forEach(c => c.classList.remove('selected'));
    
    // Select current card
    card.classList.add('selected');
    
    // Update results
    const data = archetypeData[type];
    const inflationRate = document.getElementById('inflationRate');
    const inflationLabel = document.getElementById('inflationLabel');
    
    if (inflationRate && inflationLabel) {
        inflationRate.textContent = data.inflation;
        inflationLabel.textContent = data.label;
    }
    
    // Show and populate receipt
    const receipt = document.getElementById('basketReceipt');
    if (receipt) {
        receipt.style.display = 'block';
        
        const now = new Date();
        const receiptDate = now.toLocaleDateString() + ' ' + now.toLocaleTimeString();
        const transactionId = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
        const cityName = getQueryParam('city') || 'Austin';
        
        const itemsHtml = data.items.map((item, index) => 
            `<div class="receipt-item">
                <div class="receipt-item-name">${item.name}</div>
                <div class="receipt-item-details">
                    <span>${item.sku} QTY ${item.qty}</span>
                    <span>${item.price}</span>
                </div>
            </div>`
        ).join('');
        
        receipt.innerHTML = `
            <div class="receipt-header">
                <strong>TRADER JOE'S</strong><br>
                Thank you for shopping with us!
            </div>
            
            <div class="receipt-store-info">
                Store #123 - ${cityName}<br>
                ${receiptDate}<br>
                Trans# ${transactionId} | Cashier: ALEX
            </div>
            
            ${itemsHtml}
            
            <div class="receipt-separator"></div>
            
            <div class="receipt-subtotal">
                <span>SUBTOTAL:</span>
                <span>${data.subtotal}</span>
            </div>
            
            <div class="receipt-tax">
                <span>TAX:</span>
                <span>${data.tax}</span>
            </div>
            
            <div class="receipt-total">
                <div class="receipt-total-line">
                    <span>TOTAL:</span>
                    <span>${data.total}</span>
                </div>
                <div class="receipt-total-line">
                    <span>CREDIT CARD:</span>
                    <span>${data.total}</span>
                </div>
            </div>
            
            <div class="receipt-change">
                <div class="receipt-total-line">
                    <span>YoY INFLATION:</span>
                    <span>${data.change}</span>
                </div>
            </div>
            
            <div class="receipt-footer">
                Visit us at traderjoes.com<br>
                Follow @TraderJoesList<br><br>
                INFLATION TRACKER<br>
                Data as of ${now.toLocaleDateString()}
            </div>
        `;
    }
}

function customBasket() {
    alert('Custom basket builder coming soon! This would allow you to create your own personalized inflation basket.');
}
