/**
 * Created by Tom on 19-Oct-16.
 */

var world = ( function() {

    function __init(World) {
        var galaxy = World['galaxy'];
    }

    function canvas_fill(canvas_id, tile_id) {
        var c = document.getElementById(canvas_id);
        var ctx = c.getContext("2d");
        var img = document.getElementById(tile_id);
        var pat = ctx.createPattern(img, "repeat");

        ctx.rect(0, 0, c.width, c.height);
        ctx.fillStyle = pat;
        ctx.fill();
    }

    return {
        init: __init,
        canvas_fill: canvas_fill
    };
})();