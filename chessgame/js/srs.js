// Ripetizione spaziata (SM-2 semplificato), stato persistito in localStorage.
// Usato sia dagli endgame che dai puzzle tattici, in due pool separati.
var SRS = (function() {
    var POOLS = { ENDGAMES: 'srs_endgames', PUZZLES: 'srs_puzzles' };
    var SETTINGS_KEY = 'srs_settings';
    var DEFAULT_SETTINGS = { maxEndgamesPerDay: 5, maxPuzzlesPerDay: 10 };

    function todayStr() {
        return new Date().toISOString().slice(0, 10);
    }

    function loadPool(poolKey) {
        try {
            return JSON.parse(localStorage.getItem(poolKey)) || {};
        } catch (e) {
            return {};
        }
    }

    function savePool(poolKey, pool) {
        localStorage.setItem(poolKey, JSON.stringify(pool));
    }

    function getSettings() {
        try {
            var stored = JSON.parse(localStorage.getItem(SETTINGS_KEY)) || {};
            return Object.assign({}, DEFAULT_SETTINGS, stored);
        } catch (e) {
            return Object.assign({}, DEFAULT_SETTINGS);
        }
    }

    function saveSettings(settings) {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    }

    function getState(poolKey, itemId) {
        var pool = loadPool(poolKey);
        return pool[itemId] || null;
    }

    // Un elemento mai rivisto (state === null) è considerato "dovuto" subito,
    // così entra gradualmente nel pool (il cap giornaliero ne limita l'ingresso).
    function isDue(state, today) {
        if (!state) return true;
        return state.dueDate <= today;
    }

    // Ritorna fino a maxCount ID "dovuti oggi", i più in ritardo per primi.
    function dueItems(poolKey, allIds, maxCount) {
        var pool = loadPool(poolKey);
        var today = todayStr();
        var due = allIds
            .map(function(id) { return { id: id, state: pool[id] || null }; })
            .filter(function(entry) { return isDue(entry.state, today); })
            .sort(function(a, b) {
                var aDate = a.state ? a.state.dueDate : '9999-99-99';
                var bDate = b.state ? b.state.dueDate : '9999-99-99';
                return aDate < bDate ? -1 : aDate > bDate ? 1 : 0;
            });
        return due.slice(0, maxCount).map(function(entry) { return entry.id; });
    }

    function addDays(dateStr, days) {
        var d = new Date(dateStr + 'T00:00:00');
        d.setDate(d.getDate() + days);
        return d.toISOString().slice(0, 10);
    }

    // quality: 'wrong' | 'hard' | 'good' | 'easy'
    function review(poolKey, itemId, quality) {
        var pool = loadPool(poolKey);
        var state = pool[itemId] || { interval: 0, ease: 2.5, repetitions: 0, lapses: 0 };
        var today = todayStr();

        if (quality === 'wrong') {
            state.lapses += 1;
            state.repetitions = 0;
            state.interval = 1;
            state.ease = Math.max(1.3, state.ease - 0.2);
        } else {
            state.repetitions += 1;
            if (state.repetitions === 1) {
                state.interval = 1;
            } else if (state.repetitions === 2) {
                state.interval = 6;
            } else {
                state.interval = Math.round(state.interval * state.ease);
            }
            if (quality === 'hard') {
                state.ease = Math.max(1.3, state.ease - 0.15);
            } else if (quality === 'easy') {
                state.ease = Math.min(2.5, state.ease + 0.15);
            }
        }

        state.dueDate = addDays(today, state.interval);
        state.lastReviewed = today;
        pool[itemId] = state;
        savePool(poolKey, pool);
        return state;
    }

    return {
        POOLS: POOLS,
        getSettings: getSettings,
        saveSettings: saveSettings,
        dueItems: dueItems,
        review: review,
        getState: getState,
        todayStr: todayStr,
    };
})();
