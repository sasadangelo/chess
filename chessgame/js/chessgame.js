        // Inizializza la scacchiera e il gioco
        var board = null;
        var game = new Chess();
        //var stockfish = STOCKFISH(); // Inizializza il motore Stockfish
        var stockfish = new Worker('js/stockfish.min.js');
        var engineRunning = false;

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

        // Aggiungi evento al pulsante per caricare la FEN
        document.getElementById('startBtn').addEventListener('click', function() {
            var fen = document.getElementById('fenInput').value;
            updateBoard(fen);
        });
