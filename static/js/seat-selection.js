document.addEventListener('DOMContentLoaded', function() {
    const seatMap = document.querySelector('.grid');
    const seatsInput = document.getElementById('seats');
    const selectedSeats = new Set();
    
    
    const bookedSeats = new Set(['A1', 'A2', 'B5', 'C7', 'D4', 'E9']);
    
    
    bookedSeats.forEach(seatId => {
        const seatButton = document.querySelector(`[data-seat="${seatId}"]`);
        if (seatButton) {
            seatButton.classList.remove('bg-gray-700', 'hover:bg-blue-500');
            seatButton.classList.add('bg-red-500', 'cursor-not-allowed');
            seatButton.disabled = true;
        }
    });
    
    
    seatMap.addEventListener('click', function(e) {
        const seatButton = e.target.closest('.seat');
        if (!seatButton || seatButton.disabled) return;
        
        const seatId = seatButton.dataset.seat;
        
        if (selectedSeats.has(seatId)) {
            // Deselect seat
            selectedSeats.delete(seatId);
            seatButton.classList.remove('bg-blue-500');
            seatButton.classList.add('bg-gray-700');
        } else {
            // Select seat
            selectedSeats.add(seatId);
            seatButton.classList.remove('bg-gray-700');
            seatButton.classList.add('bg-blue-500');
        }
        
        
        seatsInput.value = Array.from(selectedSeats).join(',');
        
        
        const event = new Event('change');
        seatsInput.dispatchEvent(event);
    });
    
    // Keyboard navigation
    seatMap.addEventListener('keydown', function(e) {
        const currentSeat = document.activeElement;
        if (!currentSeat.classList.contains('seat')) return;
        
        const currentRow = currentSeat.dataset.seat[0];
        const currentCol = parseInt(currentSeat.dataset.seat.slice(1));
        
        let nextSeat;
        switch(e.key) {
            case 'ArrowUp':
                nextSeat = findSeat(String.fromCharCode(currentRow.charCodeAt(0) - 1), currentCol);
                break;
            case 'ArrowDown':
                nextSeat = findSeat(String.fromCharCode(currentRow.charCodeAt(0) + 1), currentCol);
                break;
            case 'ArrowLeft':
                nextSeat = findSeat(currentRow, currentCol - 1);
                break;
            case 'ArrowRight':
                nextSeat = findSeat(currentRow, currentCol + 1);
                break;
            case ' ':
            case 'Enter':
                e.preventDefault();
                currentSeat.click();
                return;
        }
        
        if (nextSeat) {
            e.preventDefault();
            nextSeat.focus();
        }
    });
    
    function findSeat(row, col) {
        return document.querySelector(`[data-seat="${row}${col}"]`);
    }
    
    // Initialize tooltips for booked seats
    bookedSeats.forEach(seatId => {
        const seatButton = document.querySelector(`[data-seat="${seatId}"]`);
        if (seatButton) {
            seatButton.title = 'Already booked';
        }
    });
});