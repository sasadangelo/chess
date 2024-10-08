// Inizializza la scacchiera e il gioco
var board = null;
var game = new Chess();
//var stockfish = STOCKFISH(); // Inizializza il motore Stockfish
var stockfish = new Worker('js/stockfish.min.js');
var engineRunning = false;

var categories = {};
var games = {};

function loadCSV(file, callback) {
    $.ajax({
        url: file,
        dataType: 'text',
    }).done(function(data) {
        var allRows = data.split(/\r?\n|\r/);
        var headers = allRows[0].split(',');
        var result = [];

        for (var i = 1; i < allRows.length; i++) {
            var row = allRows[i].split(',');
            if (row.length === headers.length) {
                var obj = {};
                for (var j = 0; j < headers.length; j++) {
                    obj[headers[j].trim()] = row[j].trim();
                }
                result.push(obj);
            }
        }
        callback(result);
    });
}

// Carica le categorie
loadCSV('data/end_games_categories.csv', function(data) {
    data.forEach(function(category) {
        categories[category.ID] = category.Name;
        $('#categorySelect').append(new Option(category.Name, category.ID));
    });
});

// Carica i giochi
loadCSV('data/end_games.csv', function(data) {
    data.forEach(function(game) {
        if (!games[game.Category_ID]) {
            games[game.Category_ID] = [];
        }
        games[game.Category_ID].push(game);
    });
});

// Aggiorna la lista dei giochi quando viene selezionata una categoria
$('#categorySelect').on('change', function() {
    var categoryId = $(this).val();
    $('#gameSelect').empty().append(new Option("Seleziona un gioco", ""));
    if (games[categoryId]) {
        games[categoryId].forEach(function(game) {
            $('#gameSelect').append(new Option(game.Name, game.ID));
        });
    }
});

// Funzione per aggiornare la scacchiera con una posizione FEN
function updateBoard(fen) {
    game.load(fen); // Carica la posizione FEN nel motore scacchi
    // Aggiorna l'orientamento della scacchiera in base al turno
    var orientation = game.turn() === 'b' ? 'black' : 'white';
    board.orientation(orientation);
    board.position(fen); // Aggiorna la scacchiera visiva
}

console.log(game.turn())
// Configurazione iniziale della scacchiera
var config = {
    draggable: true,
    position: 'start',
    orientation: game.turn() === 'b' ? 'black' : 'white',
    onDrop: function(source, target) {
        var move = game.move({
            from: source,
            to: target,
            promotion: 'q' // sempre promuovi a regina per semplicità
        });

        // Se la mossa è illegale, ritorna il pezzo indietro
        if (move === null) return 'snapback';

        // Se la mossa è valida, fai muovere il computer
        window.setTimeout(makeBestMove, 250);            }
};

board = Chessboard('board', config);

// Funzione per far giocare il computer
function makeBestMove() {
    if (game.game_over()) {
        checkGameOver(); // Check the game state
        return;
    }

    var fen = game.fen();
    stockfish.postMessage('position fen ' + fen);
    stockfish.postMessage('go depth 15'); // Setta la profondità di calcolo di Stockfish

    engineRunning = true;
}

stockfish.onmessage = function(event) {
    var message = event.data; // Accedi al contenuto del messaggio

    if (message.includes('bestmove') && engineRunning) {
        var bestMove = message.split(' ')[1];
        var move = game.move(bestMove, { sloppy: true });
        if (move !== null) {
            board.position(game.fen());

            if (game.game_over()) {
                checkGameOver(); // Check the game state after the engine's move
            }
        }
        engineRunning = false;
    }
};

// Function to check if the game is over and who won
function checkGameOver() {
    if (game.in_checkmate()) {
        if (game.turn() === 'w') {
            alert('Checkmate! Black wins.');
        } else {
            alert('Checkmate! White wins.');
        }
    } else if (game.in_stalemate()) {
        alert('Stalemate! It\'s a draw.');
    } else if (game.in_draw()) {
        alert('Draw!');
    } else if (game.insufficient_material()) {
        alert('Draw due to insufficient material!');
    } else if (game.in_threefold_repetition()) {
        alert('Draw due to threefold repetition!');
    } else {
        alert('Game over.');
    }
}

// Function to start a new game
function startNewGame() {
    var mode = $('input[name="mode"]:checked').val();

    if (mode === 'manual') {
        var gameId = $('#gameSelect').val();
        var categoryId = $('#categorySelect').val();

        if (gameId && categoryId) {
            var selectedGame = games[categoryId].find(game => game.ID === gameId);
            if (selectedGame) {
                updateBoard(selectedGame.FEN);
            }
        } else {
            alert('Please select a category and a game.');
        }
    } else if (mode === 'automatic') {
        var randomCategory = Object.keys(games)[Math.floor(Math.random() * Object.keys(games).length)];
        var randomGame = games[randomCategory][Math.floor(Math.random() * games[randomCategory].length)];
        updateBoard(randomGame.FEN);
        alert('Automatically selected game: ' + randomGame.Name);
    }
}
// Start the game when the button is clicked
$('#startBtn').on('click', startNewGame);

// Toggle manual options based on the selected mode
$('input[name="mode"]').on('change', function() {
    if ($(this).val() === 'manual') {
        $('#manualOptions').show();
    } else {
        $('#manualOptions').hide();
    }
});

// Hide manual options by default when the document is ready
$(document).ready(function() {
    $('#manualOptions').hide(); // Hide manual options by default
});