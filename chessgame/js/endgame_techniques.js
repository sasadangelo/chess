// Spiegazioni delle tecniche di matto, associate alla categoria dell'end game.
// Usate da chessgame.js per popolare il bottone "Come si risolve?".
var STAIRCASE_TECHNIQUE = {
    title: 'Tecnica della scaletta (Staircase Mate)',
    steps: [
        'Bastano i due pezzi a lungo raggio (torri e/o donne): ognuno controlla un\'intera riga o colonna, senza bisogno del proprio re.',
        'Metti un pezzo su una riga adiacente al re nemico, così da bloccargli il passo: il re non può oltrepassarla.',
        'Con l\'altro pezzo dai scacco sulla riga dove si trova il re, costringendolo ad arretrare di una riga.',
        'Scambia i ruoli tra i due pezzi (chi ha dato scacco ora blocca, chi bloccava ora dà scacco) e ripeti, spingendo il re riga dopo riga, come su una scaletta.',
        'Quando il re arriva sull\'ultima riga (la prima o l\'ottava) e non ha più case dove arretrare, dai scacco matto con il pezzo che controlla quella riga.',
        'Attenzione: non avvicinare mai il pezzo "bloccante" alla riga del re, altrimenti potrebbe catturarlo — resta sempre una riga di distanza.'
    ]
};

var BOX_TECHNIQUE = {
    title: 'Tecnica della scatola (Box Method)',
    steps: [
        'Usa prima la sola donna per costruire una "scatola" intorno al re nemico, restando sempre a distanza di cavallo da lui (così non può mai catturarla né darti fastidio).',
        'Ogni volta che il re nemico si muove o resta fermo, restringi la scatola avvicinando la donna di una casella, mantenendo sempre la distanza di cavallo.',
        'Continua a restringere la scatola finché il re nemico è confinato sul bordo della scacchiera.',
        'A quel punto porta il tuo re verso il re avversario, avvicinandoti passo dopo passo con l\'opposizione, per dargli sostegno.',
        'Quando il tuo re è abbastanza vicino, dai scacco matto con la donna su una casella del bordo protetta dal tuo re.',
        'Attenzione allo stallo: finché il matto non è pronto, lascia sempre almeno una casella libera al re nemico.'
    ]
};

var ENDGAME_TECHNIQUES = {
    1: BOX_TECHNIQUE,        // Queen vs King
    2: STAIRCASE_TECHNIQUE,  // Two Rooks vs King
    9: STAIRCASE_TECHNIQUE,  // Two Queens vs King
    10: STAIRCASE_TECHNIQUE  // Queen and Rook vs King
};
