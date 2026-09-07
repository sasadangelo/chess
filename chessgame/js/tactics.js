// Tactics Gym: puzzle "trova la mossa" generati dalle partite reali dell'utente.
var board = null;
var game = new Chess();

var puzzles = [];
var currentPuzzle = null;
var lastPuzzleId = null;
var attempts = 0;
var solved = false;

var PIECE_NAMES = { p: 'Pedone', n: 'Cavallo', b: 'Alfiere', r: 'Torre', q: 'Donna', k: 'Re' };

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

function populateFilters() {
    var categories = [];
    puzzles.forEach(function(p) {
        if (categories.indexOf(p.Category) === -1) categories.push(p.Category);
    });
    categories.sort().forEach(function(c) {
        $('#categoryFilter').append(new Option(c, c));
    });
}

function filteredPool() {
    var category = $('#categoryFilter').val();
    var difficulty = $('#difficultyFilter').val();
    return puzzles.filter(function(p) {
        return (!category || p.Category === category) && (!difficulty || p.Difficulty === difficulty);
    });
}

function pickRandomPuzzle() {
    var pool = filteredPool();
    if (pool.length === 0) return null;
    var candidates = pool.filter(function(p) { return p.ID !== lastPuzzleId; });
    if (candidates.length === 0) candidates = pool;
    return candidates[Math.floor(Math.random() * candidates.length)];
}

function loadPuzzle() {
    var puzzle = pickRandomPuzzle();
    if (!puzzle) {
        alert('Nessun puzzle disponibile con questi filtri.');
        return;
    }
    currentPuzzle = puzzle;
    lastPuzzleId = puzzle.ID;
    attempts = 0;
    solved = false;

    game.load(puzzle.FEN);
    var orientation = game.turn() === 'b' ? 'black' : 'white';
    board.orientation(orientation);
    board.position(puzzle.FEN);

    $('#feedback').text('').removeClass('correct wrong');
    $('#puzzleInfo').text('Categoria: ' + puzzle.Category + ' | Difficoltà: ' + puzzle.Difficulty);
    $('#showSolutionBtn').hide();
    $('#gameLink')
        .attr('href', puzzle.GameLink)
        .text('Vedi la partita originale (' + puzzle.Date + ', ' + puzzle.Opening + ')')
        .show();
}

function showCorrectFeedback(move) {
    var msg = 'Corretto! ';
    if (move.captured) {
        msg += 'Hai vinto: ' + (PIECE_NAMES[move.captured] || move.captured) + '. ';
    }
    msg += 'Categoria: ' + currentPuzzle.Category + ' (' + currentPuzzle.Difficulty + ').';
    $('#feedback').text(msg).removeClass('wrong').addClass('correct');
}

var config = {
    draggable: false,
    position: 'start'
};

board = Chessboard('board', config);

attachClickToMove(board, game, function(source, target) {
    if (solved || !currentPuzzle) return 'snapback';

    var move = game.move({ from: source, to: target, promotion: 'q' });
    if (move === null) return 'snapback';

    var playedUci = source + target + (move.promotion ? move.promotion : '');
    if (playedUci === currentPuzzle.Solution) {
        solved = true;
        showCorrectFeedback(move);
    } else {
        game.undo();
        attempts++;
        $('#feedback').text('Non corretto, riprova (tentativo ' + attempts + ').').removeClass('correct').addClass('wrong');
        if (attempts >= 2) {
            $('#showSolutionBtn').show();
        }
        return 'snapback';
    }
});

$(window).on('resize', function() { board.resize(); });

$('#newPuzzleBtn').on('click', loadPuzzle);

$('#showSolutionBtn').on('click', function() {
    if (!currentPuzzle || solved) return;
    var uci = currentPuzzle.Solution;
    var move = game.move({ from: uci.substring(0, 2), to: uci.substring(2, 4), promotion: uci.substring(4, 5) || 'q' });
    if (move) {
        board.position(game.fen());
        solved = true;
        $('#feedback')
            .text('Soluzione: ' + uci.substring(0, 2) + '-' + uci.substring(2, 4) + '. Categoria: ' + currentPuzzle.Category + '.')
            .removeClass('wrong').addClass('correct');
        $('#showSolutionBtn').hide();
    }
});

loadCSV('data/tactics_puzzles.csv', function(data) {
    puzzles = data;
    populateFilters();
    if (puzzles.length > 0) {
        loadPuzzle();
    } else {
        $('#feedback').text('Nessun puzzle trovato: genera prima tactics_puzzles.csv (skill chess-tactics-puzzles).');
    }
});
