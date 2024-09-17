
// Get the DOM elements
const boardElement = document.getElementById('board');
const restartButton = document.getElementById('restart');

// Initialize the game board
const initBoard = () => {
    boardElement.innerHTML = '';  // Clear any previous board content
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');  // Add 'cell' class for styling
        cell.setAttribute('data-index', i);  // Store the index as an attribute
        cell.addEventListener('click', handleMove);  // Add click event listener
        boardElement.appendChild(cell);  // Append each cell to the board
    }
};

// Handle player's move
const handleMove = async (e) => {
    const index = e.target.getAttribute('data-index');  // Get clicked cell index
    const response = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index: parseInt(index) })  // Send index to Flask backend
    });
    const result = await response.json();

    if (result.status === 'continue') {
        updateBoard(result.board);  // Update the board if the game continues
    } else if (result.status === 'win') {
        alert(`Player ${result.winner} wins!`);
        updateBoard(result.board);  // Show final state
    } else if (result.status === 'tie') {
        alert('It\'s a tie!');
    } else if (result.status === 'invalid') {
        alert('Invalid move. Try again.');  // Alert if invalid move
    }
};

// Update the board with the new state
const updateBoard = (board) => {
    const cells = document.querySelectorAll('.cell');  // Select all cells
    cells.forEach((cell, index) => {
        cell.textContent = board[index] === '_' ? '' : board[index];  // Display the 'X' or 'O'
    });
};

// Restart the game
restartButton.addEventListener('click', async () => {
    const response = await fetch('/restart', { method: 'POST' });
    const result = await response.json();
    if (result.status === 'reset') {
        initBoard();  // Reinitialize the board on reset
    }
});

// Initialize the board on page load
initBoard();
