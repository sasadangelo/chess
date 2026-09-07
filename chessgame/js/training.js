// Sessione di allenamento giornaliera: combina endgame e puzzle tattici dovuti oggi
// secondo la pianificazione di srs.js, in un'unica coda mescolata.
var board = null;
var game = new Chess();
var stockfish = new Worker('js/stockfish.min.js');
var engineRunning = false;

var endgames = [];
var puzzles = [];
var queue = [];
var queueIndex = 0;
var sessionStats = { completed: 0, total: 0 };

var currentMode = null; // 'endgame' | 'puzzle'
var currentEndgameItem = null;
var humanColor = null;
var currentPuzzleItem = null;
var puzzleAttempts = 0;

var PIECE_NAMES = { p: 'Pedone', n: 'Cavallo', b: 'Alfiere', r: 'Torre', q: 'Donna', k: 'Re' };

function loadCSV(file, callback) {
    $.ajax({ url: file, dataType: 'text' }).done(function(data) {
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

function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
}

function renderSettings() {
    var settings = SRS.getSettings();
    $('#maxEndgames').val(settings.maxEndgamesPerDay);
    $('#maxPuzzles').val(settings.maxPuzzlesPerDay);
}

function saveSettingsAndRestart() {
    SRS.saveSettings({
        maxEndgamesPerDay: parseInt($('#maxEndgames').val(), 10) || 0,
        maxPuzzlesPerDay: parseInt($('#maxPuzzles').val(), 10) || 0,
    });
    startSession();
}

function buildQueue() {
    var settings = SRS.getSettings();
    var endgameIds = endgames.map(function(e) { return e.ID; });
    var puzzleIds = puzzles.map(function(p) { return p.ID; });
    var dueEndgameIds = SRS.dueItems(SRS.POOLS.ENDGAMES, endgameIds, settings.maxEndgamesPerDay);
    var duePuzzleIds = SRS.dueItems(SRS.POOLS.PUZZLES, puzzleIds, settings.maxPuzzlesPerDay);

    queue = [];
    dueEndgameIds.forEach(function(id) {
        var item = endgames.filter(function(e) { return e.ID === id; })[0];
        if (item) queue.push({ type: 'endgame', item: item });
    });
    duePuzzleIds.forEach(function(id) {
        var item = puzzles.filter(function(p) { return p.ID === id; })[0];
        if (item) queue.push({ type: 'puzzle', item: item });
    });
    shuffle(queue);
    sessionStats = { completed: 0, total: queue.length };
    queueIndex = 0;
}

function updateProgress() {
    $('#progress').text(queue.length === 0 ? '' : 'Elemento ' + (queueIndex + 1) + ' di ' + queue.length);
}

function startSession() {
    buildQueue();
    updateProgress();
    $('#sessionSummary').hide();
    $('#board').show();
    if (queue.length === 0) {
        showSessionComplete();
        return;
    }
    runCurrentItem();
}

function runCurrentItem() {
    if (queueIndex >= queue.length) {
        showSessionComplete();
        return;
    }
    updateProgress();
    $('#feedback').text('').removeClass('correct wrong');
    var entry = queue[queueIndex];
    if (entry.type === 'endgame') {
        $('#itemTypeLabel').text('Endgame');
        $('#puzzleActions').hide();
        runEndgameItem(entry.item);
    } else {
        $('#itemTypeLabel').text('Puzzle Tattico');
        $('#puzzleActions').show();
        runPuzzleItem(entry.item);
    }
}

function nextItem() {
    sessionStats.completed++;
    queueIndex++;
    setTimeout(runCurrentItem, 1200);
}

function showSessionComplete() {
    $('#itemTypeLabel').text('');
    $('#puzzleInfo').text('');
    $('#puzzleActions').hide();
    $('#feedback').removeClass('correct wrong').text('');
    $('#progress').text('');
    $('#board').hide();
    $('#sessionSummary')
        .text('Hai completato ' + sessionStats.completed + '/' + sessionStats.total + ' esercizi dovuti oggi. Torna domani per i prossimi.')
        .show();
}

// ---- Endgame ----

function runEndgameItem(item) {
    currentMode = 'endgame';
    currentEndgameItem = item;
    game.load(item.FEN);
    humanColor = game.turn();
    board.orientation(humanColor === 'b' ? 'black' : 'white');
    board.position(item.FEN);
    $('#puzzleInfo').text(item.Name + ' — Obiettivo: ' + (item.Objective === 'Win' ? 'Vinci' : 'Pareggia'));
}

function checkEndgameOver() {
    if (!game.game_over()) return false;
    var outcome;
    if (game.in_checkmate()) {
        outcome = (game.turn() === humanColor) ? 'Loss' : 'Win';
    } else {
        outcome = 'Draw';
    }
    handleEndgameOutcome(outcome);
    return true;
}

function handleEndgameOutcome(outcome) {
    var objective = currentEndgameItem.Objective;
    var success = (outcome === 'Win') || (outcome === objective);
    SRS.review(SRS.POOLS.ENDGAMES, currentEndgameItem.ID, success ? 'good' : 'wrong');
    var outcomeLabel = { Win: 'vittoria', Draw: 'patta', Loss: 'sconfitta' }[outcome];
    var msg = (success ? 'Riuscito! ' : 'Non riuscito. ') + 'Esito: ' + outcomeLabel + ' (obiettivo: ' + (objective === 'Win' ? 'vincere' : 'pareggiare') + ').';
    $('#feedback').text(msg).removeClass('correct wrong').addClass(success ? 'correct' : 'wrong');
    nextItem();
}

function makeBestMove() {
    if (checkEndgameOver()) return;
    var fen = game.fen();
    stockfish.postMessage('position fen ' + fen);
    stockfish.postMessage('go depth 15');
    engineRunning = true;
}

stockfish.onmessage = function(event) {
    var message = event.data;
    if (currentMode === 'endgame' && message.includes('bestmove') && engineRunning) {
        var bestMove = message.split(' ')[1];
        var move = game.move(bestMove, { sloppy: true });
        if (move !== null) {
            board.position(game.fen());
            checkEndgameOver();
        }
        engineRunning = false;
    }
};

// ---- Puzzle ----

function runPuzzleItem(item) {
    currentMode = 'puzzle';
    currentPuzzleItem = item;
    puzzleAttempts = 0;
    game.load(item.FEN);
    board.orientation(game.turn() === 'b' ? 'black' : 'white');
    board.position(item.FEN);
    $('#puzzleInfo').text('Categoria: ' + item.Category + ' | Difficoltà: ' + item.Difficulty);
}

function handlePuzzleDrop(source, target) {
    var move = game.move({ from: source, to: target, promotion: 'q' });
    if (move === null) return 'snapback';

    var playedUci = source + target + (move.promotion ? move.promotion : '');
    if (playedUci === currentPuzzleItem.Solution) {
        var quality = puzzleAttempts === 0 ? 'easy' : 'hard';
        SRS.review(SRS.POOLS.PUZZLES, currentPuzzleItem.ID, quality);
        var msg = 'Corretto!';
        if (move.captured) msg += ' Hai vinto: ' + (PIECE_NAMES[move.captured] || move.captured) + '.';
        $('#feedback').text(msg).removeClass('wrong').addClass('correct');
        nextItem();
        return;
    }

    game.undo();
    puzzleAttempts++;
    if (puzzleAttempts >= 2) {
        SRS.review(SRS.POOLS.PUZZLES, currentPuzzleItem.ID, 'wrong');
        var uci = currentPuzzleItem.Solution;
        game.move({ from: uci.substring(0, 2), to: uci.substring(2, 4), promotion: uci.substring(4, 5) || 'q' });
        $('#feedback').text('Non corretto. Soluzione mostrata.').removeClass('correct').addClass('wrong');
        setTimeout(function() { board.position(game.fen()); }, 200);
        nextItem();
        return 'snapback';
    }
    $('#feedback').text('Non corretto, riprova (tentativo ' + puzzleAttempts + ').').removeClass('correct').addClass('wrong');
    return 'snapback';
}

var config = {
    draggable: false,
    position: 'start'
};

board = Chessboard('board', config);

attachClickToMove(board, game, function(source, target) {
    if (currentMode === 'endgame') {
        var move = game.move({ from: source, to: target, promotion: 'q' });
        if (move === null) return 'snapback';
        if (checkEndgameOver()) return;
        window.setTimeout(makeBestMove, 250);
    } else if (currentMode === 'puzzle') {
        return handlePuzzleDrop(source, target);
    }
});

$(window).on('resize', function() { board.resize(); });

renderSettings();

$('#applySettingsBtn').on('click', saveSettingsAndRestart);

loadCSV('data/end_games.csv', function(data) {
    endgames = data;
    loadCSV('data/tactics_puzzles.csv', function(puzzleData) {
        puzzles = puzzleData;
        startSession();
    });
});
