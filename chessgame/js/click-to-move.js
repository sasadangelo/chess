// Tap-to-move per chessboard.js: tocca un pezzo per vedere le mosse possibili,
// poi tocca la casella di destinazione per muovere. Sostituisce il drag,
// che su mobile fa scrollare la pagina insieme al pezzo trascinato.
function attachClickToMove(board, game, onMove) {
    var selected = null;

    function clearHighlights() {
        $('#board .square-55d63').removeClass('highlight1-32417 move-hint move-hint-capture');
    }

    function showHints(square) {
        $('[data-square="' + square + '"]').addClass('highlight1-32417');
        game.moves({ square: square, verbose: true }).forEach(function(move) {
            $('[data-square="' + move.to + '"]').addClass(move.captured ? 'move-hint-capture' : 'move-hint');
        });
    }

    $('#board').on('click', '.square-55d63', function() {
        var square = $(this).attr('data-square');
        if (!square) return;

        if (selected === square) {
            clearHighlights();
            selected = null;
            return;
        }

        if (selected) {
            var legalMoves = game.moves({ square: selected, verbose: true });
            var isLegal = legalMoves.some(function(move) { return move.to === square; });
            if (isLegal) {
                var from = selected;
                clearHighlights();
                selected = null;
                var result = onMove(from, square);
                if (result !== 'snapback') {
                    board.position(game.fen());
                }
                return;
            }
        }

        clearHighlights();
        var piece = game.get(square);
        if (piece && piece.color === game.turn()) {
            selected = square;
            showHints(square);
        } else {
            selected = null;
        }
    });
}
