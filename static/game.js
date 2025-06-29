window.startGame = function(boardData, p1Type, p2Type) {
    const boardDiv = document.getElementById('game-board');
    const statusDiv = document.getElementById('status');
    let board = boardData;
    let gameOver = false;
    let hoverCol = null;
    let hoverPieces = []; // Store references to hover pieces

    function render() {
        // Use a table for perfect alignment and restore column gap
        let table = document.createElement('table');
        table.className = 'c4-table';
        table.style.borderSpacing = '6px'; // restore gap between columns
        table.style.margin = '0 auto';
        // Hover row
        let hoverTr = document.createElement('tr');
        hoverPieces = []; // Reset hover pieces array
        for (let col = 0; col < board.ncol; col++) {
            let hoverTd = document.createElement('td');
            hoverTd.className = 'c4-hover-cell';
            hoverTd.style.padding = '0';
            hoverTd.style.height = '60px'; // Make it easier to click
            hoverTd.style.cursor = 'pointer';
            let hoverPiece = document.createElement('span');
            hoverPiece.className = 'cell hover-cell';
            hoverPiece.style.display = 'block';
            hoverPiece.style.margin = '0 auto';
            hoverPiece.style.background = 'none';
            hoverPiece.style.border = 'none';
            hoverPiece.style.fontSize = '2.5em';
            hoverPiece.style.height = '50px';
            hoverPiece.style.width = '50px';
            hoverPiece.style.lineHeight = '50px';
            hoverPiece.style.textAlign = 'center';
            hoverPieces[col] = hoverPiece; // Store reference
            
            if (isHumanTurn() && board.state[0][col] === 0 && !gameOver) {
                hoverTd.onmouseenter = () => updateHover(col);
                hoverTd.onmouseleave = () => updateHover(null);
                hoverTd.onclick = () => makeMove(col);
            }
            hoverTd.appendChild(hoverPiece);
            hoverTr.appendChild(hoverTd);
        }
        table.appendChild(hoverTr);
        // Board rows
        for (let row = 0; row < board.nrow; row++) {
            let tr = document.createElement('tr');
            for (let col = 0; col < board.ncol; col++) {
                let td = document.createElement('td');
                td.style.padding = '0';
                let val = board.state[row][col];
                let cls = 'cell ' + (val === 1 ? 'p1' : val === 2 ? 'p2' : 'empty');
                let symbol = val === 1 ? '●' : val === 2 ? '○' : '.';
                let cell = document.createElement('span');
                cell.className = cls;
                cell.textContent = symbol;
                cell.dataset.col = col;
                cell.style.display = 'block';
                cell.style.margin = '0 auto';
                td.appendChild(cell);
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }
        boardDiv.innerHTML = '';
        boardDiv.appendChild(table);
        updateHover(hoverCol); // Update hover state after render
    }

    function updateHover(col) {
        hoverCol = col;
        for (let i = 0; i < hoverPieces.length; i++) {
            if (hoverPieces[i]) {
                if (i === col && isHumanTurn() && board.state[0][i] === 0 && !gameOver) {
                    hoverPieces[i].textContent = board.curr_player === 1 ? '●' : '○';
                    hoverPieces[i].style.color = board.curr_player === 1 ? 'red' : 'gold';
                    hoverPieces[i].style.opacity = '1';
                } else {
                    hoverPieces[i].textContent = '';
                    hoverPieces[i].style.opacity = '0.5';
                }
            }
        }
    }

    function isHumanTurn() {
        if (board.curr_player === 1) return p1Type === 'human';
        if (board.curr_player === 2) return p2Type === 'human';
        return false;
    }
    function isAITurn() {
        if (board.curr_player === 1) return p1Type === 'ai' || p1Type === 'random';
        if (board.curr_player === 2) return p2Type === 'ai' || p2Type === 'random';
        return false;
    }

    function makeMove(col) {
        console.log('Making move for column:', col); // Debug log
        fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ col })
        })
        .then(r => r.json())
        .then(data => {
            console.log('Move response:', data); // Debug log
            if (data.error) {
                statusDiv.textContent = data.error;
                return;
            }
            board = data.board;
            hoverCol = null;
            render();
            if (data.winner !== null) {
                gameOver = true;
                if (data.winner === 0) {
                    statusDiv.textContent = "It's a draw!";
                } else {
                    statusDiv.textContent = `Player ${data.winner} wins!`;
                }
            } else {
                statusDiv.textContent = `Player ${board.curr_player}'s turn`;
                if (isAITurn()) maybeAIMove();
            }
        })
        .catch(error => {
            console.error('Error making move:', error);
            statusDiv.textContent = 'Error making move: ' + error.message;
        });
    }

    function maybeAIMove() {
        fetch('/ai_move', { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.board) {
                board = data.board;
                hoverCol = null;
                render();
            }
            if (data.winner !== null) {
                gameOver = true;
                if (data.winner === 0) {
                    statusDiv.textContent = "It's a draw!";
                } else {
                    statusDiv.textContent = `Player ${data.winner} wins!`;
                }
            } else {
                statusDiv.textContent = `Player ${board.curr_player}'s turn`;
                if (isAITurn()) maybeAIMove();
            }
        });
    }

    render();
    statusDiv.textContent = `Player ${board.curr_player}'s turn`;
    if (isAITurn()) maybeAIMove();
};
