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
    board.position(fen); // Aggiorna la scacchiera visiva
}

// Configurazione iniziale della scacchiera
var config = {
    draggable: true,
    position: 'start',
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
        alert('Game over');
        return;
    }

    var fen = game.fen();
    stockfish.postMessage('position fen ' + fen);
    stockfish.postMessage('go depth 15'); // Setta la profondità di calcolo di Stockfish

    engineRunning = true;
}

stockfish.onmessage = function(event) {
    var message = event.data; // Accedi al contenuto del messaggio
    console.log(message)
    console.log(message.includes('bestmove'))
    console.log(engineRunning)


    if (message.includes('bestmove') && engineRunning) {
        var bestMove = message.split(' ')[1];
        console.log(bestMove)
        console.log(game.move(bestMove, { sloppy: true }));
        board.position(game.fen());
        engineRunning = false;
    }
};

// Aggiungi evento al pulsante per caricare la FEN del gioco selezionato
$('#startBtn').on('click', function() {
    var gameId = $('#gameSelect').val();
    var categoryId = $('#categorySelect').val();

    if (gameId && categoryId) {
        var selectedGame = games[categoryId].find(game => game.ID === gameId);
        if (selectedGame) {
            updateBoard(selectedGame.FEN);
        }
    } else {
        alert('Seleziona una categoria e un gioco.');
    }
});