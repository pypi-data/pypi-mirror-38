import { deprecate } from '../utils/deprecate';
import isArray from '../utils/is-array';
import { createLocal } from '../create/local';

export var prototypeMin = deprecate(
     'moment().min is deprecated, use moment.min instead. https://github.com/moment/moment/issues/1548',
     function () {
         var other = createLocal.apply(null, arguments);
         return other < this ? this : other;
     }
 );

export var prototypeMax = deprecate(
    'moment().max is deprecated, use moment.max instead. https://github.com/moment/moment/issues/1548',
    function () {
        var other = createLocal.apply(null, arguments);
        return other > this ? this : other;
    }
);

// Pick a moment m from moments so that m[fn](other) is true for all
// other. This relies on the function fn to be transitive.
//
// moments should either be an array of moment objects or an array, whose
// first element is an array of moment objects.
function pickBy(fn, moments) {
    var res, i;
    if (moments.length === 1 && isArray(moments[0])) {
        moments = moments[0];
    }
    if (!moments.length) {
        return createLocal();
    }
    res = moments[0];
    for (i = 1; i < moments.length; ++i) {
        if (moments[i][fn](res)) {
            res = moments[i];
        }
    }
    return res;
}

// TODO: Use [].sort instead?
export function min () {
    var args = [].slice.call(arguments, 0);

    return pickBy('isBefore', args);
}

export function max () {
    var args = [].slice.call(arguments, 0);

    return pickBy('isAfter', args);
}
