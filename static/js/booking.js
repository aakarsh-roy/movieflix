document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('booking-form');
    const seatsInput = document.getElementById('seats');
    const insuranceCheckbox = document.querySelector('input[name="ticket_insurance"]');
    const premiumSeatCheckbox = document.querySelector('input[name="seat_selection"]');
    const totalPriceElement = document.getElementById('total-price');
    
    // Constants for pricing
    const TICKET_PRICE = 200;
    const INSURANCE_PRICE = 20;
    const PREMIUM_SEAT_PRICE = 50;
    
    function calculateTotal() {
        const seats = seatsInput.value.split(',').filter(seat => seat.trim()).length;
        let total = seats * TICKET_PRICE;
        
        if (insuranceCheckbox.checked) {
            total += seats * INSURANCE_PRICE;
        }
        
        if (premiumSeatCheckbox.checked) {
            total += seats * PREMIUM_SEAT_PRICE;
        }
        
        updateSummary(seats, total);
    }
    
    function updateSummary(seatCount, total) {
        const summaryHTML = `
            <div class="mb-4 border-t border-gray-700 pt-4">
                <h3 class="text-lg font-medium mb-3">Booking Summary</h3>
                <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                        <span>Tickets (${seatCount} × ₹${TICKET_PRICE})</span>
                        <span>₹${seatCount * TICKET_PRICE}</span>
                    </div>
                    ${insuranceCheckbox.checked ? `
                        <div class="flex justify-between text-blue-400">
                            <span>Insurance (${seatCount} × ₹${INSURANCE_PRICE})</span>
                            <span>₹${seatCount * INSURANCE_PRICE}</span>
                        </div>
                    ` : ''}
                    ${premiumSeatCheckbox.checked ? `
                        <div class="flex justify-between text-blue-400">
                            <span>Premium Seats (${seatCount} × ₹${PREMIUM_SEAT_PRICE})</span>
                            <span>₹${seatCount * PREMIUM_SEAT_PRICE}</span>
                        </div>
                    ` : ''}
                    <div class="flex justify-between font-bold pt-2 border-t border-gray-700">
                        <span>Total Amount</span>
                        <span>₹${total}</span>
                    </div>
                </div>
            </div>
        `;
        
        totalPriceElement.innerHTML = summaryHTML;
    }
    
    // Event listeners
    seatsInput.addEventListener('input', calculateTotal);
    insuranceCheckbox.addEventListener('change', calculateTotal);
    premiumSeatCheckbox.addEventListener('change', calculateTotal);
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate seats
        const seats = seatsInput.value.split(',').filter(seat => seat.trim());
        if (seats.length === 0) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Selection',
                text: 'Please select at least one seat'
            });
            return;
        }
        
        // Show confirmation
        Swal.fire({
            icon: 'question',
            title: 'Confirm Booking',
            html: `Are you sure you want to book ${seats.length} ticket(s)?`,
            showCancelButton: true,
            confirmButtonText: 'Yes, Book Now',
            cancelButtonText: 'No, Cancel'
        }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
        });
    });
    
    // Initial calculation
    calculateTotal();
});