Effect = new function() {
}

Effect.Loop = function(callbacks) {
    this.maxSteps = -1;
    this.startStep = 0;
    this.curStep = 0;
    this.delay = .25;
    this.running = false;
    this.callbacks = callbacks;
}

update(Effect.Loop.prototype, {

    run: function() {
        this.running = true;
        this.done = false;
        this.loop(this);
    },

    loop: function() {
        if( this.running == true && ( this.maxSteps != -1 && this.curStep < this.maxSteps) ) {
            this.callbacks.onStep(this);
            this.curStep++;
            setTimeout(bind(this.loop, this), this.delay);
        }
        else {
            if( this.callbacks.onDone )
                this.callbacks.onDone(this);
        }
    }

});

// based on the scriptaculous script
Effect.highlight = function(element, options) {
    element = $(element);
    options = update({
        time: 1,
        startColor:   Color.fromHexString("#ffff99"),
        endColor:  Color.fromBackground(element),
        numSteps: 8
    }, options);

    var startRgb = options.startColor.asRGB();
    var endRgb = options.endColor.asRGB();
    var rgbDelta = {
        r: endRgb.r - startRgb.r,
        g: endRgb.g - startRgb.g,
        b: endRgb.b - startRgb.b
    };
    var rgbSteps = {
        r: rgbDelta.r / options.numSteps,
        b: rgbDelta.b / options.numSteps,
        g: rgbDelta.g / options.numSteps
    }
    var curColor = clone(startRgb);
    var loop = new Effect.Loop({
        onStep: function(loop) {
            curColor = {
                r: curColor.r + rgbSteps.r,
                g: curColor.g + rgbSteps.g,
                b: curColor.b + rgbSteps.b
            }
            element.style.backgroundColor = Color.fromRGB(curColor);
        },

        onDone: function(loop) {
            element.style.backgroundColor = options.endColor;
            //options.endColor.toHexString();
        }

    });

    loop.maxSteps = options.numSteps;
    loop.delay = (options.time / options.numSteps) * 1000;
    loop.run()
}

Effect.pulse = function(element, options) {
    Effect.fadeOut(element, options);
}

/**
 *  Fade an element in.
 *  element - The element to fade in.
 *  time    - The time in seconds (can be a decimal) to fully fade in.
 */
Effect.fadeIn = function(element, options) {
    element = $(element);
    var curOpacity = 0.0;

    options = update({
        time: 1,
        endOpacity: 1.0,
        step: .05
    }, options);

    Effect.setOpacity(element, curOpacity);
    showElement(element);

    var loop = new Effect.Loop({
        onStep: function(loop) {
            curOpacity += options.step;
            Effect.setOpacity(element, curOpacity);
        },
        onDone: function(loop) {
            Effect.setOpacity(element, options.endOpacity);
        }

    });

    loop.maxSteps = Math.floor((options.endOpacity - curOpacity) / options.step);

    loop.delay = (options.time / loop.maxSteps) * 1000;

    loop.run();
}

/**
 *  Fade an element out.
 *  element - The element to fade out.
 *  time    - The time in seconds (can be a decimal) to fully fade out.
 */
Effect.fadeOut = function(element, options) {
    var curOpacity = Effect.getOpacity(element) || 1.0;

    options = update({
        time: .5,
        endOpacity: 0.0,
        step: .05
    }, options);



    var loop = new Effect.Loop({
        onStep: function(loop) {
            Effect.setOpacity(element, curOpacity);
            curOpacity -= options.step;
        },

        onDone: function(loop) {
            hideElement(element);
        }

    });

    loop.maxSteps = Math.floor((curOpacity - options.endOpacity) / options.step);
    loop.delay = (options.time / loop.maxSteps) * 1000;
    loop.run();
}

//
// Taken from scriptaculous
//
Effect.setOpacity = function(element, value) {
    element = $(element);
    var els = element.style;
    if( value == 1 ) {
        els.opacity = '0.999999';
        if( /MSIE/.test(navigator.userAgent) )
            els.filter = element.style.filter.replace(/alpha\([^\)]*\)/gi, '');
    }
    else {
        if( value < 0.00001 ) value = 0;
        els.opacity = value;
        if( /MSIE/.test(navigator.userAgent) )
            els.filter = element.style.filter.replace(/alpha\([^\)]*\)/gi, '') +
                         "alpha(opacity=" + value * 100 + ")";
    }
}

//
// Taken from scriptaculous
//
Effect.getOpacity = function(element) {
    var opacity;
    if( opacity = element.style.opacity )
        return parseFloat(opacity);
    if( opacity = (element.style.filter || '').match(/alpha\(opacity=(.*)\)/) )
        if( opacity[1] ) return parseFloat(opacity[1]) / 100;
    return 1.0;
}